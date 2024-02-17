import re
from datetime import datetime

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/workout/")
def workout():
    return render_template("workout.html")


@app.route("/food/")
def food():
    return render_template("food.html")


@app.route("/weight/")
def weight():
    return render_template("weight.html")


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")