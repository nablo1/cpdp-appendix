# Online appendix for manuscript "What makes a good project for Cross-Project Software Defect Prediction?"
This is the online appendix for manuscript "What makes a good project for Cross-Project Software Defect Prediction? *The role of size, domain, and diversity*". A Bachelor thesis study in Software Engineering and Management, submitted in June 2022, and created by:
* Mohammad Nablo | University of Gothenburg 
* Jakob Roseke | University of Gothenburg 

# Table of contents
* [1. Study Overview](https://github.com/nablo1/cpdp-appendix#study-overview)
* [2. Repository content](https://github.com/nablo1/cpdp-appendix#repository-content)
* [3. Introduction and requirements](https://github.com/nablo1/cpdp-appendix#introduction-and-requirements)
* [4. Data collection](https://github.com/nablo1/cpdp-appendix#data-collection)
  * [4.1 Labeling files](https://github.com/nablo1/cpdp-appendix#labeling-files)
  * [4.2 Calculation of metrics](https://github.com/nablo1/cpdp-appendix#calculation-of-metrics)
* [5. Data analysis](https://github.com/nablo1/cpdp-appendix#data-analysis)
  * [5.1 Classifiers and predictions](https://github.com/nablo1/cpdp-appendix#classifiers-and-predictions)
  * [5.2 Statistical analysis](https://github.com/nablo1/cpdp-appendix#statistical-analysis)

# Study Overview
The study extends prior research on software defect prediction. In particular, cross-project defect prediction. We conducted an experiment where we investigated the impact of the size and domain of a project, as well as the diversity of a selection of projects on the prediction results. We constructed a dataset based on 40 open-source GitHub Java projects, ran various predictions using 6 different ML classifiers, and performed statistical significance tests on the produced results to achieve our objectives. 

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


