# ticket-service
Ticketing Rest API Backend Project

## Getting started:
### Clone this repository:
```
git clone https://github.com/ticket-service.git
```
### Install pipenv
```
pip install pipenv
```
### Activate environment:
```
pipenv shell
```
### Install dependencies:
```
pipenv install
```
### create database in postgres:
```
CREATE DATABASE ticket_service;
```
### create environment variables
```
Create a .env file by copying the .env.example file.
After copying the contents, edit the SECRET_KEY with your respective secret key.
In DATABASE_URL, replace your_database_user and your_database_password with your respective Database User and Password.
```
### Start the server:
``` 
python manage.py runserver
```
