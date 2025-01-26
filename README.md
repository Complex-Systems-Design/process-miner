## 1) Getting Started
All commands outlined in this chapter must be run from the root directory of this project, otherwise adapt them accordingly.

### 1.1) Prerequisites
Ensure that the following requirements are met:
- Installed [Python v3.13](https://www.python.org/downloads/release/python-3130)
- (Optional, but highly recommended) A Python virtual environment (venv). To do so, proceed as follows:
    1. Create the Python virtual environment named venv:
        ```bash
        python3.13 -m venv venv
        ```
    2. Activate the virtual environment and make sure it has been activated correctly :
        ```bash
        source venv/bin/activate
        which python3.13 && which pip3.13
        # Ensure, the following ouput is returned to check for correct activation:
        # ./venv/bin/python3.13
        # ./venv/bin/pip3.13
        ```
- Required Python dependencies:
    1. Install the required dependencies:
        ```bash
        python3.13 -m pip install -r requirements.txt
        ```

### 1.2) Prepare and run Django
1. Apply the Django migrations (create database schema):
    ```bash
    python3.13 manage.py migrate
    ```
2. Create a test user, necessary for authentication:
    ```bash
    python3.13 manage.py shell

    from django.contrib.auth.models import User

    User.objects.create_user(username='user', email='testuser@example.com', password='user')
    ```
    If successful, leave the Django management shell (ctrl + d).
3. Start the webserver:
    ```bash
    python3.13 manage.py runserver
    ```
    If successful, access the app under http://localhost:8000/app/