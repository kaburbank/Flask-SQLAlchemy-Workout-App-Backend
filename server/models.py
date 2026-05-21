from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Define Models here

# Relationships:
# - A WorkoutExercise belongs to a Workout
# - A WorkoutExercise belongs to an Exercise
# - A Workout has many WorkoutExercises
# - An Exercise has many WorkoutExercises
# - A Workout has many Exercises through WorkoutExercises
# - An Exercise has many Workouts through WorkoutExercises

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    __table_args__ = (
        db.UniqueConstraint('name', name='uq_exercise_name'),  # Table constraint: name must be unique
    )

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    # An Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value) < 3:
            raise ValueError('Exercise name must be at least 3 characters long.')
        return value

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.CheckConstraint('duration_minutes IS NULL OR duration_minutes >= 0', name='ck_workout_duration_positive'),  # Table constraint: duration_minutes must be positive if present
    )

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    # A Workout has many Exercises through WorkoutExercises
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

    @validates('date')
    def validate_date(self, key, value):
        from datetime import date as dt_date
        if value > dt_date.today():
            raise ValueError('Workout date cannot be in the future.')
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),  # Table constraint: prevent duplicate exercise in the same workout
        db.CheckConstraint('reps IS NULL OR reps >= 0', name='ck_reps_positive'),
        db.CheckConstraint('sets IS NULL OR sets >= 0', name='ck_sets_positive'),
        db.CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='ck_duration_positive'),
    )

    # A WorkoutExercise belongs to a Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')
    # A WorkoutExercise belongs to an Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets', 'reps', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key.capitalize()} must be non-negative.')
        return value
