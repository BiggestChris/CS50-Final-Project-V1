import re, os
from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
import json
from flask_basicauth import BasicAuth



app = Flask(__name__)

# Define the database object globally
db = None

# Function to connect to the database only when needed and then close - ChatGPT helped with this, I was receiving timeout errors when the application was open fro more than 5 minutes
def get_database():
    global db
    if db is None:
        # Configure CS50 Library to use MySQL database on PythonAnywhere
        db = SQL("mysql://BiggestChris:!Xy7nhhHZmdmFyr@BiggestChris.mysql.eu.pythonanywhere-services.com/BiggestChris$fitness")
    return db

# Unsure if I can explicitly close the connection - but need a way to manage as a placeholder
def close_database():
    global db
    if db is not None:
        db = None
    return "Database connection closed"

# Import workout after defining db and app
from workout import exercise, weight_import, food_import, weight_export, food_export, exercise_export, retrieve_workout
from workoutobject import workout_list
workout_list_json = json.dumps(workout_list)


# ChatGPT helped with authorisation code
app.config['BASIC_AUTH_USERNAME'] = 'Chris'
app.config['BASIC_AUTH_PASSWORD'] = 'Gym5TYL3!'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@basic_auth.required
def basic_auth_check():
    pass  # This function is needed to ensure basic auth is checked for all routes


@app.route("/")
def home():
    return render_template("home.html")


# Help received from ChatGPT refining this function
@app.route("/workout", methods=('GET', 'POST'))
def workout():
    if request.method == 'POST':
        get_database()
        exercise()
        close_database()


        return redirect("/workout")
    else:
        get_database()
        last_workout = retrieve_workout()
        last_workout_json = json.dumps(last_workout)
        close_database()

        return render_template("workout.html", workout_list=workout_list, workout_list_json=workout_list_json, last_workout_json=last_workout_json)



@app.route("/food", methods=('GET', 'POST'))
def food():
    if request.method == 'POST':
        get_database()
        food_import()
        close_database()

        return redirect("/")
    else:
        return render_template("food.html")


@app.route("/weight", methods=('GET', 'POST'))
def weight():
    if request.method == 'POST':
        get_database()
        weight_import()
        close_database()

        return redirect("/")
    else:
        return render_template("weight.html")


@app.route("/export")
def export_page():
    return render_template("export.html")


@app.route("/weight_export", methods=('GET', 'POST'))
def get_data_weight():
    if request.method == 'POST':
        get_database()
        weight_export()
        close_database()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/food_export", methods=('GET', 'POST'))
def get_data_food():
    if request.method == 'POST':
        get_database()
        food_export()
        close_database()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/exercise_export", methods=('GET', 'POST'))
def get_data_exercise():
    if request.method == 'POST':
        get_database()
        exercise_export()
        close_database()

        return redirect("/")
    else:
        return render_template("export.html")