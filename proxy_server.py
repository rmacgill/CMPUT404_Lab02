#!/usr/bin/env python3
import socket, sys, time

# some constants to make this easier
LOCAL_HOST = ""
LOCAL_PORT = 8013

REMOTE_HOST = "www.google.com"
REMOTE_PORT = 80

BUFFER_SIZE = 4096

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
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

      # for q3
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # bind the socket to our specified address
      s.bind((LOCAL_HOST, LOCAL_PORT))

      # set socket to listen mode so that it can accept connections
      # (argument is how many pending connections to sit on before refusing new ones)
      s.listen(3)

      # loop forever until program is shut down
      while True:
         # accept connection
         conn, addr = s.accept()
         print("Connected by", addr)

         # collect sent data up to our BUFFER_SIZE
         payload = conn.recv(BUFFER_SIZE)

         # wait before sending response and looping again
         time.sleep(0.5)

         remote_s = create_tcp_socket();
         remote_ip = get_remote_ip(REMOTE_HOST)
         remote_s.connect((remote_ip, REMOTE_PORT))
         send_data(remote_s, payload)
         remote_s.shutdown(socket.SHUT_WR)

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
         # respond with whatever we were sent from google
         conn.sendall(full_data)
         # close the connection
         conn.close()

if __name__ == "__main__":
   main()