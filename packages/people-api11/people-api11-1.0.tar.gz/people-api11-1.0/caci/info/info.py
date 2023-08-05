import zipfile
import json
import os
import pymongo
FILE = os.path.dirname(os.path.realpath(__file__))

def load():
    # Unzip the file
    zip_file = zipfile.ZipFile(FILE + '/fake_profiles.json.zip', 'r')
    zip_file.extractall(FILE)
    zip_file.close()
    # Load the Json format
    file_json = json.loads(open(FILE + '/fake_profiles.json').read())
    return file_json
