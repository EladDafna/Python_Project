import time
from socket import *
import datetime
import sqlite3

# Define the server address and buffer size
SERVER_ADDRESS = ('127.0.0.1', 55556)
BUFFER_SIZE = 1024

# Get the current date and time
last_date = datetime.datetime.now().strftime('%Y-%M-%d %H:%m')
print(last_date)

# connect to the sqlite3 database
with sqlite3.connect('database.sqlite3') as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS station_status ( 
    station_id INT, 
    last_date TEXT, 
    alarm1 INT, 
    alarm2 INT, 
    PRIMARY KEY(station_id) ); 
    """)
    conn.commit()

    # create a UDP socket
    with socket(AF_INET, SOCK_DGRAM) as s:

        # bind the socket to server address
        s.bind(SERVER_ADDRESS)
        print(f' The Server is running... {s.getsockname()[0]} {s.getsockname()[1]}')

        while True:
            try:
                new_data, new_client = s.recvfrom(BUFFER_SIZE)
            except OSError:
                continue

            try:
                station_id, alarm1, alarm2 = new_data.decode('utf-8').split()
            except ValueError:
                print("Error: Received data is not in utf-8 format")
                continue

            print(f'The new information received from the client is:'
                  f'\nstation_id:{station_id}'
                  f'\n alarm_1: {alarm1}'
                  f'\n alarm_2: {alarm2}'
                  )

            with conn:
                conn.execute('''
                                 INSERT OR REPLACE INTO
                                 station_status
                                 VALUES(?, ?, ?, ?)
                                 ''', (station_id, last_date, alarm1, alarm2))

            update_data_to_client = "The data is update, let's check it".encode('utf-8')
            print("send the update to the client....")
            time.sleep(2)
            try:
                s.sendto(update_data_to_client, new_client)
            except OSError:
                print("Error: Failed to send data from server.")
            continue
