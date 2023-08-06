from __future__ import print_function

import datetime
import logging
import os
import re
import sys
import uuid
import zipfile
from distutils.spawn import find_executable
from shutil import rmtree
import json
import base64

import pydicom
import easyprocess
import magic
import pathos
import requests
from pyunpack import Archive
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import configargparse


class XnatUploadTool:
    def __init__(self, **kwargs):
        # Designed to be called from script using argparse, otherwise dict must be passed in as kwargs with
        # all following variables set
        try:
            self.args = kwargs
            self.starttime = None
            self.httpsess = None
            self.lastrenew = None
            self.logger = None
            self.prearcdate = False
            self.host = kwargs['host']
            self.localval = dict()
            self.upload_time = int()
            self.build_time = int()
            self.archive_time = int()

            # Pull u/p from env if not set in args
            if kwargs['username'] is None or kwargs['password'] is None:
                (self.username, self.password) = os.environ['XNATCREDS'].split(':', 2)
            else:
                self.username = kwargs['username']
                self.password = kwargs['password']

            self.timeout = kwargs['timeout']
            self.sessiontimeout = datetime.timedelta(minutes=kwargs['sessiontimeout'])

            self.target = kwargs['target']
            self.project = kwargs['project']
            self.session = kwargs['session']
            self.subject = kwargs['subject']
            self.scan = kwargs['scan']
            self.datatype = kwargs['datatype']
            self.xmlnamespace = kwargs['xmlnamespace']
            if kwargs['bsubjectheaders']:
                self.subjectheaders = json.loads(base64.b64decode(kwargs['bsubjectheaders']))
            else:
                self.subjectheaders = json.loads(kwargs['subjectheaders'])

            if kwargs['bsessionheaders']:
                self.sessionheaders = json.loads(base64.b64decode(kwargs['bsessionheaders']))
            else:
                self.sessionheaders = json.loads(kwargs['sessionheaders'])

            if kwargs['bscanheaders']:
                self.scanheaders = json.loads(base64.b64decode(kwargs['bscanheaders']))
            else:
                self.scanheaders = json.loads(kwargs['scanheaders'])

            self.resource = kwargs['resource']

            if 'jobs' in kwargs and kwargs['jobs'] is not None:
                self.threads = kwargs['jobs']
            else:
                self.threads = 1
            self.logfile = kwargs['logfile']
            self.tmpdir = kwargs['tmpdir']
            self.validate = kwargs['validate']
            self.raw = kwargs['raw']
            self.verbose = kwargs['verbose']

            self.filetree = {self.target: {}}
            self.ingestconfig = None

            if kwargs['ingestconfig']:
                parser = configargparse.ArgumentParser()
                self.ingestconfig = parser.parse_args(default_config_files=[kwargs['ingestconfig']])

            # Set up logging
            self.setup_logger()

            # Initialize Sessions
            self.renew_session()
        except KeyError as e:
            logging.error('Unable to initialize uploader, missing argument: %s' % str(e))
            exit(1)

    def setup_upload(self):
        # Check for project
        self.logger.debug('Preparing for upload to %s from %s as %s: declared type %s' %
                          (self.host, self.target, self.username, self.datatype))
        self.logger.debug('Checking status for %s/%s/%s' % (self.project, self.subject, self.session))
        if self.check_project() is not True:
            self.logger.error("Project %s does not exist" % self.project)
            exit(1)

        # If not running configured for filesystem ingestion
        # Check for subject and session, attempt to create for non dicom
        # Ingestion will handle the whole filesystem processing differently
        if self.datatype != 'dicom':
            if self.check_subject(create=True) is not True:
                self.logger.error("Subject %s does not exist and cannot be created on project %s" %
                                  (self.subject, self.project))
                exit(1)

            if self.check_session(create=True) is not True:
                self.logger.error("Session %s does not exist and cannot be created for project %s/subject %s" %
                                  (self.session, self.project, self.subject))
                exit(1)

            if self.check_scan(create=True) is not True:
                self.logger.error("Scan %s does not exist and cannot be created for project %s/subject %s/session %s" %
                                  (self.scan, self.session, self.subject, self.project))
                exit(1)

        return True

    def start_upload(self):
        self.setup_upload()

        self.starttime = datetime.datetime.now()
        self.logger.info("Starting upload of %s to %s/%s/%s/%s" % (self.target, self.host, self.project,
                                                                   self.subject, self.session))

        # Analyze dir structure to see if tar.gz is present
        self.logger.debug("Analyzing target %s" % self.target)
        # If scan, expect single dir with files in it for a scan
        if self.scan is not True:
            self.analyze_dir(self.target + '/' + self.scan)
        else:
            self.analyze_dir(self.target)

        results = list()
        if os.path.isfile(self.target):
            # If a single file fire it off
            results.append(self.upload_singlefile(self.scan))
        elif self.scan or self.threads < 2:
            # If a single scan or a single thread don't use mp pool
            if self.scan:
                # Expect a single dir with files in it for a scan
                results.append(self.process_scan(self.target, self.filetree))
            else:
                # Expect a subdir for each scan and parallelize
                for scan in self.filetree[self.target]:
                    results.append(self.process_scan(scan, self.filetree))
        else:
            # Execute as multiprocessor job
            p = pathos.pools.ProcessPool(self.threads)
            scans = list()
            filetrees = list()
            for scan in self.filetree[self.target]:
                scans.append(scan)
                filetrees.append(self.filetree)

            # Launch pool and collect results
            results = p.map(self.process_scan, scans, filetrees)

        # Tally results
        for thisresult in results:
            if len(thisresult) > 1 and thisresult[2] is not None and re.match(r'[0-9]+_[0-9]+', str(thisresult[2])):
                self.prearcdate = thisresult[2]
                self.localval.update(thisresult[1])

        self.upload_time = (datetime.datetime.now() - self.starttime).total_seconds()
        self.logger.info('All uploads complete in %ds [Proj %s Sub %s Sess %s]' % (
            self.upload_time, self.project, self.subject, self.session))
        lastend = datetime.datetime.now()

        # Check that prearcdate is set and has proper format, then build and archive session
        if self.datatype == 'dicom':
            if self.prearcdate is not False and re.match(r'[0-9]+_[0-9]+', str(self.prearcdate)):
                self.logger.info('Starting post processing')
                prearcpathfinal = "/data/prearchive/projects/%s/%s/%s" % (self.project, self.prearcdate, self.session)
                proctime = datetime.datetime.now()
                self.renew_session()
                try:
                    r = self.httpsess.post(url=self.host + prearcpathfinal, params={'action': 'build'},
                                           timeout=(30, self.timeout))
                except requests.exceptions.ReadTimeout:
                    self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                                      (scan, self.timeout))
                if r.status_code == 200:
                    self.build_time = (datetime.datetime.now() - lastend).total_seconds()
                    self.logger.info('Build Successful in %ds: %s' % (self.build_time, prearcpathfinal))
                    lastend = datetime.datetime.now()
                else:
                    self.logger.error('Build Failed: %s, (%s)', prearcpathfinal, r.status_code)
                self.renew_session()
                r = self.httpsess.post(url=(self.host + "/data/services/archive"), params={'src': prearcpathfinal},
                                       timeout=(30, self.timeout))
                if r.status_code == 200:
                    self.archive_time = (datetime.datetime.now() - lastend).total_seconds()
                    self.logger.info('Archive Successful in %ds: %s' % (self.archive_time, prearcpathfinal))
                else:
                    self.logger.error('Archive Failed: %s, (%s)', prearcpathfinal, r.reason)

                self.logger.info('Processing complete, runtime %ds [Proj %s Sub %s Sess %s]' %
                                 ((datetime.datetime.now() - proctime).total_seconds(), self.project, self.subject,
                                  self.session))
            else:
                self.logger.error('Unable to build and archive, no uploads succeeded [Proj %s Sub %s Sess %s]' %
                                  (self.project, self.subject, self.session))
                exit(1)

            if self.validate:
                # Compare local file data to uploaded data
                self.logger.info('Upload Validation:')
                scan_ssum = 0
                scan_lsum = 0
                scansserver = self.get_serverscans()
                scanslocal = self.localval

                for thisscan in scanslocal:
                    scan_dcomp = (scanslocal[thisscan]['desc'] == scansserver[thisscan]['desc'])
                    scan_ccomp = (scanslocal[thisscan]['count'] == scansserver[thisscan]['count'])

                    if scan_dcomp and scan_ccomp:
                        self.logger.info('MATCH: Series %d (%s/%s)/%d files: [Series: %s] [Count: %s]' %
                                         (thisscan, scanslocal[thisscan]['localname'], scanslocal[thisscan]['desc'],
                                          scanslocal[thisscan]['count'], str(scan_dcomp), str(scan_ccomp)))
                    else:
                        if scan_ccomp is False:
                            scan_ccomp = ('%s: %s local vs %s remote' % (scan_ccomp, scanslocal[thisscan]['count'],
                                                                         scansserver[thisscan]['count']))
                        if scan_dcomp is False:
                            scan_dcomp = ('%s: %s local vs %s remote' % (scan_dcomp, scanslocal[thisscan]['desc'],
                                                                         scansserver[thisscan]['desc']))

                        self.logger.error('ERROR: Series %d (%s/%s)/%d files: [Series: %s] [Count %s]' %
                                          (thisscan, scanslocal[thisscan]['localname'], scanslocal[thisscan]['desc'],
                                           scanslocal[thisscan]['count'], str(scan_dcomp), str(scan_ccomp)))
                    scan_ssum += scanslocal[thisscan]['count']
                    scan_lsum += scansserver[thisscan]['count']
                if scan_ssum == scan_lsum:
                    self.logger.info('MATCH: [Source files %d]/[Server files %d]' % (scan_ssum, scan_lsum))
                else:
                    self.logger.info('ERROR: [Source files %d]/[Server files %d]' % (scan_ssum, scan_lsum))
            else:
                self.logger.info('Validation disabled, assuming success')

        self.logger.info("Completed upload of %s in %ss" % (
            self.target, str(datetime.datetime.now() - self.starttime).split('.')[0],))

        self.logger.debug("%d,%d,%d" % (self.upload_time, self.build_time, self.archive_time))

        return True

    def process_scan(self, scan, filetree):
        # Process a directory of scans, to be parallelized
        valdata = dict()
        prearcdate = None
        filecount = 0
        zcount = 0

        if scan == '.':
            self.logger.debug("[%s] Starting upload", self.target)
        else:
            self.logger.debug("[%s] Starting upload", scan)

        if self.raw is True:
            # If raw is set, decompress archive files and upload individually
            if os.path.isfile(self.target):
                self.upload_singlefile(scan)
                filecount = 1
            elif self.scan:
                self.upload_datafile(targetdir=self.target, scan=scan)
            else:
                for thisarchive in filetree[self.target][scan]['archives']:
                    mytmpdir = self.tmpdir + '/xnat-upload-' + uuid.uuid4().hex
                    os.mkdir(mytmpdir)
                    targetarchive = os.path.join(self.target, scan, thisarchive)

                    # Decompression
                    self.logger.debug("[%s] Decompressing %s to %s" % (scan, targetarchive, mytmpdir))
                    Archive(targetarchive).extractall(mytmpdir)

                    # Gather source data information for later validation of upload
                    if self.validate:
                        (zcount, valdata[scan]) = self.validate_dicom_session(mytmpdir, scan)
                        filecount += zcount

                    # Upload
                    self.renew_session()
                    prearcdate = self.upload_rawscan(targetdir=mytmpdir, scan=scan)

                    # Cleanup
                    self.logger.debug("[%s] Cleaning up %s " % (scan, mytmpdir))
                    rmtree(mytmpdir)

                if self.datatype == 'dcm':
                    if len(self.filetree[self.target][scan]['dcmfiles']) > 0:
                        self.renew_session()
                        # Gather source data information for later validation of upload
                        if self.validate:
                            valdata[scan] = self.validate_dicom_session(os.path.join(self.target, scan), scan)
                        # Upload all files in scan dir
                        prearcdate = self.upload_rawscan(targetdir=os.path.join(self.target, scan), scan=scan)
                elif len(self.filetree[self.target][scan]['otherfiles']) > 0:
                    self.renew_session()
                    # Upload all files in scan dir
                    self.upload_datafiles(targetdir=os.path.join(self.target, scan), scan=scan)

        else:
            # Decompress existing archives and rezip files to take advantage of zip handler
            for thisarchive in filetree[self.target][scan]['archives']:
                # Decompress in order to analyze contents
                if scan == thisarchive:
                    targetarchive = os.path.join(self.target, thisarchive)
                else:
                    targetarchive = os.path.join(self.target, scan, thisarchive)
                mytmpdir = self.tmpdir + '/xnat-upload-' + uuid.uuid4().hex
                os.mkdir(mytmpdir)
                self.logger.debug("[%s] Decompressing %s to %s" % (scan, targetarchive, mytmpdir))
                Archive(targetarchive).extractall(mytmpdir)
                # Gather source data information for later validation of upload
                if self.validate:
                    (zcount, valdata) = self.validate_dicom_session(mytmpdir, scan)
                    filecount += zcount
                # Recompress for upload
                myzipfile = ("%s/%s.zip" % (self.tmpdir, uuid.uuid4().hex))
                self.logger.debug("[%s] Recompressing %s (%s files) as %s" %
                                  (scan, mytmpdir, len(os.listdir(mytmpdir)), myzipfile))
                self.zipdir(path=mytmpdir, targetzip=myzipfile)
                dccount = str()
                if zcount > 0:
                    dccount = (" w/ (%s valid dicom files)", zcount)
                self.logger.debug("[%s] Recompressed %s%s as %s" %
                                  (scan, mytmpdir, dccount, myzipfile))
                # Upload to server
                self.renew_session()
                try:
                    prearcdate = self.upload_zipscan(targetzip=myzipfile, scan=scan)
                except requests.exceptions.ReadTimeout:
                    self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                                      (scan, self.timeout))
                # Cleanup
                self.logger.debug("[%s] Cleaning up %s & %s" % (scan, mytmpdir, myzipfile))
                rmtree(mytmpdir)
                os.remove(myzipfile)

            # Zip raw files to take advantage of zip handler
            if len(self.filetree[self.target][scan]['dcmfiles']) > 0:
                # Gather source data information for later validation of upload
                mytmpdir = self.tmpdir + '/xnat-upload-' + uuid.uuid4().hex
                os.mkdir(mytmpdir)
                myzipfile = ("%s/%s.zip" % (mytmpdir, scan))
                mysourcedir = os.path.join(self.target, scan)
                self.logger.debug("[%s] Recompressing %s as %s" % (scan, mysourcedir, myzipfile))
                if self.validate:
                    (zcount, valdata) = self.validate_dicom_session(mysourcedir, scan)
                    filecount += zcount
                # Compress
                self.zipdir(path=mysourcedir, targetzip=myzipfile)
                dccount = str()
                if zcount > 0:
                    dccount = (" w/ (%s valid dicom files)", zcount)
                self.logger.debug("[%s] Recompressed %s%s as %s" %
                                  (scan, mytmpdir, dccount, myzipfile))
                # Upload
                self.renew_session()
                prearcdate = self.upload_zipscan(targetzip=myzipfile, scan=scan)
                # Cleanup
                self.logger.debug("[%s] Cleaning up %s" % (scan, myzipfile))
                rmtree(mytmpdir)
        return scan, valdata, prearcdate, filecount

    def renew_session(self):
        # Set up request session and get cookie
        if self.lastrenew is None or ((self.lastrenew + self.sessiontimeout) < datetime.datetime.now()):
            # Renew expired session, or set up new session
            self.httpsess = requests.Session()

            # Retry logic
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            self.httpsess.mount('http://', adapter)
            self.httpsess.mount('https://', adapter)

            # Log in and generate xnat session
            response = self.httpsess.post(self.host + '/data/JSESSION', auth=(self.username, self.password),
                                          timeout=(30, self.timeout))
            if response.status_code != 200:
                self.logger.error("Session renewal failed, no session acquired: %d %s" % (response.status_code,
                                                                                          response.reason))
                exit(1)

            self.lastrenew = datetime.datetime.now()

        return True

    def setup_logger(self):
        # Set up logging
        if self.logfile is not None:
            hdlr = logging.FileHandler(self.logfile)
        else:
            hdlr = logging.StreamHandler(sys.stdout)

        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        return True

    def bytes_format(self, number_of_bytes):
        # Formats byte to human readable text
        if number_of_bytes < 0:
            raise ValueError("number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return str(number_of_bytes) + ' ' + unit

    def archive_test(self, filepath, timeout=10):
        # Tests archive validity
        patool_path = find_executable("patool")
        if not patool_path:
            raise ValueError('patool not found! Please install patool!')
        p = easyprocess.EasyProcess([
            sys.executable,
            patool_path,
            '--non-interactive',
            'test',
            filepath
        ]).call(timeout=timeout)
        if p.return_code:
            return False
        return True

    def analyze_dir(self, directory):
        # Don't bother with single file
        if os.path.isfile(self.target):
            return True
        # Analyze directory tree to find map of uploadable files
        if os.path.exists(directory):
            for d, r, f in os.walk(directory):
                # Cycle through directories
                for subdir in r:
                    if subdir.startswith(".") is not True and subdir not in self.filetree:
                        self.filetree[directory][subdir] = {'dcmfiles': list(), 'archives': list(),
                                                            'otherfiles': list()}
                for subfile in f:
                    if subfile.startswith('.'):
                        self.logger.debug('Hidden file %s skipped' % subfile)
                    else:
                        mysubdir = os.path.basename(os.path.normpath(d))
                        mypath = os.path.join(d, subfile)
                        mime_type = magic.from_file(mypath, mime=True)
                        if mysubdir not in self.filetree[directory]:
                            self.filetree[directory][mysubdir] = {'dcmfiles': list(), 'archives': list(),
                                                                  'otherfiles': list()}
                        if mime_type == 'application/dicom':
                            self.filetree[directory][mysubdir]['dcmfiles'].append(subfile)

                            session_fields = None
                            subject_fields = None
                            # Check if user wants to pull subject and/or session from first dicom file
                            if self.subject is not None:
                                subject_fields = re.search('\(([0-9a-fA-F]+)\,([0-9a-fA-F]+)\)', self.subject)

                            if self.session is not None:
                                session_fields = re.search('\(([0-9a-fA-F]+)\,([0-9a-fA-F]+)\)', self.session)

                            td = pydicom.read_file(os.path.join(directory, mysubdir, subfile))
                            if subject_fields is not None:
                                # Set subject
                                self.logger.info('Dicom tag %s specified for subject' % self.subject)
                                self.subject = td[hex(int(subject_fields.group(1), 16)),
                                                  hex(int(subject_fields.group(2), 16))].value.replace(" ", "_")
                                self.logger.info('Subject set to tag value: %s ' % self.subject)
                            if session_fields is not None:
                                # Set session
                                self.logger.info('Dicom tag %s specified for session' % self.session)
                                self.session = td[hex(int(session_fields.group(1), 16)),
                                                  hex(int(session_fields.group(2), 16))].value.replace(" ", "_")
                                self.logger.info('Session set to tag value: %s' % self.session)
                        elif self.archive_test(mypath):
                            if d == directory:
                                self.filetree[directory][subfile] = {'dcmfiles': list(), 'archives': [subfile],
                                                                     'otherfiles': list()}
                            else:
                                self.filetree[directory][mysubdir]['archives'].append(subfile)
                        else:
                            self.logger.debug("File %s/%s non-dicom or archive: %s" % (d, subfile, str(mime_type)))
                            self.filetree[directory][mysubdir]['otherfiles'].append(subfile)
        else:
            self.logger.error('Directory %s does not exist' % (os.path.abspath(directory)))
            exit(1)

        return True

    def upload_zipscan(self, targetzip, scan):
        # Uploads a compressed zipfile of scans
        zipsize = os.path.getsize(targetzip)

        self.logger.info('[%s] Uploading zipfile %s (%s) to [Proj %s Sub %s Sess %s Scan %s]' %
                         (scan, targetzip, self.bytes_format(zipsize), self.project, self.subject, self.session, scan))

        bwstarttime = datetime.datetime.now()
        mypayload = dict()
        mydata = open(targetzip, 'rb')
        mypayload['import-handler'] = 'DICOM-zip'
        mypayload['inbody'] = 'true'
        mypayload['PROJECT_ID'] = self.project
        mypayload['SUBJECT_ID'] = self.subject
        mypayload['EXPT_LABEL'] = self.session

        try:
            r = self.httpsess.post(url=(self.host + "/data/services/import"), params=mypayload, data=mydata,
                                   timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout:
            self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                              (scan, self.timeout))

        if r.status_code == 200 and (len(r.text.split('/')) > 4):
            prearcdate = r.text.split('/')[5]
            if self.session is None:
                self.session = r.text.split('/')[6]
                self.session = self.session.strip('\n');
                self.session = self.session.strip('\r');
            transtime = (datetime.datetime.now() - bwstarttime).total_seconds()
            self.logger.info('[%s] Uploaded zipfile (runtime %ds)' % (scan, transtime))
            return prearcdate
        else:
            transtime = (datetime.datetime.now() - bwstarttime).total_seconds()
            self.logger.error('[%s] Failed to upload zipfile (runtime %ds): %s' %
                              (scan, transtime, r.reason))
            return False

    def upload_subzip(self, targetzip, scan):
        # Uploads a compressed file directly from scan subdir, taking dir name as scan name
        zipsize = os.path.getsize(os.path.join(targetzip))

        self.logger.info('[%s] Uploading zipfile %s (%s) to [Proj %s Sub %s Sess %s Scan %s]' %
                         (scan, targetzip, self.bytes_format(zipsize), self.project, self.subject, self.session, scan))

        bwstarttime = datetime.datetime.now()
        mypayload = dict()
        mydata = open(targetzip, 'rb')
        mypayload['import-handler'] = 'DICOM-zip'
        mypayload['inbody'] = 'true'
        mypayload['PROJECT_ID'] = self.project
        mypayload['SUBJECT_ID'] = self.subject
        mypayload['EXPT_LABEL'] = self.session

        try:
            r = self.httpsess.post(url=(self.host + "/data/services/import"), params=mypayload, data=mydata,
                                   timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout:
            self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                              (scan, self.timeout))

        if r.status_code == 200:
            prearcdate = r.text.split('/')[5]
            if self.session is None:
                self.session = r.text.split('/')[6]
                self.session = self.session.strip('\n');
                self.session = self.session.strip('\r');
            transtime = (datetime.datetime.now() - bwstarttime).total_seconds()
            self.logger.info('[%s] Uploaded zipfile (runtime %ds)' % (scan, transtime))
            return prearcdate
        else:
            transtime = (datetime.datetime.now() - bwstarttime).total_seconds()
            self.logger.error('[%s] Upload failed for zipfile, (runtime %ds): %s' %
                              (scan, transtime, r.reason))
            return False

    def upload_rawscan(self, targetdir, scan):
        # Upload dcm files individually from directory
        targetfiles = list()
        badfiles = list()
        self.logger.debug('[%s] Analyzing %d mimetypes in %s' % (scan, len(os.listdir(targetdir)), targetdir))
        sumsize = 0
        for thisfile in os.listdir(targetdir):
            if magic.from_file(os.path.join(targetdir, thisfile), mime=True) == 'application/dicom':
                targetfiles.append(thisfile)
                sumsize = sumsize + os.path.getsize(os.path.join(targetdir, os.path.join(targetdir, thisfile)))
            else:
                badfiles.append(thisfile)

        if sumsize == 0:
            self.logger.info('[%s] No files suitable for transfer. Skipping', scan)
            return False

        self.logger.info('[%s] Uploading %d dcm files (%s) to [Proj %s Sub %s Sess %s Scan %s], skipping %d '
                         'unsupported files' % (scan, len(targetfiles), self.bytes_format(sumsize), self.project,
                                                self.subject, self.session, scan, len(badfiles)))

        bwstarttime = datetime.datetime.now()
        prearcdate = None
        failreason = None
        upstat = {'success': 0, 'failure': 0, 'total': 0}
        for thisdcm in targetfiles:
            mypayload = dict()
            mydata = open(os.path.join(targetdir, thisdcm), 'rb')
            mypayload['import-handler'] = 'gradual-DICOM'
            mypayload['inbody'] = 'true'
            mypayload['PROJECT_ID'] = self.project
            mypayload['SUBJECT_ID'] = self.subject
            mypayload['EXPT_LABEL'] = self.session

            try:
                r = self.httpsess.post(url=(self.host + "/data/services/import"), params=mypayload, data=mydata,
                                       timeout=(30, self.timeout))
            except requests.exceptions.ReadTimeout:
                self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                                  (scan, self.timeout))

            if r.status_code == 200:
                upstat['success'] += 1
                prearcdate = r.text.split('/')[5]
            else:
                upstat['failure'] += 1
                failreason = r.reason

            upstat['total'] += 1

        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

        if prearcdate:
            self.logger.info('[%s] Transferred %d files (%d/%d sucessful) (runtime %ds)' %
                             (scan, len(targetfiles), upstat['success'], upstat['total'], transtime))
            return prearcdate
        else:
            self.logger.error('[%s] Failed to transfer %d files (%d/%d sucessful), (runtime %ds): last failure %s' %
                              (scan, len(targetfiles), upstat['failure'], upstat['total'], transtime, failreason))
            return False

    def upload_datafiles(self, targetdir, scan):
        # Upload generic data files individually from directory
        targetfiles = list()

        self.logger.debug('[%s] Analyzing %d datafile in %s' % (scan, len(os.listdir(targetdir)), targetdir))
        sumsize = 0

        if self.scan:
            if os.path.isdir(os.path.join(targetdir, scan, self.scan)):
                mypath = os.path.join(targetdir, scan, self.scan)
            else:
                self.logger.error('Path %s for scan %s does not exist' %
                                  (os.path.join(targetdir, scan, self.scan), self.scan))
                return False
        else:
            mypath = os.path.join(targetdir, scan)

        for thisfile in os.listdir(mypath):
            if thisfile.startswith('.') is not True:
                targetfiles.append(thisfile)
                sumsize = sumsize + os.path.getsize(os.path.join(mypath, thisfile))

        if sumsize == 0:
            self.logger.info('[%s] No files suitable for transfer. Skipping', scan)
            return False

        self.logger.info('[%s] Uploading %d data files (%s) of type %s to [Proj %s Sub %s Sess %s Folder %s]' %
                         (scan, len(targetfiles), self.bytes_format(sumsize), self.datatype, self.project, self.subject,
                          self.session, self.resource))

        bwstarttime = datetime.datetime.now()
        upstat = {'success': 0, 'failure': 0, 'total': 0}
        myurl = ("%s/data/projects/%s/subjects/%s/experiments/%s" %
                 (self.host, self.project, self.subject, self.session))
        if self.scan:
            myurl = ("%s/scans/%s" % (myurl, self.scan))

        for thisfile in targetfiles:
            mypayload = dict()
            mydata = open(os.path.join(mypath, thisfile), 'rb')

            try:
                myurl = ("%s/resources/%s/files/%s?inbody=true&update-stats=true&event_reason=batch-upload"
                         "&event_action=Uploaded-%s" % (myurl, self.resource, thisfile, self.datatype))
                response = self.httpsess.post(url=myurl, params=mypayload, data=mydata,
                                              timeout=(30, self.timeout))
            except requests.exceptions.ReadTimeout:
                self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                                  (scan, self.timeout))

            if response.status_code == 200:
                upstat['success'] += 1
            else:
                upstat['failure'] += 1

            upstat['total'] += 1

        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

        self.logger.info('[%s] Transferred %d files (%d/%d sucessful) (runtime %ds)' %
                         (scan, len(targetfiles), upstat['success'], upstat['total'], transtime))
        return None

    def upload_singlefile(self, scan):
        # Upload generic data files individually

        self.logger.debug('[%s] Analyzing datafile in %s' % (scan, self.target))
        sumsize = os.path.getsize(self.target)

        if sumsize == 0:
            self.logger.info('[%s] No files suitable for transfer. Skipping', scan)
            return False

        self.logger.info('[%s] Uploading data file (%s) of type %s to [Proj %s Sub %s Sess %s Folder %s]' %
                         (scan, self.bytes_format(sumsize), self.datatype, self.project, self.subject,
                          self.session, self.resource))

        bwstarttime = datetime.datetime.now()
        upstat = {'success': 0, 'failure': 0, 'total': 0}
        myurl = ("%s/data/projects/%s/subjects/%s/experiments/%s" %
                 (self.host, self.project, self.subject, self.session))
        if self.scan:
            myurl = ("%s/scans/%s" % (myurl, scan))
        mypayload = self.scanheaders
        mydata = open(self.target, 'rb')

        try:
            myurl = ("%s/resources/%s/files/%s?inbody=true&update-stats=true&event_reason=batch-upload"
                     "&event_action=Uploaded-%s" %
                     (myurl, self.resource, os.path.basename(self.target), self.datatype))
            response = self.httpsess.post(url=myurl, params=mypayload, data=mydata, timeout=(30, self.timeout))
        except requests.exceptions.ReadTimeout:
            self.logger.error("[%s] failed to upload due to read timeout, increase default from %d" %
                              (scan, self.timeout))

        if response.status_code == 200:
            upstat['success'] += 1
        else:
            upstat['failure'] += 1

        upstat['total'] += 1

        transtime = (datetime.datetime.now() - bwstarttime).total_seconds()

        self.logger.info('[%s] Transferred %d files (%d/%d sucessful) (runtime %ds)' %
                         (self.scan, 1, upstat['success'], upstat['total'], transtime))
        return scan, None, None, 1

    def zipdir(self, targetzip, path, fast=False):
        # Zips a scan directory in uploadable format
        scan = os.path.splitext(os.path.basename(targetzip))[0]

        try:
            if fast:
                zipf = zipfile.ZipFile(targetzip, 'w', zipfile.ZIP_STORED)
            else:
                zipf = zipfile.ZipFile(targetzip, 'w', zipfile.ZIP_DEFLATED)

            # ziph is zipfile handle
            zcount = 0
            for root, dirs, files in os.walk(path + '/'):
                for myfile in files:
                    if magic.from_file(os.path.join(root, myfile), mime=True) == 'application/dicom':
                        zipf.write(os.path.join(root, myfile))
                        zcount += 1

            zipf.close()
            return zcount
        except Exception as e:
            self.logger.error("[%s] Recompression failed for %s into %s: %s" % (scan, path, targetzip, e))
            return False

    def check_project(self):
        # Checks project existence on server
        try:
            response = self.httpsess.get(self.host + '/data/archive/projects/%s?accessible=true' % self.project)
            if response.status_code == 200:
                    self.logger.debug('Project %s found' % self.project)
                    return True
        except Exception as e:
            self.logger.error('Error checking project existence %s', str(e))

        return False

    def check_subject(self, create=False):
        # Checks subject existence on server
        if self.subject is None:
            self.logger.error('Subject is not set, required for this upload.')
            return False

        try:
            response = self.httpsess.get(self.host + '/data/projects/%s/subjects/%s?format=json' %
                                         (self.project, self.subject))
            if response.status_code == 200:
                self.logger.info('Subject %s found' % self.subject)
                return True
        except Exception as e:
            self.logger.error('Error checking subject existence %s', str(e))

        if create is True:
            # create new subject
            # curl - u $CRED - X PUT "$HOST/REST/projects/$PROJECT/subjects/$SUBJECT?event_reason=test&
            # req_format=form&gender=$GENDERTEXT&dob=02/14/$YEAR" - d xnat:subjectData / group = group$GROUP
            response = self.httpsess.put(self.host + '/data/projects/%s/subjects/%s?format=json' %
                                         (self.project, self.subject), data=self.subjectheaders)
            if response.status_code == 201:
                if self.verbose:
                    self.logger.info('Created new subject %s' % self.subject)
                return True

        return False

    def check_session(self, create=False):
        # Checks session existence for project/subject, creates with proper fields if necessary
        if self.session is None:
            self.logger.error('Session is not set, required for this upload.')
            return False

        try:
            response = self.httpsess.get(self.host + '/data/projects/%s/subjects/%s/experiments/%s?format=json' %
                                         (self.project, self.subject, self.session))
            if response.status_code == 200:
                self.logger.debug('Session %s found' % self.session)
                return True
        except Exception as e:
            self.logger.error('Error checking session existence %s', str(e))

        if create is True:
            response = self.httpsess.put(self.host +
                                         '/data/projects/%s/subjects/%s/experiments/%s'
                                         '?xsiType=%s:%sSessionData' % (
                                             self.project,
                                             self.subject,
                                             self.session,
                                             self.xmlnamespace,
                                             self.datatype
                                         ), data=self.sessionheaders)

            if response.status_code == 201:
                if self.verbose:
                    self.logger.info('Created new session %s' % self.session)
                return True

            return False

    def check_scan(self, create=False):
        if self.scan is None:
            self.logger.error('Scan is not set, required for this upload.')
            return False

        # Checks scan existence for project/subject/session, creates with proper fields if necessary
        try:
            response = self.httpsess.get(self.host + '/data/projects/%s/subjects/%s/experiments/%s/scans/%s'
                                                     '?format=json' %
                                         (self.project, self.subject, self.session, self.scan))
            if response.status_code == 200:
                self.logger.debug('Scan %s found' % self.scan)
                return True
        except Exception as e:
            self.logger.error('Error checking scan existence %s', str(e))
        if create is True:
            response = self.httpsess.put(self.host +
                                         '/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s'
                                         '?xsiType=%s:%sScanData'
                                         % (
                                             self.project,
                                             self.subject,
                                             self.session,
                                             self.scan,
                                             self.xmlnamespace,
                                             self.datatype
                                         ), data=self.scanheaders)

            if response.status_code == 200:
                if self.verbose:
                    self.logger.info('Created new scan %s' % self.scan)
                return True

            return False

    def validate_dicom_session(self, targetpath, scan):
        # Validates dicom contents of scan and gathers data for validation
        dd = dict()
        zcount = 0
        # Creates index of dicom series names from files in dir
        for f in os.listdir(targetpath):
            if magic.from_file(os.path.join(targetpath, f), mime=True) == 'application/dicom':
                td = pydicom.read_file(os.path.join(targetpath, f))
                if td.SeriesNumber not in dd:
                    dd[int(td.SeriesNumber)] = {'desc': td.SeriesDescription, 'count': 1, 'localname': scan}
                    zcount += 1
                else:
                    dd[int(td.SeriesNumber)]['count'] += 1
                    zcount += 1

        if len(dd) > 1:
            self.logger.warning('[%s] More than one series detected in scan: %s' % (scan, str(dd.keys())))

        return zcount, dd

    def get_serverscans(self):
        # Gathers server side upload for validation
        self.renew_session()
        scandata = dict()
        try:
            mypayload = {'format': 'json'}
            scans = self.httpsess.get(("%s/data/archive/projects/%s/subjects/%s/experiments/%s/scans/" %
                                       (self.host, self.project, self.subject, self.session)),
                                      params=mypayload).json()

            for thisscan in scans['ResultSet']['Result']:
                scandata[int(thisscan['ID'])] = {'desc': thisscan['series_description'], 'count': 0}
                filelist = self.httpsess.get("%s/data/archive/projects/%s/subjects/%s/experiments/%s/scans/%s/"
                                             "resources/DICOM/files" %
                                             (self.host, self.project, self.subject, self.session, thisscan['ID']),
                                             params=mypayload).json()

                scandata[int(thisscan['ID'])]['count'] += len(filelist['ResultSet']['Result'])

            return scandata
        except Exception as e:
            self.logger.error(('Error retrieving file validation data from %s: %s' % (self.host, str(e))))

        return False
