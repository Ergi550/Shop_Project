# Shop Project

Full-stack e-commerce app — Django REST backend + Angular frontend + PostgreSQL via Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (must be running)
- [Node.js](https://nodejs.org/) + npm (for the Angular frontend)

## Getting Started

### 1. Create the environment file

Create a `.env` file in the project root (next to `docker-compose.yml`):

```
DB_PASSWORD=your_password_here
```

### 2. Start the backend (Django + PostgreSQL)

```bash
docker compose up --build
```

This starts:
- **PostgreSQL** on internal port 5432
- **Django** on http://localhost:8000

On first run, apply migrations:

```bash
docker compose exec backend python manage.py migrate
```

To create a superuser for the Django admin:

```bash
docker compose exec backend python manage.py createsuperuser
```

Django admin is available at http://localhost:8000/admin

### 3. Start the frontend (Angular)

In a separate terminal:

```bash
cd frontend
npm install
npm start
```

Angular dev server runs at http://localhost:4200

## Stopping

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```