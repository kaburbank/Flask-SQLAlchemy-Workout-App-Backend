from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Define Models here

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')
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

    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uq_workout_exercise'),
    )

    @validates('sets', 'reps', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key.capitalize()} must be non-negative.')
        return value
