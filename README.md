# Online appendix for manuscript "What makes a good project for Cross-Project Software Defect Prediction?"
This is the online appendix for manuscript "What makes a good project for Cross-Project Software Defect Prediction? *The role of size, domain, and diversity*". A Bachelor thesis study in Software Engineering and Management, submitted in June 2022, and created by:
* Mohammad Nablo | University of Gothenburg 
* Jakob Roseke | University of Gothenburg 

# Table of contents
* [1. Overview](https://github.com/nablo1/cpdp-appendix#overview)
* [2. Repository content](https://github.com/nablo1/cpdp-appendix#repository-content)
* [3. Introduction and requirements](https://github.com/nablo1/cpdp-appendix#introduction-and-requirements)
* [4. Data collection](https://github.com/nablo1/cpdp-appendix#data-collection)
  * [4.1 Labeling files](https://github.com/nablo1/cpdp-appendix#labeling-files)
  * [4.2 Calculation of metrics](https://github.com/nablo1/cpdp-appendix#calculation-of-metrics)
* [5. Data analysis](https://github.com/nablo1/cpdp-appendix#data-analysis)
  * [5.1 Classifiers and predictions](https://github.com/nablo1/cpdp-appendix#classifiers-and-predictions)
  * [5.2 Statistical analysis](https://github.com/nablo1/cpdp-appendix#statistical-analysis)

# Overview
The manuscript extends prior research on software defect prediction. In particular, cross-project defect prediction. We conducted an experiment where we investigated the impact of the size and domain of a project, as well as the diversity of a selection of projects on the prediction results. We constructed a dataset based on 40 open-source GitHub Java projects, ran various predictions using 6 different ML classifiers, and performed statistical significance tests on the produced results to achieve our objectives. 

# Repository Structure
The repository is structured as follows:
* **data** directory: contains datatables that represent projects and combinations of projects to be used for training and testing.
* **results** directory: contains the results of the predictions for each used classifier.
* **scripts** directory: contains the automated scripts used for data collection and analysis.

# Introduction and Requirements
The scripts in this repository can be used to reproduce the steps of the experiment; creating raw data, running predictions with different classifiers, and performing statistical analysis. The experiment steps were carried out on a Windows 10 system. The required tools for reproducing the steps are:
* Git 2.36.1 - [Download](https://git-scm.com/download/win)
* Python 3.x - [Download](https://www.python.org/downloads/)
* PyDriller 1.15.2 by Davide Spadini et al. - [Download](https://github.com/ishepard/pydriller)
* Jupyter notebook 6.4.11 - Install via pip: `pip install notebook`
* CKJM extended 2.x - [Download](https://gromit.iiar.pwr.wroc.pl/p_inf/ckjm/down.html)
* MySQL Community 8.x, full installation - [Download](https://dev.mysql.com/downloads/)
* MySQL Connector for Python 8.x - Install via pip: `pip install mysql-connector-python`

Please make sure that all required Python libraries are installed before running the scripts.

# Data Collection
## Labeling Files
The first step in the data collection is to label Java files in a project as *defect-prone* or *defect-free*. The labeling procedure is carried out using `files_labeling.py` script.
Before executing the script, the target Java project must be freshly cloned in the same directory as the script, and upon that, lines 8 to 11 in the script, marked with `ENTER HERE`, must be filled with the proper configuration settings:
* `host`: server name or IP address on which your MySQL-server is running i.e. *localhost*
* `user`: username of MySQL-server i.e. *root*
* `password`: password of MySQL-server
* `project`: name of cloned project as is

The script results in 3 tables: `all_commits`, `szz`, and `all_files`. The first two can be inspected for testing purposes or discarded. `all_files` table is the main take from the script as it includes all Java files with their labels.

## Calculation of Metrics
Metrics calculation is carried out using the script `ckjm.py`. The script loops through all Java classes in the target project, and executes a shell command using CKJM, and stores the extracted metrics in a new MySQL table.
Before executing the script, the target project must be successfully built using Maven, Gradle, or any other build automation tool of your choice, and lines 15 to 19 in the script, marked with `ENTER HERE`, must be filled with the proper configuration settings:
* `host`: server name or IP address on which your MySQL-server is running i.e. *localhost*
* `user`: username of MySQL-server i.e. *root*
* `password`: password of MySQL-server
* `database`: name of a new database to store all metrics tables
* `table`: table name assigned by you that corresponds to the target project.

The outcome of the executed script is a table that contains all Java classes, their corresponding Java files, and their calculated metrics. Using a MySQL query you can then merge each `all_files` table that represents a single project with the table that contains the metrics by matching the `java_file` attribute. 

# Data Analysis
## Classifiers and Predictions
The predictions are carried out using `ML_pipeline.ipynb`. The pipeline must be run once for each classifier you wish to use. First, choose a classifier from the list in the pipeline (or add a new one of your choice) and assign to the `clf` variable. Second, specify the directory that you wish to save the results in and assign to the `folder` variable. 



