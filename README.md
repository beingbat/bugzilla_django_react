## THIS IS THE EXTENSION OF BUGZILLA DJANGO PROJECT TO HOOK REST API ENDPOINTS WITH REACT FRONTEND

#### Project Setup Instructions:

Project is deployed at https://bugzilla-django.herokuapp.com/ but if you want to run it locally follow the instructions below:

- First clone it using link: https://github.com/at-malek/bugzilla.git
- Create a virtual environment first for running this project. Following are steps for creating virtualenv:

  - Go to the directory where you want to create virtualenv, here it is created in project folder itself. So, first creat project folder and open it.
  - Open terminal in that directory and run command:
    <code>$ python3 -m venv ./venv --prompt bugzilla</code>
  - Activate the virtualenv using
    <code>$ source venv/bin/activate</code>
  - Then install all the requirement packages from requirements.txt
    <code> $ python -m pip install requirements.txt</code>

- Then to run the project, first we need to create database and tables i.e. migrations so run the following commands for that:
  <code>$ cd bugzilla</code>
  <code>$ python manage.py makemigrations</code>
  <code>$ python manage.py migrate</code>
- Finally, to run server run command:
  <code>$ python manage.py runserver</code>
