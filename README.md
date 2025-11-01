🛍️ DjangoOnlineStore

DjangoOnlineStore is a web-based e-commerce application built using Django, PostgreSQL, and Docker Compose.
It includes a PostgreSQL database, an Adminer interface for database management, and a Django web application for store management.

🚀 Tech Stack

Python 3.12+

Django 5.2

PostgreSQL 17 (Alpine)

Adminer (Database management UI)

Docker & Docker Compose

📁 Project Structure

Environment Setup

1. Create a .env file in the root directory with the following variables:

POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=onlinestore_db

2. Make sure Docker and Docker Compose are installed on your system.

3. (Optional) If you want to run it locally without Docker:
pip install -r requirements.txt

🐳 Run with Docker Compose

Start all services:

docker compose up --build

Once running:

Django app: http://localhost:8000
Adminer (database UI): http://localhost:8080

🗄️ Connect to Database via Adminer

1. Go to http://localhost:8080
2. Use the following credentials:

System: PostgreSQL
Server: psql
Username: admin
Password: admin123
Database: onlinestore_db

3. Click Login to access and manage your database.

🧱 Docker Services
Service	Description	Port
web	Django web application	8000
psql	PostgreSQL database	5432
adminer	Database management interface	8080

Useful Commands

Run Django migrations:

docker compose exec web python manage.py migrate

Create a Django superuser:

docker compose exec web python manage.py createsuperuser

Access Django container shell:

docker compose exec web bash

Stop containers:

docker compose down

Remove containers and volumes:

docker compose down -v



