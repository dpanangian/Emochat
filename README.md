# Emochat
https://emochat.azurewebsites.net/


# Installation
A minimal tutorial on how to get the app running.


## Environment

Create a new python environment.
### Linux & Mac Os users

1) Create an environment

    ```
    python3 -m venv emochat-env
    ```
2) Activate the environment
    ```
    source emochat-env/bin/activate
    ```
    Done.

### Windows users

1) Install Miniconda (less shitty than Anaconda)
https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
2) open Anaconda Prompt

3) Create a conda environment

    ```
    conda create -n emochat-env python=3.8
    ```
2) Activate the environment
    ```
    conda activate emochat-env
    ```
    Done.

## Open the project folder
1) Clone the project
 
2) cd to the directory

## Installing Dependencies

The `requirements.txt` file should list all Python libraries that we need for the app, and they will be installed using:

```
pip install -r requirements.txt
```

## Run Django app

1) Migrate the models to the database

    ```
    python3 manage.py migrate
    ```
2) Activate the environment
    ```
    python3 manage.py runserver
    ```
3) Voila! the app should be running here
    http://127.0.0.1:8000/
    

# Manage the database using Django-admin

1) Create a superuser
    ```
    python3 manage.py createsuperuser
    ```
2) Run the server
    ```
    python3 manage.py runserver
    ```
3) Open the django-admin here
    http://127.0.0.1:8000/admin/
    
# Migrating Models
Models need to be migrated after changes applied before running the server

1) Create migrations

    ```
    python3 manage.py makemigrations
    ```
2) Run the migrations
    ```
    python3 manage.py migrate
    ```
    ```
3) Run the server
    ```
    python3 manage.py runserver





