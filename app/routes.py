
# API routes will be defined here
from flask import Blueprint, request, jsonify
from app import db
from app.models import Exercise, Workout, WorkoutExercise
from app.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from datetime import datetime

bp = Blueprint('api', __name__)

# Exercise endpoints
@bp.route('/exercises', methods=['POST'])
def create_exercise():
	data = request.get_json()
	schema = ExerciseSchema()
	try:
		validated = schema.load(data)
		exercise = Exercise(**validated)
		db.session.add(exercise)
		db.session.commit()
		return schema.jsonify(exercise), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 400

@bp.route('/exercises', methods=['GET'])
def get_exercises():
	exercises = Exercise.query.all()
	schema = ExerciseSchema(many=True)
	return schema.jsonify(exercises), 200


# Show an exercise and associated workouts
@bp.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
	exercise = Exercise.query.get_or_404(id)
	schema = ExerciseSchema()
	# Get all workouts for this exercise
	workouts = [we.workout for we in exercise.workout_exercises]
	workout_schema = WorkoutSchema(many=True)
	result = schema.dump(exercise)
	result['workouts'] = workout_schema.dump(workouts)
	return jsonify(result), 200

# Delete exercise and associated WorkoutExercises
@bp.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
	exercise = Exercise.query.get_or_404(id)
	# Delete associated WorkoutExercises
	WorkoutExercise.query.filter_by(exercise_id=id).delete()
	db.session.delete(exercise)
	db.session.commit()
	return '', 204

# Workout endpoints
@bp.route('/workouts', methods=['POST'])
def create_workout():
	data = request.get_json()
	schema = WorkoutSchema()
	try:
		validated = schema.load(data)
		workout = Workout(**validated)
		db.session.add(workout)
		db.session.commit()
		return schema.jsonify(workout), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 400

@bp.route('/workouts', methods=['GET'])
def get_workouts():
	workouts = Workout.query.all()
	schema = WorkoutSchema(many=True)
	return schema.jsonify(workouts), 200


# Show a single workout with its associated exercises and details
@bp.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
	workout = Workout.query.get_or_404(id)
	schema = WorkoutSchema()
	# Get all WorkoutExercises for this workout
	workout_exercises = WorkoutExercise.query.filter_by(workout_id=id).all()
	exercise_schema = ExerciseSchema()
	exercises = []
	for we in workout_exercises:
		ex = exercise_schema.dump(we.exercise)
		ex['reps'] = we.reps
		ex['sets'] = we.sets
		ex['duration_seconds'] = we.duration_seconds
		exercises.append(ex)
	result = schema.dump(workout)
	result['exercises'] = exercises
	return jsonify(result), 200

# Delete workout and associated WorkoutExercises
@bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
	workout = Workout.query.get_or_404(id)
	# Delete associated WorkoutExercises
	WorkoutExercise.query.filter_by(workout_id=id).delete()
	db.session.delete(workout)
	db.session.commit()
	return '', 204

from flask import Blueprint, request, jsonify
from app import db
from app.models import Exercise, Workout, WorkoutExercise
from app.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from datetime import datetime

# Add an exercise to a workout, including reps/sets/duration
@bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
	data = request.get_json() or {}
	data['workout_id'] = workout_id
	data['exercise_id'] = exercise_id
	schema = WorkoutExerciseSchema()
	try:
		validated = schema.load(data)
		we = WorkoutExercise(**validated)
		db.session.add(we)
		db.session.commit()
		return schema.jsonify(we), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 400
