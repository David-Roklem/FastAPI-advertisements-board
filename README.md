# Inroduction
This project utilizes FastAPI framework for advertisements board development. It uses SQLalchemy as ORM which wraps PostgreSQL. As a migration tool Alembic is presented.

## Getting Started
You can clone this repository by using terminal command:
```
git clone https://github.com/David-Roklem/FastAPI-advertisements-board.git
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
As this project uses [python-dotenv](https://pypi.org/project/python-dotenv/) library, first of all you need to configure your .env with the following variables:
```
DB_NAME=''
DB_USER=''
DB_PASS=''
DB_HOST=''
DB_PORT=int

SECRET_KEY=''
ALGORITHM=''
ACCESS_TOKEN_EXPIRE_MINUTES=int
```
Also, as you can see, there are three constants which are required for JWT authentication. For testing usage you can set them up as follows: ``` SECRET_KEY = "secret", ALGORITHM = "HS256", ACCESS_TOKEN_EXPIRE_MINUTES = 30 ```
In production SECRET_KEY must be generated automatically by some safe algorithm and stored in a secure place.

To run the project on your local machine you should follow these steps:
1) configure you database, then run it
2) apply migrations to your database by the command:
```
alembic upgrade head
```
3) run src/main.py file:
```
poetry shell
python src/main.py
```
4) go to http://127.0.0.1:8000/docs
5) now you can make use of all the path operations using Swagger UI

### Project's current state
At this point, these *main tasks* are finished:

✅Регистрация пользователя

✅Вход в систему

✅Размещение объявления

✅Просмотр списка всех объявлений

✅Просмотр списка объявлений пользователя

✅Детальный просмотр одного объявления

✅Удаление своего объявления



**Администратор может:**

✅Все выше перечисленное

✅Удаление комментариев в любой группе объявлений

✅Назначение пользователя администратором



**Дополнительный функционал:**

✅Серверная пагинация

✅Фильтрация объявлений

✅Авторизация с помощью JWT-токена

🔭 Тестирование приложения

🔭Настройка CI/CD через Github actions

🔭Сборка проекта в докер-образ

🔭Настройка логгера(терминал)

🔭При критических ошибках отправление ошибки в телеграмм чат

🔭Реализовать работу через No-SQL DB (MongoDB)
