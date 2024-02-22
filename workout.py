import re, os
from datetime import datetime
import pandas as pd
import pygsheets

from flask import request
from sqlalchemy import create_engine

from app import db
    
# Help received from ChatGPT refining this function
def exercise():
    # TODO: Add Server-side checks on entries
    exercise_name = request.form.get("exercise")
    weights =[]
    sets = []
    numbers = ["one","two","three","four","five"]

    # Loop through all possible sets
    for i in numbers:       
        set_value = request.form.get(f"set-{i}-reps")
        set_weight = request.form.get(f"set-{i}-weight")
        if set_value:
            sets.append(int(set_value))
            weights.append(set_weight)

    # Upload into SQL tables
    db.execute("INSERT INTO exercise (Exercise) VALUES (?)", exercise_name)
    
    # Get the last inserted row ID (primary key)
    last_inserted_id = db.execute("SELECT last_insert_rowid()")[0]['last_insert_rowid()']

    # Upload into SQL tables
    # TODO: Error deriving from zero-indexing arrays and first numbers being "one" (suspected) - Fix
    for i in range(len(sets)):
        try:
            if sets[i]:
                db.execute("UPDATE exercise SET ? = ?, ? = ? WHERE ID = ?", f"Set{numbers[i].capitalize()}_Reps", sets[i], f"Set{numbers[i].capitalize()}_Weight", weights[i], last_inserted_id)
        except IndexError:
            pass

    return "success"

# Help received from ChatGPT refining this function
def weight_import():
    # Look for CSV file
    if 'weight_file' not in request.files:
        return 'No file part'
    file = request.files['weight_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        # Process the CSV file
        pass
    else:
        return 'Please upload a CSV file'


    # Read CSV file
    if file:
        df = pd.read_csv(file)

    # Transpose CSV file into SQL
    # TODO: Be able to upload multiple weight files without deleting prior data
    engine = create_engine("sqlite:///fitness.db")
    df.to_sql('weight', engine, if_exists='replace', index=False)
    engine.dispose()

    return "success"

# Taken using weight_import as a template
def food_import():
    # Look for CSV file
    if 'food_file' not in request.files:
        return 'No file part'
    file = request.files['food_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.csv'):
        # Process the CSV file
        pass
    else:
        return 'Please upload a CSV file'


    # Read CSV file
    if file:
        df = pd.read_csv(file)

    # Transpose CSV file into SQL
    # TODO: Be able to upload multiple weight files without deleting prior data
    engine = create_engine("sqlite:///fitness.db")
    df.to_sql('food', engine, if_exists='replace', index=False)
    engine.dispose()

    return "success"

# Help received from ChatGPT refining this function
def export():
    # Retrieve data from SQL table
    engine = create_engine("sqlite:///fitness.db")

    # TODO: Select tables
    for var in ['exercise', 'weight', 'food']:
        sql_query = f"SELECT * FROM {var}"
        df = pd.read_sql_query(sql_query, engine)

        # Define the file path for the CSV file
        csv_file_path = f'{var}.csv'

        # Export DataFrame to CSV file
        df.to_csv(csv_file_path, index=False)

        # Check if the file was created successfully
        if os.path.exists(csv_file_path):
            print(f"CSV file '{csv_file_path}' created successfully.")
        else:
            print("Failed to create CSV file.")

    # G-sheets authorisation
    # TODO: Need to load in JSON securely - having it in Repo and then uploading publicly created a security risk
        # json is now moved separately, but file location still in code which is a risk, repo moved to private for now until resolved
    gc = pygsheets.authorize(service_file=r'C:\Users\styli\OneDrive\Documents\Coding\CS50\CS50 - Final Project - Git\GSheets API\g-sheets-for-python-a3ee6cd4d658.json')

    # Create empty dataframe
    df2 = pd.DataFrame()

    # Open the google spreadsheet (this has the key from the Greg Burns Fitness Sheet)
    sh = gc.open_by_key('1F_6EtWT68BO2EfY_dErs-fNKWiEMCj497Hs0MnI-HsY')

    #select the Daily Tracker worksheet 
    wks = sh.worksheet_by_title('Daily Tracker')

    # TODO: Daily Tracker
        # Read Column C to pick up dates
    date_column = wks.get_col(3)
    # Above creates a list of values in the cells in that column

    # Need to compare to dates in Weight table
    dates = db.execute('SELECT [Time of Measurement], [Weight(kg)] FROM weight')
    # Above creates a list of dictionaries, with 'Time of Measurement' and 'Weight(kg)' as the keys in those dictionaries

    fresh_dates = []

    for x in dates:
        date_object = datetime.strptime((x['Time of Measurement']), "%m/%d/%Y, %H:%M:%S")
        formatted_date = date_object.strftime("%d/%m/%y")
        fresh_dates.append({'date': formatted_date, 'weight': x['Weight(kg)']})

    # Where they are matching - need to load in the weight into Column D
    for index, date in enumerate(date_column):
        # Ensure we skip the header row
        if index == 0:
            continue

        # Define the regex patterns
        pattern1 = r'^.{4}(\d{1}/\d{1}/\d{2})$'
        pattern2 = r'^.{4}(\d{1}/\d{2}/\d{2})$'
        pattern3 = r'^.{4}(\d{2}/\d{1}/\d{2})$'
        pattern4 = r'^.{4}(\d{2}/\d{2}/\d{2})$'

        match = re.match(pattern1, date) or re.match(pattern2, date) or re.match(pattern3, date) or re.match(pattern4, date)
        if match:
            # If the string matches the pattern
            # TODO: Fix error in how this is working - currently carrying over whole string
            extracted_part = match.group(1)
            # Extract the part representing the month
            day_part = extracted_part.split('/')[0]
            month_part = extracted_part.split('/')[1]
            # Check if the day or month part has only one digit
            if len(day_part) == 1:
                # Insert '0' before the single digit day
                extracted_part = '0' + extracted_part
            if len(month_part) == 1:
                # Insert '0' before the single digit month
                extracted_part = extracted_part[:3] + '0' + extracted_part[3:]

            # Iterate over fresh_dates to find a matching date
            for fresh_date in fresh_dates:              
                if extracted_part == fresh_date['date']:
                    # Update the weight in Column D
                    wks.update_value(f"D{index+1}", fresh_date['weight'])
                    break  # Break the loop once we find a match

        else:
            pass


    wks.update_value(f"D6", 'TEST')   
    # If multiple entries for one day - pick the earliest time




    # Update the first sheet with df, starting at cell - note (y,x) is format of set_dataframe coordinates.
    # So wks.set_dataframe(df2,(9,4)) will update cell Row 9, Column D (4))
    wks.set_dataframe(df2,(9,4))