To set up the environment for running the project on a windows 10 installation:

1) I used visual studio code as my IDE: https://code.visualstudio.com/

2) Install python 3.7.7: https://www.python.org/downloads/

3) a) Install MySQL (64-bit version): https://dev.mysql.com/downloads/mysql/
   b) I found it useful to install the mysql workbench and mysql notifier to be able to view/query the database
      separate from the project and to start the database
   c) When you set up your local database, be sure to write down the username, password, and name of the database for later use

4) Install pip for python: https://pip.pypa.io/en/stable/installing/



FOR THE FOLLOWING STEPS:
	It *may* help to create a virtual environment in which all of these libraries can be installed. This will localize the installations
	to the project rather than across the whole system. However, this process can be difficult to figure out. The documentation I used
	can be found here: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
	I used venv (rather than virtualenv) which comes natively with Python 3.7.7
	To create the environment, enter "py -m venv env" into the terminal in Visual Studio Code after you have opened the project -
			(C:\Users\...\Documents\GitHub\cs4330project> should be the opened directory (inside the cs4330project folder))
	This command, if executed properly, will create a folder named "env" inside of the cs4330project folder
	Once created, ensure that the environment "env" is activated (look for "(env)" in green text in the terminal)
	If it is not activated, run the command ".\env\Scripts\activate" (there should be a .bat file in the env folder)



5) Install Django. Then use pip to attach it to the project: https://www.djangoproject.com/download/

6) Install MySQLclient using pip. The command is: "pip install mysqlclient"

7) Using MySQL Workbench, import the dump file
a) Select "Data Import/Restore" > Select "Import from Self-Contained File" > Find the dump file in the file explorer >
   Find the "Start Import" button at the bottom right and click it

8) Run MySQL Notifier >
   Find the icon in the hidden icons (located in a popup menu in the bottom right of the windows task bar by clicking the up arrow)>
   Right click > Mouse over the database > Click on "Start"

9) I used the following visual studio code extensions:
	a) Python
	b) SQLite (not required)
	c) SQLTools (not required)

10) a) On line 11 of "views.py" you will need to use the username, password, and name of the database from step 3c
    b) Starting at line 77 in "settings.py" you will find an array named "DATABASES". You will need to configure the "'NAME'", "'USER'", and "'PASSWORD'" fields
       using the login information from step 3c ('NAME' is the name of the database and 'USER' is the username)

11) To run the project, in "Explorer" find the "manage.py" file and select it >
   Go to "Run" and click "Run and Debug" >
   For Debug Configuration, select "Django" >
   The path should be "${workspaceFolder}\cs4330\manage.py"

12) Go to "localhost:8000" in a web browser to login as a user
    Go to "localhost:8000/admin_login" to login as an admin and view statistics


ADDITIONAL INFO:

Admin login: admin/admin
Employee user login: cfont@email.com/password
Non-employee user login: hrob@email.com/password