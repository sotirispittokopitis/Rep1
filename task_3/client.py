import socket
import json
import binascii
import os
# code from:
# https://realpython.com/python-sockets/

import os
import socket
import time

def send_file(filename, conn):
    # get the file size
    file_size = os.path.getsize(filename)
    # send the file size followed by a newline character
    conn.sendall(f"{file_size}\n".encode())
    time.sleep(0.5)
    # send the file data
    with open(filename, 'rb') as f:
        conn.sendall(f.read())

def start_client(files_to_send):
    HOST = "127.0.0.1"
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        for filename in files_to_send:
            send_file(filename, s)
        print("All files sent")

if __name__ == "__main__":
    file1 = "../new2/circuit/proof.json"
    file2 = "../new2/circuit/public.json"
    file3 = "../new2/circuit/verification_key.json"

    files = [file1, file2, file3]
    start_client(files)





