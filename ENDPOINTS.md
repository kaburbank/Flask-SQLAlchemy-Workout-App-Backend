# API Endpoints

## Workouts
- **GET /workouts**: List all workouts
- **GET /workouts/<id>**: Show a single workout with its associated exercises and details
- **POST /workouts**: Create a new workout (fields: date, duration_minutes, notes)
- **DELETE /workouts/<id>**: Delete a workout (deletes associated WorkoutExercises)

## Exercises
- **GET /exercises**: List all exercises
- **GET /exercises/<id>**: Show an exercise and associated workouts
- **POST /exercises**: Create a new exercise (fields: name, category, equipment_needed)
- **DELETE /exercises/<id>**: Delete an exercise (deletes associated WorkoutExercises)

## WorkoutExercises
- **POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises**: Add an exercise to a workout, including reps/sets/duration

See the code for request/response examples and validation details.
