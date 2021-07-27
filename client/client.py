#!/usr/bin/python           # This is client.py file
import argparse
import socket               # Import socket module

parser = argparse.ArgumentParser(description='Izumi remote control')
parser.add_argument('-input',required=True, type=str,
                    help="the command")
# parser.add_argument('-port', dest="profile_name", required=True, metavar="FILE", type=str,
#                    help='path to a profile for setting up the pipeline')

try:
    args = parser.parse_args()
    command = args.input
    s = socket.socket()         # Create a socket object
    #host = socket.gethostname() # Get local machine name
    host = '127.0.0.1'
    port = 47193               # Reserve a port for your service.
    s.connect((host, port))
    s.sendall(command.encode("utf-8"))
    s.close()                     # Close the socket when done
except ConnectionRefusedError:
    print("ConnectionRefusedError")
    exit(1)