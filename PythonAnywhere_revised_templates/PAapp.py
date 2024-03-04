import re, os
from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
import json
from flask_basicauth import BasicAuth



app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("mysql://BiggestChris:!Xy7nhhHZmdmFyr@BiggestChris.mysql.eu.pythonanywhere-services.com/BiggestChris$fitness")

# Import workout after defining db and app
from workout import exercise, weight_import, food_import, weight_export, food_export, exercise_export, retrieve_workout
from workoutobject import workout_list
workout_list_json = json.dumps(workout_list)


# ChatGPT helped with authorisation code
app.config['BASIC_AUTH_USERNAME'] = 'Chris'
app.config['BASIC_AUTH_PASSWORD'] = 'Test'
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
        exercise()

        return redirect("/workout")
    else:
        last_workout = retrieve_workout()
        last_workout_json = json.dumps(last_workout)

        return render_template("workout.html", workout_list=workout_list, workout_list_json=workout_list_json, last_workout_json=last_workout_json)



@app.route("/food", methods=('GET', 'POST'))
def food():
    if request.method == 'POST':
        food_import()

        return redirect("/")
    else:
        return render_template("food.html")


@app.route("/weight", methods=('GET', 'POST'))
def weight():
    if request.method == 'POST':
        weight_import()

        return redirect("/")
    else:
        return render_template("weight.html")


@app.route("/export")
def export_page():
    return render_template("export.html")


@app.route("/weight_export", methods=('GET', 'POST'))
def get_data_weight():
    if request.method == 'POST':
        weight_export()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/food_export", methods=('GET', 'POST'))
def get_data_food():
    if request.method == 'POST':
        food_export()

        return redirect("/")
    else:
        return render_template("export.html")

@app.route("/exercise_export", methods=('GET', 'POST'))
def get_data_exercise():
    if request.method == 'POST':
        exercise_export()

        return redirect("/")
    else:
        return render_template("export.html")