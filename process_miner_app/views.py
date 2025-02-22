# TODO remove as soon as ml implementation is ready
from time import sleep
import os
import shutil

from django.http import HttpResponse, HttpRequest, FileResponse, Http404
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode

# importing authenticate function for User authentication
# if authentication is successful, User object is returned, None otherwise
from django.contrib.auth import authenticate, login, logout

# import of ml implementation
from ml_bl.app.mock import ml_algorithm_mock, unzip

def index(request: HttpRequest) -> HttpResponse:
    '''
    Handler for the entry point
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:
    '''

    return render(request, 'process_miner_app/index.html')

# TODO imlement as soon as implementation is done, react to raised exception from lukas
def error(request: HttpRequest) -> HttpResponse:
    '''
    Handler for the error page
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:
    '''
    return HttpResponse('this is an error page')

def login_handler(request: HttpRequest) -> HttpResponse:
    '''  
    Handler for log-in requests
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:
    '''
    # extracting username from POST request via dict key
    # .get is used to make sure, no KeyError is thrown if key cannot be found, returns None if so
    username = request.POST.get('username')
    password = request.POST.get('password')

    # user authentication
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('process_miner_app:input_handler')
    else:
        # If authentication fails, return to index page
        return redirect('process_miner_app:index')


def input_handler(request: HttpRequest) -> HttpResponse:
    '''
    Handler for file uploads
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:    
    '''
    # Handle GET requests
    if request.method == 'GET':
        # Retrieve the filename from the session if it exists
        previous_output_file_name = request.session.get('output_file', None)
        if previous_output_file_name:
            # Try to delete the file
            file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', previous_output_file_name)
            delete_file(file_path)
            del request.session['output_file']

        return render(request, 'process_miner_app/file_upload.html')
    
    # Handle POST requests (form submit events)
    elif request.method == 'POST':

        # retrieve file based on name from request
        file = request.FILES['fileUpload']

        # prepare full_path, necessary to make sure, directory exists
        # hardcode upload.zip, πas only zip uplaod is possible, no need to extract file extension
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'upload.zip')
        # make sure, directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # write file to full_path in chunks
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        # if data is uploaded again (for example when reperforming calculation, file is overwritten)

        unzip()

        # TODO, implement pipeline from Lukas, try except
        output_file_name = ml_algorithm_mock()
        
        # Store the output file name in the session
        request.session['output_file'] = output_file_name

        return redirect("process_miner_app:output_handler")

def output_handler(request: HttpRequest) -> HttpResponse:
    '''
    Handler for output path
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:   
    '''

    filename = request.session.get('output_file')

    context = {
        'filename': filename
    }

    return render(request, 'process_miner_app/file_download.html', context)

def downloadHandler(request: HttpRequest, filename: str) -> FileResponse:
    '''
    Handler for file downloads
        Parameters:
            request (HttpRequest):
            filename (str): name of file to be downloaded
        Returns:
            HttpResponse:   
    '''

    file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', filename)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(open(file_path, 'rb'), as_attachment=True)

def logout_handler(request: HttpRequest) -> HttpResponse:
    '''
    Handler for logouts
        Parameters:
            request (HttpRequest):
            filename (str): name of file to be downloaded
        Returns:
            HttpResponse:   
    '''
    # Delete the existing output file if it exists
    if 'output_file' in request.session:
        output_file_path = os.path.join(settings.MEDIA_ROOT, 'downloads', request.session['output_file'])
        delete_file(output_file_path)
        del request.session['output_file']
        
    logout(request)

    return redirect('process_miner_app:index')

def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except FileNotFoundError:
        pass