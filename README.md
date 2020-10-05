# Group 2 CS 458
Software Engineering Practicum

steps for setting up your project:
step 0:
	- make sure you have pip, virtualenv, and pipenv installed.
	- go to the folder you want the repository in through your terminal


1. clone the repository in that folder: type "git clone https://github.com/larissaford/Group2cs458.git"

2. go into the folder through the terminal: type "cd Group2cs458"

3. create a virtual environment: 
	many ways to do this, here's just one:
	-type "virtualenv ." or "virtual -p python3 ." depending on how python is set up on your computer

4. activate your virtual environment: 
	different ways to do this as well:
	- on linux: "source bin/activate"
	- on Windows: "source Scripts/activate" or "env/Scripts/activate"
	 
5. go into the src file: "cd src"

6. download the most recent version of django: "pip install django==3.1.2"

7. go into the carpideas folder (the source folder of our project)

8. to run our server, type: "python manage.py runserver"
	-this can take a minute
	-to quit the server on windows, type CTRL-C
