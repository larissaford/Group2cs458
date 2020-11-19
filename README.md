# Group 2 CS 458
Software Engineering Practicum

## Steps for setting up your project:

step 0:

	- Make sure you have python, pip, virtualenv, and pipenv installed. Python 3.9 currently doesn't work, and python 3.8 needs to be the 64 bit version
	- Go to the folder you want the repository in through your terminal.
	
Inside your terminal:

1. Clone the repository in that folder: type "git clone https://github.com/larissaford/Group2cs458.git"

2. Go into the folder through the terminal: type "cd Group2cs458"

3. Type "python3 -m venv local_python_environment" or "python -m venv local_python_environment" depending on how python is set up on your computer

4. To activate your virtual environement, 

	- Type "source local_python_environment/bin/activate" for linux

	- Or "source local_python_environment/Scripts/activate" for windows
	
5. To get the project dependencies, type: "pip install -r requirements.txt" inside the virtual environment
(this downloads Django for the user)

6. Go into the src file: "cd src/carpideas"(our source file)

7. Set up the email account, which will send account activation emails.
	-Create a .env file
	-Type "export EMAIL_USERNAME=youremailhere@domain.com" (without quotes)
	-Type "export EMAIL_PASSWORD=theEmailsPasswordHere" (without quotes)

6. To run our server, type: "python manage.py runserver"
	
	- This can take a minute
	- To quit the server on windows, type CTRL-C
