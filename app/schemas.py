# Marshmallow schemas will be defined here
from marshmallow import Schema, fields, validates, ValidationError
from datetime import date


class ExerciseSchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True)
	category = fields.Str()
	equipment_needed = fields.Bool(required=True)

	@validates('name')
	def validate_name(self, value):
		if len(value) < 3:
			raise ValidationError('Exercise name must be at least 3 characters long.')



class WorkoutSchema(Schema):
	id = fields.Int(dump_only=True)
	date = fields.Date(required=True)
	duration_minutes = fields.Int(allow_none=True)
	notes = fields.Str(allow_none=True)

	@validates('date')
	def validate_date(self, value):
		if value > date.today():
			raise ValidationError('Workout date cannot be in the future.')



class WorkoutExerciseSchema(Schema):
	id = fields.Int(dump_only=True)
	workout_id = fields.Int(required=True)
	exercise_id = fields.Int(required=True)
	reps = fields.Int(allow_none=True)
	sets = fields.Int(allow_none=True)
	duration_seconds = fields.Int(allow_none=True)

	@validates('sets')
	def validate_sets(self, value):
		if value is not None and value < 0:
			raise ValidationError('Sets must be non-negative.')

	@validates('reps')
	def validate_reps(self, value):
		if value is not None and value < 0:
			raise ValidationError('Reps must be non-negative.')

	@validates('duration_seconds')
	def validate_duration(self, value):
		if value is not None and value < 0:
			raise ValidationError('Duration must be non-negative.')
