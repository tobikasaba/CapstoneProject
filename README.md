# IBM Back-End Development Capstone

Capstone project for the IBM Back-End Developer Professional Certificate. The
repository demonstrates a small backend system built with a Django web
application, Flask REST microservices, seed data, automated tests, Docker
images, and an unfinished Kubernetes deployment scaffold.

The main application is a fictional band website called **Djirection**. Users can
sign up, log in, browse songs and photos from separate microservices, view
concerts, and RSVP as attending or not attending.

## What This Project Contains

| Directory | Purpose |
| --- | --- |
| `Back-end-Development-Capstone/` | Django web application for the Djirection site, authentication, concert pages, and RSVP workflow. |
| `Back-End-Development-Pictures/` | Flask REST API that serves and mutates picture/event data from an in-memory JSON seed list. |
| `Back-End-Development-Songs/` | Flask REST API that serves and mutates song data stored in MongoDB and seeded from JSON on startup. |
| `tutorial/` | Standalone Flask and MongoDB tutorial exercises used as learning references. |
| `requirements.txt` | Root dependency list covering the main Python stack used across the repo. |

## Architecture

The project is split into a web frontend/backend and two API services:

1. The Django app renders HTML templates for the band website.
2. The Django app calls the Songs API through `SONGS_URL`.
3. The Django app calls the Pictures API through `PICTURES_URL`.
4. Users authenticate through Django's built-in user model.
5. Concerts and RSVP records are stored in the Django database.
6. Song records are owned by the Songs microservice.
7. Picture records are owned by the Pictures microservice.

By default, the Django app points to deployed Render URLs for the Songs and
Pictures services. For local development, set `SONGS_URL` and `PICTURES_URL` to
your local Flask service URLs.

## Tech Stack

- Python 3.10+
- Django 4.2
- Flask 2.3
- MongoDB with PyMongo
- SQLite for local Django development
- Requests for service-to-service HTTP calls
- Bootstrap and Bootstrap Icons for the Django templates
- Pytest for API tests
- Docker for containerized service builds
- Kubernetes YAML scaffold for deployment practice

## Django Web App

Location: `Back-end-Development-Capstone/`

Key features:

- Public home page for the Djirection band
- User signup, login, and logout
- Songs page populated from the Songs microservice
- Photos page populated from the Pictures microservice
- Authenticated concerts page
- Concert detail page with RSVP form
- Admin-managed concerts
- Read-only Django admin models for externally owned songs and photos

Important files:

- `manage.py` - Django command entry point
- `django_concert/settings.py` - Django configuration
- `concert/models.py` - Concert, RSVP, Song, and Photo models
- `concert/views.py` - Page handlers and microservice calls
- `concert/urls.py` - Web routes
- `templates/` - Django HTML templates
- `Dockerfile` and `entrypoint.sh` - Container runtime setup

Required environment variables:

```bash
DJANGO_SECRET_KEY=replace-me
```

Optional environment variables:

```bash
DEBUG=True
SONGS_URL=http://localhost:8081
PICTURES_URL=http://localhost:8082
```

The Docker entrypoint also expects these values when creating a superuser:

```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=change-me
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### Run the Django App Locally

```bash
cd Back-end-Development-Capstone
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_SECRET_KEY=dev-secret-key
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The app will run at:

```text
http://127.0.0.1:8000/
```

## Pictures Microservice

Location: `Back-End-Development-Pictures/`

This Flask API loads `backend/data/pictures.json` into an in-memory Python list
when the app starts. Changes made through the API last only until the service is
restarted.

Endpoints:

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check. |
| `GET` | `/count` | Count picture records. |
| `GET` | `/picture` | Return all pictures. |
| `GET` | `/picture/<id>` | Return one picture by numeric ID. |
| `POST` | `/picture` | Create a picture record. |
| `PUT` | `/picture/<id>` | Update a picture record. |
| `DELETE` | `/picture/<id>` | Delete a picture record. |

Run locally:

```bash
cd Back-End-Development-Pictures
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The development server uses port `8080` when started with `python app.py`.

Docker:

```bash
cd Back-End-Development-Pictures
docker build -t pictures-service .
docker run -p 3000:3000 pictures-service
```

## Songs Microservice

Location: `Back-End-Development-Songs/`

This Flask API loads `backend/data/songs.json`, connects to MongoDB, drops the
`songs` collection, and reloads the seed data on startup. Because the collection
is reset at startup, local changes made through the API are not durable across
service restarts.

Required service dependency:

- MongoDB running locally or available through `MONGODB_URI`

Environment variable:

```bash
MONGODB_URI=mongodb://localhost:27017
```

Endpoints:

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check. |
| `GET` | `/count` | Count song records. |
| `GET` | `/song` | Return all songs. |
| `GET` | `/song/<id>` | Return one song by numeric ID. |
| `POST` | `/song` | Create a song record. |
| `PUT` | `/song/<id>` | Update a song record. |
| `DELETE` | `/song/<id>` | Delete a song record. |

Run locally:

```bash
cd Back-End-Development-Songs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MONGODB_URI=mongodb://localhost:27017
python app.py
```

The development server uses port `8080` when started with `python app.py`.

Docker:

```bash
cd Back-End-Development-Songs
docker build -t songs-service .
docker run -p 3000:3000 -e MONGODB_URI=mongodb://host.docker.internal:27017 songs-service
```

## Running Services Together Locally

Because both Flask services default to port `8080` when run with `python app.py`,
run one of them through the Flask CLI on a different port:

```bash
cd Back-End-Development-Songs
export MONGODB_URI=mongodb://localhost:27017
flask --app app run --host=0.0.0.0 --port=8081
```

```bash
cd Back-End-Development-Pictures
flask --app app run --host=0.0.0.0 --port=8082
```

Then start Django with local service URLs:

```bash
cd Back-end-Development-Capstone
export DJANGO_SECRET_KEY=dev-secret-key
export SONGS_URL=http://localhost:8081
export PICTURES_URL=http://localhost:8082
python manage.py runserver
```

## Testing

Each Flask microservice has its own pytest suite:

```bash
cd Back-End-Development-Pictures
pytest
```

```bash
cd Back-End-Development-Songs
pytest
```

The Pictures tests exercise the CRUD API. The Songs test suite currently checks
the health endpoint.

## Deployment Notes

- Each main app/service includes a `Dockerfile`.
- `Back-end-Development-Capstone/deployment.yml` is a Kubernetes deployment
  scaffold with placeholders for `kind`, image, and container port.
- The Django container entrypoint runs migrations and creates a superuser from
  environment variables before starting the server.
- The Django app uses SQLite by default for local development.

## Development Notes

- The `tutorial/` directory is separate from the deployable apps and can be used
  as reference material for Flask and MongoDB basics.
- The Songs service resets MongoDB seed data every time the application imports
  its routes.
- The Pictures service stores data in memory only.
- For production-like deployment, replace development secrets, disable Django
  debug mode, configure persistent databases, and complete the Kubernetes
  manifest.
