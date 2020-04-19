To set up the environment for running the project on a windows 10 installation:

1) I used visual studio code as my IDE: https://code.visualstudio.com/

2) Install python 3.7.7: https://www.python.org/downloads/

3) a) Install MySQL (64-bit version): https://dev.mysql.com/downloads/mysql/
   b) I found it useful to install the mysql workbench and mysql notifier to be able to view/query the database
      separate from the project and to start the database

4) Install pip for python: https://pip.pypa.io/en/stable/installing/

5) Install Django. Then use pip to attach it to the project: https://www.djangoproject.com/download/

6) Install MySQLclient using pip. The command is: "pip install mysqlclient"

7) Using MySQL Workbench, import the dump file
a) Select "Data Import/Restore" > Select "Import from Self-Contained File" > Find the dump file in the file explorer >
   Find the "Start Import" button at the bottom right and click it

8) Run MySQL Notifier >
   Find the icon in the hidden icons (located in a popup menu in the bottom right of the windows task bar by clicking the up arrow)>
   Right click > Mouse over the database > Click on "Start"

9) I used the following visual studio code extensions (they are not necessary but may help with python or sql related issues):
	a) Python
	b) SQLite
	c) SQLTools

10) To run the project, in "Explorer" find the "manage.py" file and select it >
   Go to "Run" and click "Run and Debug" >
   For Debug Configuration, select "Django" >
   The path should be "${workspaceFolder}\cs4330\manage.py"