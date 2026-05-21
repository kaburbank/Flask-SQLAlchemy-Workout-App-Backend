
# Flask SQLAlchemy Workout App Backend

## Project Description
A backend REST API for tracking workouts and exercises, built with Flask, SQLAlchemy, and Marshmallow. Supports full CRUD for workouts and exercises, and allows adding exercises to workouts with reps, sets, and duration. Includes robust validation at the model, schema, and database levels.

## Installation Instructions
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```
2. Run migrations:
   ```bash
   pipenv run flask --app migrate.py db init
   pipenv run flask --app migrate.py db migrate -m "Initial migration"
   pipenv run flask --app migrate.py db upgrade
   ```
3. Seed the database with example data:
   ```bash
   pipenv run python server/seed.py
   ```

## Run Instructions
Start the development server:
```bash
pipenv run python server/app.py
```

## API Endpoints
See ENDPOINTS.md for a full list and descriptions of all endpoints.

## Files Included
- Full Flask application (server/ directory)
- Seed script: server/seed.py
- Pipfile with all dependencies
- README.md (this file)
- ENDPOINTS.md (endpoint documentation)

## Testing
Test files can be added in a tests/ directory (not included by default).
