#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

app = create_app()

with app.app_context():
    # Clear all tables
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Create example exercises
    pushup = Exercise(name='Push Up', category='Strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='Strength', equipment_needed=False)
    run = Exercise(name='Running', category='Cardio', equipment_needed=False)
    db.session.add_all([pushup, squat, run])
    db.session.commit()


    # Use today and yesterday for valid workout dates
    today = date.today()
    yesterday = today - timedelta(days=1)
    workout1 = Workout(date=yesterday, duration_minutes=30, notes='Morning workout')
    workout2 = Workout(date=today, duration_minutes=45, notes='Evening workout')
    db.session.add_all([workout1, workout2])
    db.session.commit()

    # Add exercises to workouts
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushup.id, reps=15, sets=3, duration_seconds=None)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squat.id, reps=20, sets=3, duration_seconds=None)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=run.id, reps=None, sets=None, duration_seconds=1200)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print('Database seeded successfully!')
