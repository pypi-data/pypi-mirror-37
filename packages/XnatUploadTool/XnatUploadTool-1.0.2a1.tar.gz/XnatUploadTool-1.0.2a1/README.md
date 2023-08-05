
#Xnat upload tool
Takes a single directory and uploads to xnat imaging informatics software platform.

##Summary
* Designed to upload a single session to a single subject within a project
* Can be used as a python module, or as a stand alone script
* Via the jobs argument, can be parallelized for maximum performance
* Handles login session rotation based on the 'sessiontimeout' setting, which should match your xnat server settings
* Recompresses data into zip file format to use high performance zip upload importer, can by bypassed by setting 'raw' mode.
* Performs validation on request, comparing dcm data and scan file counts in sessions to remote server post upload.
* Handles single file uploads of non-dicom data with custom headers

##Installation
Part of the PyPy repo, can be installed via either:

    pip install xnatuploadtool

or you prefer disutils:

    easy_install xnatuploadtool

Can also be installed directly by cloning this repo and running:

    python ./setup.py install

The executable script will be installed as 'xnat-uploader' in your system path. 

##Execution

Basic execution:

    xnat-uploader --host localhost:8080 --username myusername --password mypassword --project project1 
      --subject subject01 --session subject01_01 ./upload-data

Arguments can either be passed in via the cli, or via config file (~/.xnatupload.cnf, or xnatupload.cnf in the
current working directory.) Arguments in the config file should match key/value pairs as in the cli. Example:

    host = http://localhost:8080
    username = myusername
    password = mypassword
    project = project1
    subject = subject1
    jobs = 4
    tmpdir = /tmp

CLI example:

    usage: xnat-uploader [-h] [-c CONFIG] [--username USERNAME]
                         [--password PASSWORD] [--logfile LOGFILE]
                         [--tmpdir TMPDIR] [-V] [-r] [-v] [-t TIMEOUT]
                         [-s SESSIONTIMEOUT] [-j JOBS] [-d DATATYPE]
                         [--resource RESOURCE] --host HOST --project PROJECT
                         --subject SUBJECT [--subjectheaders SUBJECTHEADERS]
                         [--bsubjectheaders BSUBJECTHEADERS] [--session SESSION]
                         [--sessionheaders SESSIONHEADERS]
                         [--bsessionheaders BSESSIONHEADERS] [--scan SCAN]
                         [--scanheaders SCANHEADERS] [--bscanheaders BSCANHEADERS]
                         target
    
Xnat upload script, takes a single directory and uploads to site. Target
directory is a session, with any number of scans within it. Directories within
are treated as scans, populated with either many separate dicom files or a
single compressed flat archive of dicom files. Zip files found in the top
level are treated as a scan and are expected to have a compressed archive of
dcm files. The session name is assumed as the same as the zip file name,
without the zip extension. If a single file is specifed rather than a
directory, it is assumed to be non-dicom. This functionality requires the
specification of other datatypes. This method is single threaded. Args that
start with '--' (eg. --username) can also be set in a config file
(~/.xnatupload.cnf or ./xnatupload.cnf or /etc/xnatupload.cnf or specified via
-c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for
details, see syntax at https://goo.gl/R74nmi). If an arg is specified in more
than one place, then commandline values override config file values which
override defaults.

positional arguments:
  target                Target upload. Can be a directory with subdirectories
                        of dicom files, or a single non-dicom file

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  --username USERNAME   Username, if not set will pull from XNATCREDS env
                        variable as USERNAME:PASSWORD
  --password PASSWORD   Password, if not set will pull from XNATCREDS env
                        variable as USERNAME:PASSWORD
  --logfile LOGFILE     File to log upload events to, if not set use stdout
  --tmpdir TMPDIR       Directory to untar/compress files to
  -V, --validate        Validate scan descriptions and filecounts after upload
  -r, --raw             Disable recompression as zip file uploading each scan
                        file individually. Severely impacts performance, but
                        can solve problems with extremely large sessions
  -v, --verbose         Produce verbose logging
  -t TIMEOUT, --timeout TIMEOUT
                        Read timeout in seconds, set to higher values if
                        uploads are failing due to timeout
  -s SESSIONTIMEOUT, --sessiontimeout SESSIONTIMEOUT
                        Session timeout for xnat site in minutes, to determine
                        session refresh frequency
  -j JOBS, --jobs JOBS  Run in X parallel processes to take advantage of
                        multiple cores
  -d DATATYPE, --datatype DATATYPE
                        Data type to upload
  --resource RESOURCE   Resource name for non-dicom files
  --host HOST           URL of xnat host
  --project PROJECT     Project to upload to
  --subject SUBJECT     Subject to upload to, can be string or in dicom tag
                        format (0000,0000). If tag in parenthesis is used,
                        will be pulled from first dicom file found.
  --subjectheaders SUBJECTHEADERS
                        Subject headers in json format
  --bsubjectheaders BSUBJECTHEADERS
                        Subject headers in base64 json format
  --session SESSION     Session name to use for upload, can be string or in
                        dicom tag format (0000,0000). If tag in parenthesis is
                        used, will be pulled from first dicom file found.
  --sessionheaders SESSIONHEADERS
                        Session headers in json format
  --bsessionheaders BSESSIONHEADERS
                        Session headers in base64 json format
  --scan SCAN           Scan to upload files to, can be string or in dicom tag
                        format (0000,0000)
  --scanheaders SCANHEADERS
                        Scan headers in json format
  --bscanheaders BSCANHEADERS
                        Scan headers in base64 json format