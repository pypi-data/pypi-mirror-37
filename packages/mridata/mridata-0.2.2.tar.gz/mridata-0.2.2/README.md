mridata-python
==============
This is a python command line interface for downloading and uploading datasets to mridata.org.

Requirements
============
This package requires requests, tqdm, and boto3. You can install using pip:

	pip install requests boto3 tqdm

Installation
============

The package can be installed via pip:

	pip install mridata

To install from source, go to the directory containing setup.py, then run

	python setup.py install

Usage
=====

Help message can be viewed through:

	mridata -h
	mridata [command] -h


Download
--------
To download from mridata.org with a UUID, you can do:

	mridata download $UUID
	
To batch download from a UUID text file (`uuids.txt`), in which each line is a UUID, you can do:

	mridata batch_download $UUIDS_TEXT_FILE

Upload
------
To upload ISMRMRD, you can do:

	mridata upload_ge --username $USERNAME --password $PASSWORD --project_name $PROJECT_NAME --anatomy $ANATOMY --fullysampled True $ismrmrd_file
