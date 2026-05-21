from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import validates, ValidationError, validates_schema
from server.models import Exercise, Workout, WorkoutExercise

class ExerciseSchema(SQLAlchemyAutoSchema):
    @validates('name')
    def validate_name(self, value):
        if not value or len(value) < 3:
            raise ValidationError('Exercise name must be at least 3 characters long.')

    class Meta:
        model = Exercise
        load_instance = True
        include_relationships = True
        sqla_session = None

    workout_exercises = Nested('WorkoutExerciseSchema', many=True, exclude=("exercise",), dump_only=True)
    workouts = Nested('WorkoutSchema', many=True, exclude=("exercises", "workout_exercises"), dump_only=True)

class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True
        sqla_session = None

    exercise = Nested('ExerciseSchema', exclude=("workout_exercises", "workouts"), dump_only=True)
    workout = Nested('WorkoutSchema', exclude=("workout_exercises", "exercises"), dump_only=True)

class WorkoutSchema(SQLAlchemyAutoSchema):
    @validates('date')
    def validate_date(self, value):
        from datetime import date as dt_date
        if value > dt_date.today():
            raise ValidationError('Workout date cannot be in the future.')

    @validates_schema
    def validate_positive_fields(self, data, **kwargs):
        for field in ['reps', 'sets', 'duration_seconds']:
            val = data.get(field)
            if val is not None and val < 0:
                raise ValidationError(f"{field} must be non-negative.")

    class Meta:
        model = Workout
        load_instance = True
        include_relationships = True
        sqla_session = None

    exercises = Nested('ExerciseSchema', many=True, exclude=("workouts", "workout_exercises"), dump_only=True)
    workout_exercises = Nested('WorkoutExerciseSchema', many=True, exclude=("workout",), dump_only=True)
