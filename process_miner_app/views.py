# TODO remove as soon as ml implementation is ready
from time import sleep

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

# Mock users, authentication should be handled more professional in productive deployment
# Import User class
# from django.contrib.auth.models import User
# Create mock user
# User.objects.create_user(username='user', email='testuser@example.com', password='user')

# importing authenticate function for User authentication
# If authentication is successful, User object is returned, None otherwise
from django.contrib.auth import authenticate, login, logout

# import of ml implementation
from ml_bl.app.mock import ml_algorithm_mock

def index(request):
    '''
    Handler for the entry point
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:
    '''
    return render(request, 'process_miner_app/index.html')

# TODO imlement if required
def error(request):
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
    # Extracting username from POST request via dict key
    # .get is used to make sure, no KeyError is thrown if key cannot be found, returns None if so
    username = request.POST.get('username')
    password = request.POST.get('password')

    # User authentication
    user = authenticate(username=username, password=password)

    # pylint: disable=no-else-return
    if user is not None:
        login(request, user)
        return redirect('process_miner_app:input_handler')

    else:
        # If authentication fails, return to index page
        return redirect('process_miner_app:index')


def input_handler(request):
    '''
    Handler for file uploads
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:    
    '''
    # Handle GET requests
    # pylint: disable=no-else-return
    if request.method == 'GET':
        return render(request, 'process_miner_app/file_upload.html')
    
    # Handle POST requests (form submit events)
    elif request.method == 'POST':
        print(request.FILES)

        sleep(3)
        return redirect('process_miner_app:output_handler')


def output_handler(request):
    '''
    Handler for file downloads
        Parameters:
            request (HttpRequest):
        Returns:
            HttpResponse:   
    '''
    return render(request, 'process_miner_app/file_download.html')

def logout_handler(request):
    logout(request)

    return redirect('process_miner_app:index')


# TODO Staticdirs sauber setzen, damit evtl. Modul von Lukas als StaticDir verwendet werden kann!
