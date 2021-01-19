#!/usr/bin/env python3
import socket, sys

# Creates a socket object with the default arguments
def create_tcp_socket():
   try:
      # first arg specifies types of addresses (IPv4 for AF_INET)
      # second arg specifies socket type (TCP for SOCK_STREAM)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   except (socket.error, msg):
      print("Failed to create socket.")
      sys.exit()
   return s

# Get the IP address of the given host address
def get_remote_ip(host):
   try:
      remote_ip = socket.gethostbyname(host)
   except socket.gaierror:
      print("Hostname could ont be resolved. Exiting")
      sys.exit()
   return remote_ip

# Sends a payload using the given socket (assumes connection is established)
def send_data(serversocket, payload):
   try:
      serversocket.sendall(payload.encode())
   except socket.error:
      print("Send failed. Exiting.")
      sys.exit()

def main():
   try:
      # connection info
      host = "localhost"
      port = 8013
      payload = "GET  / HTTP/1.0\r\nHost: {}\r\n\r\n".format(host)
      buffer_size = 4096

      # create a socket object
      s = create_tcp_socket()

      # get the IP address of the host
      remote_ip = get_remote_ip(host)

      # attempt to connect to the host
      s.connect((remote_ip, port))

      # send our payload using the socket
      send_data(s, payload)

      # shut down the send functionality of our socket
      s.shutdown(socket.SHUT_WR)

      # full_data is forced to be the bytes type (empty)
      full_data = b""
      while True:
         # gather up to buffer_size data
         data = s.recv(buffer_size)
         # when we have no more data to collect, break out of the loop
         if not data:
            break
         # append up to buffer_size data
         full_data += data
      # print everything we received
      print(full_data)
   except Exception as e:
      # print general error on unexpected failure
      print(e)
   finally:
      # clean up our connection on success or failure
      s.close()

if __name__ == "__main__":
   main()
