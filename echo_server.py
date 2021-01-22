"""
CMPUT404 Winter 2021 Lab 1
Gengyuan Huang

echo_server.py is provided on CMPUT404 eclass not written by me.
its main function is slightly modified by me to support multithreading
"""

#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def handle_connection(conn, addr):
    # this function is run by a sub process / thread
    # this function is written by Gengyuan Huang

    #recieve data, wait a bit, then send it back
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            p = Process(target=handle_connection, args=(conn,addr,))
            p.daemon = True
            p.start()
            
            


if __name__ == "__main__":
    main()
