# Emochat

A minimal tutorial on how to get the apps running.


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

1) Install Miniconda (or Anaconda)
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

## Installing Dependencies


The `requirements.txt` file should list all Python libraries that we need for the app, and they will be installed using:

```
pip install -r requirements.txt
```

## Run The apps

1) Create migrations

    ```
    python3 manage.py makemigrations

2) Migrate the models to the database

    ```
    python3 manage.py migrate
    ```
3) Activate the environment
    ```
    python3 manage.py runserver
    ```
4) Voila! the app should be running here
    http://127.0.0.1:8000/
    

## Manage the database using Django-admin

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
    



