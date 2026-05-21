from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from server.models import Exercise, Workout, WorkoutExercise

class ExerciseSchema(SQLAlchemyAutoSchema):
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
    class Meta:
        model = Workout
        load_instance = True
        include_relationships = True
        sqla_session = None
    exercises = Nested('ExerciseSchema', many=True, exclude=("workouts", "workout_exercises"), dump_only=True)
    workout_exercises = Nested('WorkoutExerciseSchema', many=True, exclude=("workout",), dump_only=True)
