import pytest
from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise
from flask import json
from datetime import date

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_exercise(client):
    response = client.post('/exercises', json={
        'name': 'Push Up',
        'category': 'Strength',
        'equipment_needed': False
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Push Up'
    assert data['category'] == 'Strength'
    assert data['equipment_needed'] is False

def test_create_workout(client):
    response = client.post('/workouts', json={
        'date': date.today().isoformat(),
        'duration_minutes': 30,
        'notes': 'Morning workout'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['duration_minutes'] == 30
    assert data['notes'] == 'Morning workout'

def test_add_exercise_to_workout(client):
    # Create exercise
    ex_resp = client.post('/exercises', json={
        'name': 'Squat',
        'category': 'Strength',
        'equipment_needed': False
    })
    ex_id = ex_resp.get_json()['id']
    # Create workout
    wo_resp = client.post('/workouts', json={
        'date': date.today().isoformat(),
        'duration_minutes': 20
    })
    wo_id = wo_resp.get_json()['id']
    # Add exercise to workout
    we_resp = client.post(f'/workouts/{wo_id}/exercises/{ex_id}/workout_exercises', json={
        'reps': 10,
        'sets': 3,
        'duration_seconds': 60
    })
    assert we_resp.status_code == 201
    data = we_resp.get_json()
    assert data['reps'] == 10
    assert data['sets'] == 3
    assert data['duration_seconds'] == 60
