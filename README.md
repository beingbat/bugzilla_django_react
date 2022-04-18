## This is the read me for Bugzilla Test Project

#### Project Setup Instructions:
Project is deployed at https://bugzilla-django.herokuapp.com/ but if you want to run it locally follow the instructions below:
- First clone it using link: https://github.com/at-malek/bugzilla.git
- Create a virtual environment first for running this project. Following are steps for creating virtualenv:
  -  Go to the directory where you want to create virtualenv, here I am going to create it in the project folder itself. So, first creat project folder and open it.
  - Open terminal in that directory and run command: <code>$ python3 -m venv ./venv --prompt bugzilla</code>
  - Activate the virtualenv using <code>$ source venv/bin/activate</code>
  - Then install all the requirement packages from requirements.txt <code> $ python -m pip install requirements.txt</code>
- Then to run the project, first we need to create database and make tables i.e. migrations so run the following commands for that:
  <code>$ cd bugzilla</code>
  <code>$ python manage.py makemigrations</code>
  <code>$ python manage.py migrate</code>
- Finally, to run server run command:
  <code>$ python manage.py runserver</code>
### Project Description: A management system for managing employees, projects and bugs in those projects.

User Types:
- Manager
- QAEngineer
- Developer

Bug/Feature Types:
- Bug
- Feature

Note: The word 'manage' refers to view list of objects, view specific object and delete or modify object.

Web App Workflow:
- Each user logs in and redirected to the dashboard. Each user can change their profile information from dashboard but the amount of modification is limited by the type of the user.
- At dashboard:
- - Managers have access to Add/Manage Employees [Developers, QAEngineers], Projects. Managers can also manage Bugs directly from dashboard but they will have to go to specific project to add Bug in it.
- - QAEs can view all projects, see their assigned project, view all bugs reported, report new bugs, modify the status of the bugs they reported.
- - Developers can view their assigned project, bugs in their assigned project, and bugs that have been assigned to them and modify their status.


There are two managers with usernames:

admin (superuser)
manager

Password for admin user is 'admin' without quotes and for every other employee it is iPh0ne4@

<hr/>

#### Project Design choices and architecture:
- Project has 3 models each having its seperate app [project:Project, userprofile:Profile, bug:Bug]
- Function based views have been used for add/update features in every model and Generic Class Based views are used for List, and Detail views
- ModelForms are used for every form except the UserCreation for which UserCreationForm is used

Profile:
- Profile model is for extending the built-in User model with some extra fields. To extend User, Profile model uses OneToOne key correspondence to the User model, this foreign key is also the primary key of the model, initially signals were used to linke User and Profile models but they I wanted to cascade profile on deletion.
- Profile has two other fields: designation i.e. User Type and project i.e. User assigned Project
- Manager can register/update users for which function based views have been used. It can delete Users as well. Other User Types cannot perform any of these tasks except modifiying their own profile/user information.
- When user is created a confirmation email is sent which changes the status of user to active, unless user open the link in the email, they cannot sign in.

Project:
- Project model has two fields title and description
- Only Managers can create/modify/delete projects
- Project should not have any employees in it to delete it
- Each project has its own Bugs and Features. Bug model holds the foreign key to the project for linking itself to a project.
- Each employee is also linked to a project so Profile model defines a foreign key relation with project
- A project can have more than 1 bugs/feature and more than 1 developers/qaes but a bug/feature and developer/qae can only belong to a single project.

Bug:
- Bugs have many fields and there is constrained on two of them i.e. screenshot [ImageField] and title. Title must be unique for a bug in a project and screenshot can only be of type 'png' or 'gif'.
- Managers can create/modify bugs in any project
- QAE can create bugs in any project bug only modify bugs it created itself
- Developer assigned to a project can view bugs in it and can only modify status f bugs which are assigned to it
- Developers can assign bugs to themselves from their current project if they are not already assigned to someone.
