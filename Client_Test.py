"""
This is the Client for the test, in addition im use UDP protocol.
"""
from socket import *
import time

SERVER_ADDRESS = ('127.0.0.1', 55556)

# create a UDP socket
with socket(AF_INET, SOCK_DGRAM) as s:
    print(f' Connecting to the server, ip: {SERVER_ADDRESS[0]} port: {SERVER_ADDRESS[1]}')

    while True:
        print('The Server Is Loading......')
        time.sleep(5)
        text = input('Please choose one of the following stations id: (123, 456, 999): ')

        if text == '123':
            with open('status1.txt', 'r') as f:
                station_id = str(f.readline())
                alarm1 = str(f.readline())
                alarm2 = str(f.readline())
                alarm3 = str(f.readline())

        elif text == '456':
            with open('status2.txt', 'r') as f:
                station_id = str(f.readline())
                alarm1 = str(f.readline())
                alarm2 = str(f.readline())
                alarm3 = str(f.readline())

        elif text == '999':
            with open('status3.txt', 'r') as f:
                station_id = str(f.readline())
                alarm1 = str(f.readline())
                alarm2 = str(f.readline())
                alarm3 = str(f.readline())
        else:
            print("Error: Invalid Input, The File Is Not Found \nPlease Try Again...")
            continue

        data = station_id.encode()
        data = data + alarm1.encode('utf-8')
        data = data + alarm2.encode('utf-8')
        data = data + alarm3.encode('utf-8')

        s.sendto(data, SERVER_ADDRESS)
        print(data.decode('utf-8'))

        try:
            data, address = s.recvfrom(1024)
            print(data.decode())

        except OSError:
            print("Error: Failed to receive data from server.")
        continue
