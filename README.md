# Group 2 CS 458
Software Engineering Practicum

## Steps for setting up your project:

step 0:

	- make sure you have pip, virtualenv, and pipenv installed.
	- go to the folder you want the repository in through your terminal
	
inside your terminal:

1. clone the repository in that folder: type "git clone https://github.com/larissaford/Group2cs458.git"

2. go into the folder through the terminal: type "cd Group2cs458"

3. type "python3 -m venv local_python_environment" or "python -m venv local_python_environment" depending on how python is set up on your computer

4. to activate your virtual environement, 

	- type "source local_python_environment/bin/activate" for linux

	- or "source local_python_environment/Scripts/activate" for windows
	
5. to get the project dependencies, type: "pip install -r requirements.txt" inside the virtual environment
(this downloads Django for the user)

5. go into the src file: "cd src"

6. go into the carpideas folder (the source folder of our project)

7. to run our server, type: "python manage.py runserver"
	
	- this can take a minute
	- to quit the server on windows, type CTRL-C
