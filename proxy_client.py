"""
CMPUT404 Winter 2021 Lab 2
Gengyuan Huang

a simple client app for procy_server.py
"""

import socket as sk

# properties and parameters of the proxy_client.py
REQUEST = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'     # the http request sent to proxy server
PROXY_ADDR = ('127.0.0.1',8002)                                 # proxy server ip address

def log(msg_str):
    # print to log
    print(msg_str)

def init_socket(addr):
    # init socket connection to given ipv4 addr
    # create socket
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.connect(addr)
    log("Socket connected to ip {0} at port {1}".format(addr[0], addr[1]))
    return s

def close_socket(socket):
    # close socket conenction
    socket.close()
    log("Socket closed")

def send_request(socket, rqst):
    # send request to socket
    # request must be encoded in UTF-8
    socket.sendall(rqst)
    log("Request sent to proxy server: {0}".format(rqst))

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
    log("All data received")
    return data

def main():
    try:
        # get data
        socket = init_socket(PROXY_ADDR)    # build socket to proxy server
        send_request(socket, REQUEST.encode())       # send request to proxy server
        socket.shutdown(sk.SHUT_WR)         # tell server no more data will be sent
        data = recv_alldata(socket)
        
        # print data
        print(data)

        # program normal termination
        close_socket(socket)

    except:
        # for simplicity of this assignment
        # very limited error checking
        log("Error")

main()