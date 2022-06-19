

## **Context and purpose:**


*A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.*

*The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.*


The key word of out assignment and the Sparkify goal is the **ability of doing analytics**.
For this to be achieved the best option is to use a relational database. 
This is because the relational databases have the advantages that we are looking for:


    - the ability to do JOINS across tables
    - the ability to do aggregations and analytics
    - the flexibility in changing the queries as we progress with the analytics process.


When you do analytics you end up finding correlation you would not intuitively spot, so the flexibility a relational database offers.

## **Design and execution:**

The data available for Sparkify was stored in .json format in 2 repositories:

    *Song Dataset:* metadata about a song and the artist of that song.
    *Log Dataset: log files for events representing a song play.


For the Sparkify project, their data was re-structured in a star schema:


**Fact Table**
This contains then actual metric of the business: the event of playing a song.

songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**
These are detailed description of the 'entities' that participate in the event of playing a song (artist, song, user)

users - users in the app: user_id, first_name, last_name, gender, level
song - songs in music database: song_id, title, artist_id, year, duration
artist - artists in music database: artist_id, name, location, latitude, longitude
time - timestamps of records in songplays broken down into specific units: start_time, hour, day, week, month, year, weekday


The artist and song tables were created extracting data from the Song dataset
The users and time tables were created extracting data from the Log dataset. For the time table, extraction of year, month, etc. from the timestamp was also performed.
The fact table (songplays) had most of the data pulled from the Log dataset, except for the song id and artist id which were extracted from the songs dataset.

# **Project files and structure**

The project consists of the following **files**:

    A. sql_queries.py
The sql_queries.py contains:
    1. the SQL syntax for the creation and deletion of each of the tables described above (**x_table_drop**)
    2. the SQL syntax for inserting data into the tables(**x_table_insert**);
    3. a query that extracts the song and artist ids from the artist and songs tables in order to insert them in the songplays table (**song_select**).

These queries are referenced in the main script we use to run the code from the console:
    
     B. create_tables.py

This script was provided in the materials and it references the queries from sql_queries.py, creating a main function that executes: 
    1. creating or re-creating the database
    2. re-creating the connection and cursor for the database
    3. re-creation of the tables
    
    C. etl.ipynb

This is the working notebook for the design of the ETL process.
It includes the step by step process of extracting the data from the JSON files, altering it in order to get it into the proper shape for insertion in the database (shaping the data as data frames and arrays, adjusting the data type, extracting components of date/time) and finally inserting the data in the tables of the database.

The process is also translated in the script we use to run the ETL code from the console:

    D. etl.py
    
Part of the script was provided at the beginning of the project. The file was finished with the code lines used in the etl.ipynb.

    E. test.ipynb
The notebook was provided in order to test the database/table creation and insertion.
I included at the end the file some example queries an analyst might run in order to explore the data.
For instance: which are the top 5 most played songs or artist, top song played in a specific month, no of plays by user subscription.

    and F. the readme.md.
    
    
**Running the scripts:**


    1. Create the database and tables:
    > Open a new terminal;
    > write in the console: python3 create_tables.py and press Enter
    2. Check if the database and tables have been created.
    > open the test.ipynb and run all cells
    You should see the headers for all tables. The analysis queries should return no results.
    > shut down the kernel (otherwise the ETL won't run, because the DB will be busy)
    3. Run the ETL:
    >  write in the console: python3 etl.py and press Enter
    4. Check if the data has been inserted in the table and the user/analyst queries
    > open the test.ipynb and run all cells
    You should see the headers + 5 rows of data for all tables. The analysis queries should show at least 1 row of data.
    > shut down the kernel in case you want to re-run the process
    
    
    If you want to follow the ETL process step by step, you can run the etl.ipynb notebook. 
    However, take into account that you will be running the scripts in the same database as the .py - so you might get confusing results in the analysis queries.
    Therefore, I advise you to always re-run the create_tables.py script before each ETL run (whether .py or .ipynb).
