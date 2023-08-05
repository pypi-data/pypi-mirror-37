# Pacifica Archive Interface
[![Build Status](https://travis-ci.org/pacifica/pacifica-archiveinterface.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-archiveinterface)
[![Build status](https://ci.appveyor.com/api/projects/status/kxfjj5exb09foqlv?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-archiveinterface)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-archiveinterface/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-archiveinterface)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-archiveinterface/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-archiveinterface/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-archiveinterface/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-archiveinterface)
[![Docker Stars](https://img.shields.io/docker/stars/pacifica/archiveinterface.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/archiveinterface/general)
[![Docker Pulls](https://img.shields.io/docker/pulls/pacifica/archiveinterface.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/archiveinterface/general)
[![Docker Automated build](https://img.shields.io/docker/automated/pacifica/archiveinterface.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/archiveinterface/builds)


This code is to provide the archive interface for the rest of the
Pacifica code base. This code consists of some very specific algorithms
and APIs to support data that might exist on tape or spinning disk.

# Building and Installing

This code depends on the following libraries and python modules:

HPSS Client 7.4.1p2
Python JSON
Python CTypes
Python DocTest

This is a standard python distutils build process.

```
python ./setup.py build
python ./setup.py install
```

# Running It

There are three ways of running the archive interface; POSIX, ORACLE_HSM_SIDEBAND and HPSS.

Posix File System Backend
```
python ./scripts/archiveinterfaceserver.py -t posix -p 8080 -a 127.0.0.1 --prefix /path
```
HPSS Archive Backend
```
python ./archiveinterfaceserver.py -t hpss  -p 8080 -a 127.0.0.1 --prefix /path
```

ORACLE_HSM_SIDEBAND
```
python ./archiveinterfaceserver.py -t hsmsideband  -p 8080 -a 127.0.0.1 --prefix /path
```

# Config file
You can also pass a config file via the --config option.  This is the first option and has highest priority.
Second highest priority is the environment variable ARCHIVEI_CONFIG. This will be looked at if the --config
option was not used.
The final option is the application will default to config.cfg if neither of the first two options occured.

# Config File Example:
Note here that the different backends use different config options.  These are required for their respected
archive types.
```
[posix]
use_id2filename = false

[hpss]
user = hpss.unix
auth = /var/hpss/etc/hpss.unix.keytab

[hsm_sideband]
sam_qfs_prefix = /tmp/path
schema = schema_name
host = host
user = user
password = pass
port = 3306
```

# ID Mapping to File Names

The Pacifica software depends on a flat ID space for indexing files. This needs
to map to filenames on the backend storage in a nice way. To limit the number of
files in a single directory (or number of directories in a directory) we use the
algorithm in `archiveinterface.id2filename`. This takes a number and breaks it
into bytes. Each byte is then represented in hex and used to build the directory
tree.

For example `id2filename(12345)` becomes `/39/3039` on the backend file system.

# API Examples

## Verify working

To verify the system is working do a GET against the system with no id specified.
```
curl -X GET http://127.0.0.1:8080
```

Sample output:
```
{
    "message": "Pacifica Archive Interface Up and Running"
}
```

## Put a File

The path in the URL should be only an integer specifying a unique
file in the archive. Sending a different file to the same URL will
over-write the contents of the previous file. Setting the Last-
Modified header sets the mtime of the file in the archive and is
required.

```
curl -X PUT -H 'Last-Modified: Sun, 06 Nov 1994 08:49:37 GMT' --upload-file /tmp/foo.txt http://127.0.0.1:8080/12345
```

Sample output:
```
{
    "message": "File added to archive",
    "total_bytes": "24"
}
```

## Get a File
The HTTP `GET` method is used to get the contents
of the specified file.
```
curl -o /tmp/foo.txt http://127.0.0.1:8080/12345
```
Sample output (without -o option):
"Document Contents"

## Status a File

The HTTP ```HEAD``` method is used to get a JSON document describing the
status of the file. The status includes, but is not limited to, the
size, mtime, ctime, whether its on disk or tape. The values can be found
within the headers.
```
curl -I -X HEAD http://127.0.0.1:8080/12345
```
Sample output:
```
HTTP/1.0 204 No Content
Date: Fri, 07 Oct 2016 19:51:37 GMT
Server: WSGIServer/0.1 Python/2.7.5
X-Pacifica-Messsage: File was found
X-Pacifica-File: /tmp/12345
Content-Length: 18
Last-Modified: 1473806059.29
X-Pacifica-Ctime: 1473806059.29
X-Pacifica-Bytes-Per-Level: (18L,)
X-Pacifica-File-Storage-Media: disk
Content-Type: application/json

```

## Stage a File
The HTTP `POST` method is used to stage a file for use.  In posix this
equates to a no-op on hpss it stages the file to the disk drive.

```
curl -X POST http://127.0.0.1:8080/12345
```

Sample Output:
```
{
    "file": "/12345",
    "message": "File was staged"
}
```

## Move a File
The HTTP `PATCH` method is used to move a file.
The upload file contains the path to current file on archive
The Id at the end of the url is where the file will be moved to

```
curl -X PATCH --upload-file /tmp/foo.json http://127.0.0.1:8080/2

```

Sample Output:
```
{
    "message": "File Moved Successfully"
}
```
Sample Upload File
```
{
  "path": "/path/to/file/file.1"
}
```

# Extending Supported Backends

## Create a backend directory

Under pacifica-archiveinterface->archiveinterface->archivebackends add a
directory for the new backend type

## Create Classes that Implement the Abstract Backend Class methods

Abstract backend classses can ge found under:
pacifica-archiveinterface->archiveinterface->archivebackends->abstract
Descriptions of all the methods that need to be abstracted exists in the
comments above the class.

## Update Backend Factory

Update the archive backend factory found here:
pacifica-archiveinterface->archiveinterface->archivebackends->archive_backend_factory.py
In this file is a load_backend_archive method.  This method needs to have
its logic extended to support the new backend type.  This also entails loading the appropriate files for this backend using import

## Update Interface Server

Update the archiveinterfaceserver.py file to support the new backend choice.
File located: pacifica-archiveinterface->scripts->archiveinterfaceserver.py
In this file the type argument is defined with its supported types.  Need to
extend that array to include the new backend type

# Post Deployment Testing

Inside the post_deployment_test directory there is a file called deployment_test.py
This file will run a series of tests against a deployed archive interface.  The test are ordered so that they post, stage, status, and get files properly.
There are a few global variables at the top of the file that need to be adjusted to each deployment.

## Variables to set in deployment_test.py
```
export ARCHIVE_URL='http://127.0.0.1:8080/'
```
 - ARCHIVE_URL is the URL to the newly deployed archive_interface

## Running deployment_test.py
```
pytest -v post_deployment_tests/deployment_test.py
```
Output will be the status of the tests against the archive interface
