#!/usr/bin/env python3
import socket, time
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def handle_conn(conn):
   # collect sent data up to our BUFFER_SIZE
   full_data = conn.recv(BUFFER_SIZE)
   # wait before sending response and looping again
   time.sleep(0.5)
   # respond with whatever we were sent
   conn.sendall(full_data)
   # close the connection
   conn.close()

def main():
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

      # for q3
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      # bind the socket to our specified address
      s.bind((HOST, PORT))

      # set socket to listen mode so that it can accept connections
      # (argument is how many pending connections to sit on before refusing new ones)
      s.listen(2)

      # loop forever until program is shut down
      while True:
         # accept connection
         conn, addr = s.accept()
         print("Connected by", addr)

         p = Process(target=handle_conn, args=(conn,))
         p.daemon = True
         p.start()
         p.join()

if __name__ == "__main__":
   main()
