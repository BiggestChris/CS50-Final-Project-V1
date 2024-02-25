import re, os
from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
import json



app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fitness.db")

# Import workout after defining db and app
from workout import exercise, weight_import, food_import, weight_export, food_export, exercise_export
from workoutobject import workout_list
workout_list_json = json.dumps(workout_list)


@app.route("/")
def home():
    return render_template("home.html")


# Help received from ChatGPT refining this function
@app.route("/workout", methods=('GET', 'POST'))
def workout():
    if request.method == 'POST':
        exercise()

        return redirect("/")
    else:
        return render_template("workout.html", workout_list=workout_list, workout_list_json=workout_list_json)



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