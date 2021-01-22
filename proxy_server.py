"""
CMPUT404 Winter 2021 Lab 2
Gengyuan Huang

a simple proxy server app for proxy_client.py
it send request from client to google.com
and forward the respond from google.com to client 
"""

import socket as sk
import time
from multiprocessing import Process

# properties and parameters of the proxy_server.py
HOSTNAME_GOOGLE = "www.google.com"
NUM_BACKLOG = 2
CLIENT_ADDR = ("", 8002)

def log(msg_str):
    # print to log
    print("{:.3f}".format(time.time()), "-", msg_str)

def init_listen_socket(addr):
    # init socket to listen on given port and addr
    # set proper socket options
    # bind() socket with addr
    # listen() on socket
    # create socket
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(NUM_BACKLOG)
    log("Server listening on port {0}".format(addr[1]))
    return s

def close_socket(socket):
    # close socket conenction
    socket.close()
    log("Socket closed")

def send_request(socket, rqst):
    # send request to socket
    # request must be encoded in UTF-8
    socket.sendall(rqst)

def recv_alldata(socket):
    # accepting data until no more left
    buffer_size = 1024
    data = b""      # data in bytes
    while True:
        buffer = socket.recv(buffer_size)
        if buffer:
            data += buffer
        else:
            break
    return data

def recv_fromclient(client_socket, client_ip_port):
    # recv all data from client
    buffer_size = 1024
    data = b""      # data in bytes
    while True:
        buffer = client_socket.recv(buffer_size)
        if buffer:
            data += buffer
        else:
            break
    log("All data from client {0} at port {1} received".format(client_ip_port[0], client_ip_port[1]))
    return data

def reply_toclient(client_socket, client_ip_port, data):
    # sent data to client
    client_socket.sendall(data)
    log("Google's respond sent to client {0} at port {1}".format(client_ip_port[0], client_ip_port[1]))

def close_client(client_socket, client_ip_port):
    client_socket.close()
    log("Connection to client {0} at port {1} closed".format(client_ip_port[0], client_ip_port[1]))

def get_socket_to_google():
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.connect((sk.gethostbyname(HOSTNAME_GOOGLE), 80))
    return s

def handle_client(client_socket, client_ip_port):
    # handle one client
    log("Connection to client {0} at port {1} established".format(client_ip_port[0], client_ip_port[1]))
    # time.sleep(100)   # uncomment this line for testing multithreading
    
    socket_google = get_socket_to_google()                          # open a socket to google.com
    data = recv_fromclient(client_socket, client_ip_port)           # get request from client

    send_request(socket_google, data)                               # send client request to google.com
    socket_google.shutdown(sk.SHUT_WR)

    response = recv_alldata(socket_google)                          # get response from google.com
    reply_toclient(client_socket, client_ip_port, response)         # sent response to client
    client_socket.shutdown(sk.SHUT_RDWR)

    socket_google.close()                                           # close socket to google
    close_client(client_socket,  client_ip_port)                    # close socket to client
    

def main():
    try:
        # init server listening socket
        socket = init_listen_socket(CLIENT_ADDR)
        # server will continue run forever untill interrupt
        while True:
            client_socket, client_addr = socket.accept()            # wait for connection
            p = Process(target=handle_client, args=(client_socket, client_addr,))
            p.daemon = True                                         # prevent zombies
            p.start()
    except:
        # for simplicity of this assignment
        # very limited error checking
        log("Error, or user interrupt")

    finally:
        close_socket(socket)

main()