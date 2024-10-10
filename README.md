# COS40005 - Computing Technology Project A

This is a Django-based application designed to crawl property listings from various real estate wensites and store them in a database. The application uses Selenium to navigate and extract information from web pages and updates the status of processed URLs.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Crawl property listings from specified real estate domains.
- Store crawled URLs and mark them as visited to avoid duplication.
- Extract and assign real estate property details such as title, address, price, area, etc.
- Update the status of processed properties.

## Requirements

- Python 3.x
- Django 3.x or higher
- Selenium
- Chrome WebDriver
- Docker (for running with Docker Compose)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/hwanginhanoi/COS40005.git
cd COS40005
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3.	Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run Docker compose for Redis, PostgreSQL and RabbitMQ
```bash
docker-compose up
```

5. Set up the Django project:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

6. Run Celery Scheduler
```Bash
celery -A cos40005 beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

7. Run Celery Worker
```Bash
celery -A cos40005 worker -l info
celery -A cos40005 worker --pool=threads --concurrency=5 --loglevel=info
```