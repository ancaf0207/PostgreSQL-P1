import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import datetime as dt




def process_song_file(cur, filepath):
    
    """
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """
    This procedure processes a log file (logs of playing songs) whose filepath has been provided as an arugment.
    A. It extracts the timestamp information in order to store it into the time table.
    Also, it extracts from this timestamp the hour, day, week, month, year 
    and weekday - also stored in the time table.
    
    B. It extracts the user information in order to store it into the user table.
    
    C. It extracts the event information in order to store it into the songplay table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the log file
    """ 
    
    # open log file
    df =  pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    #A
    # convert timestamp column to datetime
    df['ts']=pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
   
    t = df[['ts']]
    time_df = t.copy(deep=True)
    time_df['hour'] = time_df['ts'].dt.hour 
    time_df['day'] = time_df['ts'].dt.day 
    time_df['week'] = time_df['ts'].dt.week 
    time_df['month'] = time_df['ts'].dt.month
    time_df['year'] = time_df['ts'].dt.year
    time_df['weekday'] = time_df['ts'].dt.weekday
    
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
    
    #B. 
    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    #C.
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    This function identifies all files in a specific filepath 
    and prints the no of files.
    
    Then, iterates through the files from the filepath and executes a function 
    that takes as argument the connection and each of the files.
    
    INPUTS:
    * cur the cursor variable
    * conn the connection variable
    * filepath the file path to the song or log file
    * func the function that will be executed for each file
    
    """
    
    
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    
    """
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Executes the data processing for the song data source.
    
    - Executes the data processing for the log data source.
    
    - Finally, closes the connection. 
    """
    
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()