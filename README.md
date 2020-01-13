# Agent-based modelling project

## Requirements
* python 3.6.4
* pip
* virtualenv

## Setup
* clone repo
* create virtualenv inside '/abm': ```python -m venv env```
* activate virtual environment: ```source env/bin/activate``` (for windows users use `\env\Scripts\activate.bat`)
* install requirements: ```pip install -r requirements.txt```

## Adding dependencies
* activate virtual environment: ```source env/bin/activate```
* install package: ```pip install <package_name>```
* write requirements: ```pip freeze > requirements.txt```
* push requirements.txt to GitHub

## Note on .gitignore
After creating virtual environment it is also recommended to create a file called '.gitignore'
In this file you can include stuff that you don't want to commit to GitHub.
For example, I don't want to commit my environment. In this case the content of '.gitignore' would be one line:
* /env
