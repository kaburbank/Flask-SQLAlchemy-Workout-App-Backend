from flask import Flask, make_response
from flask_migrate import Migrate
from .models import db, Exercise, Workout, WorkoutExercise
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    # Define Routes here

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
