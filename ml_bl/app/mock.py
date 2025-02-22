'''
Module to mock behaviour of machine learning algorithm TO BE REPLACED
'''

from django.conf import settings

from ml_bl.preprocessing.pipelines import load_tale_data_from_raw_files, preprocess_manual_preparation
import zipfile
import os
import joblib
from datetime import datetime

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
    print("Preprocessing data...")

    # get media folder path
    data_path = os.path.join(settings.MEDIA_ROOT, 'processed')
    raw_data = load_tale_data_from_raw_files(data_path)
    test_data = preprocess_manual_preparation(raw_data, train=False)
    test_X = test_data.to_numpy()

    print(len(raw_data))
    print(len(test_data))
    print("Data preprocessed")


    # load the model frin the model folder in the ml_bl folder the joblib file
    print("Loading model...")
    model_path = os.path.join(settings.BASE_DIR, 'ml_bl', 'models', 'decision_tree_classifier.joblib')
    model = joblib.load(model_path)
    print("Model loaded")

    predictions = model.predict(test_X)

    raw_data['prediction'] = predictions
    
    # save the predictions to a csv file in media folder and make sure folder exists
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'downloads'), exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S.%f')
    output_filename = f'output_{timestamp}.csv'

    raw_data.to_csv(os.path.join(settings.MEDIA_ROOT, 'downloads', output_filename), index=False)

    return output_filename


def unzip():
    zip_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'upload.zip')
    extract_to = os.path.join(settings.MEDIA_ROOT, 'processed') 

    # Make sure the extraction folder exists
    os.makedirs(extract_to, exist_ok=True)

    # Open and extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print(f'Files extracted to: {extract_to}')
