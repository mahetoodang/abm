# FriendSim Agent Based Model 🤝

## Requirements
* python 3.6.4
* pip
* virtualenv

## Setup
* clone the repository to your local machine.
* create virtualenv inside '/abm': ```python -m venv env```
* activate virtual environment: ```source env/bin/activate``` (for windows users use `\env\Scripts\activate.bat`)
* install requirements: ```pip install -r requirements.txt```

## Running the simulation

To run a model run the `main.py`, this will produce data and plots inside the `data` folder.

## User Interface

To visualise the simulation inside of the browser, run `server.py` inside of the `visualization` folder.

## Configuration

### `main.py`

Inside `main.py` you are able to configure what type of simulation you would like to run. Specifically you can set `mobility, social_hubs, segregation`, as well as specify the number of iterations in the `main()` function at the end of the file.

If you set `iter=1` and set `create_model_report(html_report=True)` then additionally an browser-based data visualisation of key statistics will be generated.

### `model.py`

To have more control over changing parameters directly, you can edit the initialisation variables of the `Friends()` class inside `model.py` located inside the `functionality` folder.

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
* __pycache__
