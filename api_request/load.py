from extract import return_dataframe, get_access_token
from transform import Data_Quality, Transform_df
from datetime import datetime
import datetime
import psycopg2
from psycopg2.extras import execute_values

def connect_to_db():
    print("Connecting to the PostgresSQL database...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port = 5432,
            dbname = "airflow",
            user = "airflow",
            password= "airflow"
        )
        return conn
    except psycopg2.Error as e:
        print("Database connection failed: {e}")
        raise

def create_table_my_played_tracks(conn):
    print("creating my_played_tracks table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.my_played_tracks(
                id SERIAL PRIMARY KEY,
                song_name VARCHAR(200),
                artist_name VARCHAR(200),
                played_at VARCHAR(200),
                timestamp VARCHAR(200),
                inserted_at TIMESTAMP DEFAULT NOW()
            )
            """)
        conn.commit()
        print("my_played_tracks table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create my_played_tracks table: {e}")
        raise

def create_table_fav_artist(conn):
    print("creating fav_artist table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS int;
            CREATE TABLE IF NOT EXISTS int.fav_artist(
                timestamp VARCHAR(200),
                ID VARCHAR(200),
                artist_name VARCHAR(200),
                count VARCHAR(200),
                CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
                       )
            """)
        conn.commit()
        print("fav_artist table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create fav_artist table: {e}")
        raise

def insert_my_played_tracks(conn, data):
    print("Inserting my recently played tracks")
    try:
        cursor = conn.cursor()
        data['inserted_at'] = datetime.datetime.now()
        values = list(data[['song_name', 'artist_name', 'played_at', 'timestamp', 'inserted_at']].itertuples(index=False, name=None))
        sql = """
            INSERT INTO raw.my_played_tracks(
                song_name,
                artist_name,
                played_at,
                timestamp,
                inserted_at
            ) VALUES %s
        """

        execute_values(cursor, sql, values)
        conn.commit()
        print("Data successfully inserted")
    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")

def insert_fav_artist(conn, data):
    print("Inserting fav artist")
    try:
        cursor = conn.cursor()
        values = list(data[['timestamp', 'ID', 'artist_name', 'count']].itertuples(index=False, name=None))
        sql = """
            INSERT INTO int.fav_artist(
                timestamp,
                ID,
                artist_name,
                count
            ) VALUES %s
        """

        execute_values(cursor, sql, values)
        conn.commit()
        print("Data successfully inserted")
    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")

def main():
    try:
        get_access_token()
        data = return_dataframe()
        conn = connect_to_db()
        create_table_my_played_tracks(conn)
        create_table_fav_artist(conn)
        insert_my_played_tracks(conn,data)
        #run below commands if you want to run transformations and clean up in python
        # Data_Quality(data)
        # Transformed_df=Transform_df(data) 
        # insert_fav_artist(conn,Transformed_df)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

main()