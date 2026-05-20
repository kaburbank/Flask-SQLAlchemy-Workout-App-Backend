# Flask SQLAlchemy Workout App Backend

A backend API for tracking workouts and exercises using Flask, SQLAlchemy, and Marshmallow.

## Features
- Create, view, and delete workouts and exercises
- Add exercises to workouts with sets, reps, and duration
- Validations at model, schema, and database levels

## Setup
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```
2. Run migrations:
   ```bash
   pipenv run flask db init
   pipenv run flask db migrate -m "Initial migration"
   pipenv run flask db upgrade
   ```
3. Start the server:
   ```bash
   pipenv run python server/app.py
   ```

## Endpoints
See the code for available endpoints.
