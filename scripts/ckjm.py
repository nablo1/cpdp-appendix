### gathering files 
import os
import ntpath
from os.path import isfile, join
from decimal import Decimal

### csv
import csv

###shell commands
import subprocess

### mysql database stuff
import mysql.connector
HOST = "ENTER_HERE"
USERNAME = "ENTER_HERE"
PASSWORD = "ENTER_HERE"
DATABASE = "ENTER_HERE"
TABLE = "ENTER_HERE"

### Connect to database
db = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWORD, database=DATABASE)
cursor = db.cursor()

### For creating database and tables
#cursor.execute("CREATE DATABASE " + database)
try:
    cursor.execute("CREATE TABLE " + TABLE + " (javafile VARCHAR(255), classfile VARCHAR(255), WMC SMALLINT(255), CBO SMALLINT(255), RFC SMALLINT(255), LCOM BIGINT UNSIGNED, Ca SMALLINT(255), Ce SMALLINT(255), NPM SMALLINT(255), LCOM3 DECIMAL(30,15), LCO SMALLINT(255), DAM DECIMAL(30,15), MOA SMALLINT(255), MFA DECIMAL(30,15), CAM DECIMAL(30,15), IC SMALLINT(255), CBM SMALLINT(255), AMC DECIMAL(30,15))")
except:
    print("Table already exists")

### Path for CKJM tool
ckjm_tool_path = 'ENTER_HERE'

### Folder of classes for project
rootdir = r'ENTER_HERE'
project = 'ENTER_HERE'

### File lists
class_files = []
dir_files = []
java_files = []
class_files_dupes = []

### Retreiving file names in folder
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.class'):

            if file not in class_files:
                ### Adding class files to list
                class_files.append(file)
                dir_files.append(subdir)

                ### Getting the name for javafiles
                temp = file.split('$')
                temp[0] = temp[0].replace('.class', '')
                temp[0] = temp[0] + '.java'
                java_files.append(temp[0])

### For troubleshooting
print(len(class_files))

### Variable lists for data
output = []
data = []
dataPoints = [] 

### Used for inserting Java filenames to table at the right index.
failed_ckjm = []
fail_iterator = 0

### Iterators for java filename and class directory path
javaFileIterator = 0
directoryIterator = 0


### Try to get CKJM metrics - some have byte tag errors which crashes
for file in class_files:
    try:
        ret = subprocess.check_output('java -jar ' + ckjm_tool_path + ' ' + dir_files[directoryIterator] + "/" + file)
        output.append(ret)

    ### To prevent crashing, print error and count failed attempt
    except:
        print(file + (" - error occured invalid byte tag."))
        failed_ckjm.append(fail_iterator)
    fail_iterator = fail_iterator + 1

    x = x + 1

### Append result to text file for later use if needed
with open('result_'+ project +'.txt', 'w') as f:
    for item in output:
        f.write("%s\n" % item)


### Percentage of failed files
print("--- Printing '%' of failed classes ---")
print(len(failed_ckjm))
print(len(class_files))
print(len(failed_ckjm)/len(class_files))

### Iterate output of CKJM module to insert into table
for result in output:
    data = result.split()

    while (javaFileIterator in failed_ckjm):
        javaFileIterator = javaFileIterator + 1

    ### Sometime the CKJM does not retrieve metrics
    ### Adding this Try-Except removes error while trying to insert data to table
    try:
        for x in range(19):
            if x == 0:
                dataPoints.append(data[x].decode('utf-8'))
            elif x != 2 and x != 3:
                temp = data[x].decode('utf-8')
                temp = temp.replace(',', '.')
                temp = Decimal(temp)
                dataPoints.append(temp)

        query = "INSERT INTO " + TABLE + " (javafile, classfile, WMC, CBO, RFC, LCOM, Ca, Ce, NPM, LCOM3, LCO, DAM, MOA, MFA, CAM, IC, CBM, AMC) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (java_files[javaFileIterator], dataPoints[0], dataPoints[1], dataPoints[2], dataPoints[3], dataPoints[4], dataPoints[5], dataPoints[6], dataPoints[7], dataPoints[8], dataPoints[9], dataPoints[10], dataPoints[11], dataPoints[12], dataPoints[13], dataPoints[14], dataPoints[15], dataPoints[16])
        cursor.execute(query, values)
        db.commit()

    ### If data list is empty, except and continue
    except:
        continue

    ### Clear dataPoints list to make ready for next metrics
    dataPoints = []

    javaFileIterator = javaFileIterator + 1