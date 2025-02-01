'''
Module to mock behaviour of machine learning algorithm TO BE REPLACED
'''

from django.conf import settings

import zipfile
import os

# use to get MEDIA_ROOT
# os.path.join(settings.MEDIA_ROOT)

# store the to be downloaded zip file in MEDIA_ROOT/downloads
# important: in views.py this is defined in downloadHandler and in file_download.html template in 
# <a href="{% url 'process_miner_app:download_handler' 'output.zip' %}" 


def ml_algorithm_mock() -> str:
    '''
    Function to mock the behaviour of the machine learning algorithm
    parameters:
        None
    returns
        value (str): Sample string
    '''
    value = 'Hello World!'

    return value


def unzip():
    zip_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'upload.zip')
    extract_to = os.path.join(settings.MEDIA_ROOT, 'processed') 

    # Make sure the extraction folder exists
    os.makedirs(extract_to, exist_ok=True)

    # Open and extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f'Files extracted to: {extract_to}')
