# YOUR PROJECT TITLE
## Video Demo:  <URL HERE>
## Description:

### 1) Summary
This application has been created to solve specific pain points that I have with recording my nutrition and fitness data on a daily basis, and then being asked to transcribe that into a specific Google Sheet template by my Personal Trainer (who's also my Brother-in-Law).

### 2) Problem
My PT wants me to track my weight on a daily basis, my macronutrient consumption on a daily basis, and the exact weights and reps lifted in my workouts. When these are plugged into the G-sheet, he can then use them to monitor whether I am sticking to my goals, the outputs of them, and there are also graphs to showcase trends over time. Ultimately, it's about tracking this data so we can observe if the input actions we are taking are having the desired effect, or if things need to change.

The problem is that _it takes so long to transpose this data_ into the template. Sometimes it's taken up to 10 minutes to copy a single workout into it (and I do 5 of these a week on a good week!). What's even more frustrating is that I actually already have mobile apps to use to track my weight (Renpho, it automatically links to my scale with bluetooth to record my measurements) and food/macronutrient intake (MyFitnessPal, it contains a massive library of food produced by different suppliers and has the macronutrient data preloaded, so you just input what you've eaten and it knows exactly how many calories/protein/fat etc.). In practice, I'm defaulting to zero and not transposing this data due to the time involved - which means in practice I am missing out on the opportunity to action upon the meaningful information it provides.

For example, there were several weeks into my plan this year I wasn't actually dropping any weight and was unsure why. When I finally ran the data off the back of this app - it was apparent why, my calorie intake for those weeks Mon-Fri was within my targets, but I didn't record my food intake on those weekends. I realised in practice on those weekends when I decided not to track my food, I wound up consuming too much as a result and offsetting my calorie savings during the prior week.

So - I wanted to create an app that will automatically transpose all of this data that's currently being recorded in different places and formats and put it into this G-sheet template to remove this pain.

### 3) Solution
This application has a single use-case in mind, which is my own. As a result, I was able to make certain decisions that I wouldn't take if I was optimising for an app to be publicly consumed. For a few examples:
1. I hardcoded the G-sheet template into my code
2. There's only one user and password accepted by the auth function
3. For most of the form fields, I didn't include server-side checks

Breaking down the app I've created by functionality there's:
1. The ability to import Weight data as a .CSV that is exported from Renpho into an SQL database
2. The ability to import Food data as a .CSV that is exported from MyFitnessPal into an SQL database
3. The ability to record Workout data whilst a workout is being performed:
    - The workout plan my PT has prepared is pre-loaded, segmented into different days of the week
    - It has a set order, but can also show me the order I performed my last workout in, and the weights and reps I achieved for each of those exercises in my last workout
    - It allows me to record new exercises as well outside of the set plan
    - All of that workout data is recorded into an SQL database
4. The ability to export Weight/Food/Workout data into the exact cells in the G-sheet where they should go based on date etc.
5. Keeping the information in the SQL database, so that in the future as I find better ways to query the data then I can act upon it (so there are fields that currently aren't used in the G-sheet being recorded for that purpose)
6. And the intention is that recording workouts will be done on a mobile (specifically _my_ mobile) so I've optimised that page for mobile, and then the importing and exporting data functions to take place on a computer

> [!NOTE]
> The above features for logging workouts are because in practice, I can't always get on the equipment I want in the order I want in the gym - there's other people working out and if someone is using the equipment I want I need to be efficient with my time and do another exercise until it's available

### 4) Architecture
In terms of the architecture:
1. I've built the app itself in Flask using Python
2. I've connected it to an SQL database, to store all of the input data and to pull data for exporting into G-sheets
3. Flask renders HTML pages via Jinja templates that I've created
4. The workout.html page contains JavaScript, this is is so can dynamically update the page as the user moves through the different permutations of workout options to bring up relevant information for the workout they are about to perform
    - So in practice, I start my workout, select the day and exercise to perform, and it updates my placeholders with the weights and reps I hit last time - so I know that's what I should be aiming for this time as I perform that exercise
5. In moving this App into Production, it has been deployed on PythonAnywhere, where a MySQL server has been set up and is storing the db files

> [!NOTE]
> This project has been a really nice way to capp off CS50, as I've been able to use everything that's been covered by the syllabus excluding coding in C itself

### 5) Files and functions
Walkthrough of the files:

#### app.py:
This is the initial Flask application, and contains all the different routes - the db connection is declared here and then imported into workout.py (which will be detailed further down) and then workout.py is imported afterwards (this ensures the same connection is used across both files).

Flask Basic Auth has been used to protect the app itself. This is because I have been taught (by CS50 and other programming friends) to always assume a malicious actor would be trying to gain access to your app and do whatever they can with it. With bots trawling the internet prodding and poking whatever they can, I thought best to implement a base level of security as this is now deployed. The keys themselves are stored on PythonAnywhere.

This file then runs through all the relevant routes that can be taken:

1. home() - this is just the home screen
2. workout() - this loads the workout page, if a GET request is run then it runs the retrieve_workout() function from workout.py and loads it into a JSON, so this object can be imported into Javascript in workout.html. If a POST request, then it runs exercise() from workout.py, runs a quick server-side check on it, then lets the user know if there was an error or not through a redirect
3. food() - this renders a page whereby I can upload a .CSV file of my Food data. When POST is the method, it runs food_import() to load this into SQL
4. weight() - similar to food(), but for importing weight data from Renpho
5. export_page() - this is a single hub page used for exporting food/weight/workout data. When posting methods are used, different routes are run but the all end up with the same redirect back to export_page()
6. get_data_weight() - for a POST this will run weight_export() and load weight data into G-sheets
7. get_data_food() - same as above but will run food_export() and load food data into G-sheets
8. get_data_exercise() - same as above but will run exercise_export() and load exercise data into G-sheets
9. upload_error() - this will render a page that says an upload is failed. Currently only used for the server-side check on NULL entries in Set One of the Workout form

#### workout.py:
All the subfunctions call in the Flask routes are stored here:

1. exercise() - this takes all the form data filled in on a submitted form in workout.html, and then adds in some extra data that it captures (order of workouts etc.) and then uploads that into rows in the SQL database fitness.db in table new_exercise
2. weight_import() - this looks or an uploaded CSV file and then places that into the weight table in fitness.db
3. food_import() - same as above but for food data
4. weight_export() - this takes the Weight data in fitness.db and then transposes into the relevant tab in G-sheets. It has to find the relevant data for each weight row (and ensure it takes the first capture for a date), then it reformats the variables so they'll match those used in the G-sheets, and does comparisons to find the relevant dates in G-sheets and load in the weight data into the column
5. food_export() - is similar, except with this there are multiple columns to load into for the different macronutrient types
6. exercise_export() - similar to the above two, this is loading new_exercise table data from fitness.db into the G-sheet. Biggest difference here is that the structure of the G-sheet is into weeks rather than days, so there's a bit more cross-referencing to find the right cell to load the data into
7. retrieve_workout() - this pulls the last workout of each type from fitness.db for loading into workout.html as a JSON (this shows current targets etc. and are loaded in dynamically)

> [!IMPORTANT]
> On G-sheet imports: Currently all of these are calling the GoogleSheets API to load data into a single cell, after enough calls Google starts throttling calls, so this does take a while to complete. I need to refactor this at some point to load the data from the database into a 'range' and export all of that at once to reduce the number of calls.

#### workoutobject.py:
This stores the workout_list variable, which is the default workouts set by my PT. I've loaded these in as a static file as I'm the sole user, but if I ever looked to change workouts regularly or wanted to make available for other users, I'd need to change this so users could load in their own workout plans.

#### prod folders and local_dev folders:
These contained archived versions of app.py and workout.py from when I was switching between Local and Prod environment. When building in Local, I used SQLite and a local database in the folder, however for Prod a hosted MySQL database is used, and the code and file references are different as a result. I've kept these folders here just in case I ever recreate the Dev environment or need to go back and forth between Dev and Prod.

#### templates:
These house the html templates used to render the pages - using jinja templates and layout.html as the base template.

1. layout.html - This contains the Bootstrapp CSS links and other parts. A navbar has been created that will load at the top of every page to navigate the app, with the Jinja template then prepared for underneath.
2. error.html - The page will come up when there's an upload error with text explaining there's beeen an error
3. export.html - This page will render 3 buttons to choose whether to export Weight, Food, or Exercise info
4. food.html - This page allows selection and upload of the Food CSV
5. home.html - This is the default homepage
6. weight.html - This page allows selection and upload of the Weight CSV
7. workout.html - This page is for recording workout data, this is by far the most complex of the pages, as JavaScript is used to dynamically render information onto the page

#### workout.html (in detail):

**HTML Form** - Loads up a form asking for:
1. Date - as in day workout is being performed
2. Workout Day - the identifier of which workout is being undertaken
3. Exercise - there is a dynamically populated list of exercises that can be selected
4. Load metric - drop down of kg, lbs, bodyweight or other
5. Set data - for up to five sets data can now be entered, with the weight/load of the set and number of reps achieved
6. Notes - text area space to include any notes relevant to the workout performed

**JavaScript** - then we have JavaScript to dynamically populate the form for the user:

Variables - these are populated by form elements, or the WorkoutList and LastWorkout JSONs loaded in from the Flask App
            
Event listeners -
1. DOM CONTENT LOADED - Automatically populates Date with todays date, and sets the Workout Day and Exercise to the top selection
2. Workout Day change - When the workout day is changed, repopulates the options for exercises with those relevant for that day
3. Exercise change - When the exercise is changed, it updates Placeholders for the Set loads and reps from those recorded in the last workout performed of that type (from the JSON)
4. Other Option input - When the 'other exercise' field is populated, it ensures that the Exercise value is matched to it
5. updateExerciseOptions(SelectedWorkout) - This loads into Exercise change, and looks in WorkoutList to pull the relevant exercises for the WorkoutDay currently selected. It also renders the order of the exercises run last time this workout was performed.
6. updateExercisePlaceholders(SelectedExercise) - This pulls the relevant Set Loads and reps from LastWorkout and assigns them as Placeholders for the Workout/Exercise combo currently selected.
7. sort_workout_null_number(items, criteria) - This is utilised in other functions to sort workouts by Workout Day first, then the order of the exercise performed

#### 6) Known bugs









    