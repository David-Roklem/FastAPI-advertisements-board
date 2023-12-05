# Test-task-Productivity-Inside
This test task is dedicated to a service which utilizes FastAPI framework for advertisements board development

## Getting Started
You can clone this repository by using terminal command:
```
git clone https://github.com/David-Roklem/Test-task-Productivity-Inside.git
```

### Dependencies
All the dependencies for this project are listed in pyproject.toml and requirements.txt files.

### Installing
This project uses poetry as a package manager as well as virtual environment. So install poetry with the command in terminal:
```
pip install poetry
```
After that, for installing all the required dependencies, run:
```
poetry install
```
Alternatively, if you don't want to use Poetry, there is ready-to-use requirements.txt file. You can install the dependecies by this command:
```
pip install -r requirements.txt
```

### PostgreSQL
The code base is adapted for utilizing PostgreSQL. If you wish to use another database, you will need to rewrite code in order to satisfy new requirements (provide correct DSN format in config.py).

### Executing program
As this project uses [https://pypi.org/project/python-dotenv/](python-dotenv) library, first of all you need to configure your .env with the following variables:
```
DB_NAME=''
DB_USER=''
DB_PASS=''
DB_HOST=''
DB_PORT=int

SECRET_KEY=''
ALGORITHM=''
ACCESS_TOKEN_EXPIRE_MINUTES=''
```
