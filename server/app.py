from flask import Flask, request, jsonify, abort
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)


    # --- Workouts Endpoints ---
    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.all()
        return jsonify(WorkoutSchema(many=True).dump(workouts)), 200

    @app.route('/workouts/<int:workout_id>', methods=['GET'])
    def get_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        # Stretch: include reps/sets/duration from WorkoutExercises
        return jsonify(WorkoutSchema().dump(workout)), 200

    @app.route('/workouts', methods=['POST'])
    def create_workout():
        data = request.get_json()
        schema = WorkoutSchema()
        try:
            workout = schema.load(data)
            db.session.add(workout)
            db.session.commit()
            return jsonify(schema.dump(workout)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    @app.route('/workouts/<int:workout_id>', methods=['DELETE'])
    def delete_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        # Stretch: delete associated WorkoutExercises (handled by cascade)
        db.session.delete(workout)
        db.session.commit()
        return '', 204

    # --- Exercises Endpoints ---
    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.all()
        return jsonify(ExerciseSchema(many=True).dump(exercises)), 200

    @app.route('/exercises/<int:exercise_id>', methods=['GET'])
    def get_exercise(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        return jsonify(ExerciseSchema().dump(exercise)), 200

    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        data = request.get_json()
        schema = ExerciseSchema()
        try:
            exercise = schema.load(data)
            db.session.add(exercise)
            db.session.commit()
            return jsonify(schema.dump(exercise)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    @app.route('/exercises/<int:exercise_id>', methods=['DELETE'])
    def delete_exercise(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        # Stretch: delete associated WorkoutExercises (handled by cascade)
        db.session.delete(exercise)
        db.session.commit()
        return '', 204

    # --- Add Exercise to Workout ---
    @app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
    def add_exercise_to_workout(workout_id, exercise_id):
        data = request.get_json()
        # Ensure workout and exercise exist
        Workout.query.get_or_404(workout_id)
        Exercise.query.get_or_404(exercise_id)
        schema = WorkoutExerciseSchema()
        try:
            we = schema.load({**data, 'workout_id': workout_id, 'exercise_id': exercise_id})
            db.session.add(we)
            db.session.commit()
            return jsonify(schema.dump(we)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
