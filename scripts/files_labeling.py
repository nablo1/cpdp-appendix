from pydriller import Git
from pydriller import Repository
import ntpath
import re
import mysql.connector
import os

host = "ENTER HERE"
user = "ENTER HERE"
password = "ENTER HERE"
project = "ENTER HERE" # The project must be in the same dir as this script

gr = Git(project)

### Retreiving all java files in the project in storing them in a list

files_w_duplicates = []
for subdir, dirs, files in os.walk(project):
	for file in files:
		if file.endswith(".java"):
			files_w_duplicates.append(file)

all_files = []
for f in files_w_duplicates:
	if f not in all_files:
		all_files.append(f)

print(len(files_w_duplicates), len(all_files))
db_conn = mysql.connector.connect(host = host, user = user, passwd = password)
mycursor = db_conn.cursor()

### Creating DB for the project
try:
	mycursor.execute("CREATE DATABASE " + project)
except:
	print("DB with this name already exists.. skipped.")

### Getting all commits from the project using PyDriller Magic

mycursor.execute("CREATE TABLE " + project + ".all_commits (commit_hash longtext, bug_fixing varchar(255))")
sql_store_commits = "INSERT INTO " + project + ".all_commits (commit_hash, bug_fixing) VALUES (%s, %s)"

def findWholeWord(word):
	return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search

for commit in Repository(project).traverse_commits():
	ms = str(commit.msg).lower()

	if findWholeWord("fix")(ms) or findWholeWord("fixed")(ms) or findWholeWord("fixes")(ms) or findWholeWord("fixing")(ms) or findWholeWord("bugfix")(ms) or findWholeWord("bug")(ms) or findWholeWord("bugs")(ms) or findWholeWord("error")(ms) or findWholeWord("errors")(ms):
		bug_fixing = "true"
	else:
		bug_fixing = "false"

	for file in commit.modified_files:
		filename = file.filename
		
	commit_data = (commit.hash, bug_fixing)
	mycursor.execute(sql_store_commits, commit_data)
	db_conn.commit()

print("All commits in project " + project + " retrieved and stored in the DB sucessfully")

### Getting buggy commits + bug-prone files with the help of the SZZ algorithm and storing them in DB

mycursor.execute("CREATE TABLE " + project + ".szz (bug_fixing longtext, filename longtext, filepath longtext, bug_introducing longtext)")

sql_retrieve_fixing_commits =  "SELECT distinct commit_hash FROM " + project + ".all_commits WHERE bug_fixing = 'true'"
sql_store_szz_hits = "INSERT INTO " + project + ".szz (bug_fixing, filename, filepath, bug_introducing) VALUES (%s, %s, %s, %s)"

mycursor.execute(sql_retrieve_fixing_commits)
results = mycursor.fetchall()
for row in results:
	try:
		buggy_commits = gr.get_commits_last_modified_lines(gr.get_commit(row[0]))
		if len(buggy_commits) == 0:
			continue
		else:
			items = buggy_commits.items()
			for item in items:
				file = item[0]
				filename = ntpath.basename(file)
				data = (row[0]), filename, file, str(item[1])
				mycursor.execute(sql_store_szz_hits, data)
				db_conn.commit()
	except Exception as e:
		print(e)
		continue

print("All bug-prone files in project " + project + " retrieved and stored in the DB sucessfully")

### Reading bug-prone files from DB without duplaictes

prone_files = []
sql_retrieve_bugprone_files = "SELECT * FROM " + project + ".bugprone_files WHERE filename LIKE '%.java%' GROUP BY filename"
mycursor.execute(sql_retrieve_bugprone_files)
res = mycursor.fetchall()
for row in res:
	prone_file = row[1].replace("'", '')
	prone_files.append(prone_file)

### Storing all files with bug-prone labels in the DB

mycursor.execute("CREATE TABLE " + project + ".all_files (file longtext, bug_prone varchar(255))")
sql_store_files = "INSERT INTO " + project + ".all_files (file, bug_prone) VALUES (%s, %s)"

existing_prone_files = []
for file in all_files:
	for p in prone_files:
		if p == file:
			existing_prone_files.append(file)
		else:
			continue

for file in all_files:
	if file in existing_prone_files:
		prone_data = (file, "true")
		mycursor.execute(sql_store_files, prone_data)
		db_conn.commit()
	else:
		free_data = (file, "false")
		mycursor.execute(sql_store_files, free_data)
		db_conn.commit()

	