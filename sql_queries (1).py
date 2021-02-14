import psycopg2

# DROP TABLES

 
    
songplay_table_drop = "DROP table IF EXISTS songplay"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS song"
artist_table_drop = "DROP table IF EXISTS artist"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES


artist_table_create = """CREATE TABLE IF NOT EXISTS artist (artist_id varchar NOT NULL, 
                        name varchar, location varchar, latitude varchar, longitude varchar, 
                        PRIMARY KEY (artist_id));"""


song_table_create = """CREATE TABLE IF NOT EXISTS song (song_id varchar NOT NULL, 
                    title varchar, artist_id varchar NOT NULL, year int, duration float, 
                    PRIMARY KEY (song_id));"""


user_table_create = """CREATE TABLE IF NOT EXISTS users (user_id int NOT NULL,
                    first_name varchar,last_name varchar, gender varchar, level varchar,
                    PRIMARY KEY (user_id));"""



songplay_table_create = """CREATE TABLE IF NOT EXISTS songplay (songplay_id SERIAL,
                        start_time timestamp NOT NULL, user_id int NOT NULL,
                        level varchar, song_id varchar NOT NULL, 
                        artist_id varchar NOT NULL, 
                        session_id int, location varchar, user_agent varchar,
                        PRIMARY KEY (songplay_id));"""



time_table_create = """CREATE TABLE IF NOT EXISTS time (start_time timestamp NOT NULL, 
                        hour int, day int, 
                        week int, month int, year int, weekday int, 
                        PRIMARY KEY (start_time));"""




# INSERT RECORDS

songplay_table_insert = """INSERT INTO songplay (start_time, user_id, level,
                        song_id, artist_id, session_id, location, user_agent) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """

user_table_insert = """INSERT INTO users (user_id, first_name, last_name, gender, level)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO NOTHING"""

song_table_insert = """INSERT INTO song (song_id, title, artist_id, year, duration) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) DO NOTHING"""

artist_table_insert = """INSERT INTO artist (artist_id, name, location, latitude, longitude) 
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (artist_id) DO NOTHING"""


time_table_insert = """INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time) DO NOTHING"""


# FIND SONGS

song_select = ("""SELECT song_id, artist.artist_id FROM song JOIN artist 
                ON song.artist_id = artist.artist_id 
               WHERE song.title=(%s) AND artist.name=(%s) AND song.duration=(%s);""")



# QUERY LISTS


drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [artist_table_create, song_table_create, user_table_create, songplay_table_create, time_table_create]

