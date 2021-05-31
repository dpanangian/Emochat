# Emochat



A minimal tutorial on how to get the app running.

## Git Branch

Don't forget to switch to dev branch


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
