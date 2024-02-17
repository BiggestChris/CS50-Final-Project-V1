import re, os
from datetime import datetime

from flask import request

from app import db
    
# Help received from ChatGPT refining this function
def exercise():
    # TODO: Add Server-side checks on entries
    exercise_name = request.form.get("exercise")
    sets = []

    # Loop through all possible sets
    for i in ["one","two","three","four","five"]:       
        set_value = request.form.get(f"set-{i}")
        if set_value:
            sets.append(int(set_value))

    # Upload into SQL tables
    db.execute("INSERT INTO exercise (Exercise, SetOne) VALUES (?, ?)", exercise_name,
               sets[0])
    
    # Get the last inserted row ID (primary key)
    last_inserted_id = db.execute("SELECT last_insert_rowid()")[0]

    # Upload into SQL tables
    if sets[1]:
        db.execute("UPDATE exercise SET SetTwo = ? WHERE ID = ?", sets[1], last_inserted_id)
    if sets[2]:
        db.execute("UPDATE exercise SET SetThree = ? WHERE ID = ?", sets[2], last_inserted_id)
    if sets[3]:
        db.execute("UPDATE exercise SET SetFour = ? WHERE ID = ?", sets[3], last_inserted_id)
    if sets[4]:
        db.execute("UPDATE exercise SET SetFive = ? WHERE ID = ?", sets[4], last_inserted_id)