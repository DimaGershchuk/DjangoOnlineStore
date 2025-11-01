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




