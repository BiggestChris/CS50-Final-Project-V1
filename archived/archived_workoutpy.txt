import re, os
from datetime import datetime

from flask import request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(100), nullable=False)
    setOne = db.Column(db.Integer)
    setTwo = db.Column(db.Integer)
    setThree = db.Column(db.Integer)
    setFour = db.Column(db.Integer)
    setFive = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Exercise {self.exercise}>'
    
# Help received from ChatGPT refining this function
def exercise(app):
    exercise_name = request.form.get("exercise")
    set_one = request.form.get("set-one")

    # Create an instance of Exercise
    exercise = Exercise(exercise=exercise_name, setOne=set_one)

    # Define a list of set fields
    set_fields = [{'input': 'set-two', 'attribute': 'setTwo'},
                    {'input': 'set-three', 'attribute': 'setThree'},
                    {'input': 'set-four', 'attribute': 'setFour'},
                    {'input': 'set-five', 'attribute': 'setFive'}]

    # Loop through the set fields
    for field in set_fields:
        # Get the value of the corresponding form field
        value = request.form.get(field['input'])

        # Check if the value is provided and assign it to the instance
        if value:
            # Use setattr() to dynamically set the attribute
            setattr(exercise, field['attribute'], value)

    # Add the instance to the session and commit changes
    db.session.add(exercise)
    db.session.commit()