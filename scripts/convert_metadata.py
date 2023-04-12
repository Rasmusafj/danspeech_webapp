import sqlite3
import pandas as pd

def main():
    # Create your connection.
    connection = sqlite3.connect('../db.sqlite3')

    df = pd.read_sql_query("SELECT * FROM CoRal_recording", connection)

    # Close the connection
    connection.close()

    # change file extension from .webm to .wav
    df['recorded_file'] = df['recorded_file'].str.replace('.webm', '.wav')

    # Remove all rows where recorded file does not contain "_"
    df = df[df['recorded_file'].str.contains("_")]

    # Get the oldest recording by experiment_start_time
    df.experiment_start_time = pd.to_datetime(df.experiment_start_time)
    experiment_start_time = str(df.sort_values(by=['experiment_start_time']).experiment_start_time[1])

    # Save the dataframe to a csv file
    df.to_csv(f'../metadata_{experiment_start_time}.csv', index=False)   


if __name__ == '__main__':
    main()