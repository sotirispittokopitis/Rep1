import socket
import json
import binascii
import os
# code from:
# https://realpython.com/python-sockets/
# (further referencing required)
import os
import socket
import time

def send_file(filename, conn):
    file_size = os.path.getsize(filename)
    conn.sendall(f"{file_size}\n".encode())
    time.sleep(0.5)
    with open(filename, 'rb') as f:
        conn.sendall(f.read())

def start_client(files_to_send):
    part1 = socket.AF_INET
    part2 = socket.SOCK_STREAM
    with socket.socket(part1, part2) as server:
        server.bind(('127.0.0.1', 65432))
        for filename in files_to_send:
            send_file(filename, server)
        print("All files sent")

if __name__ == "__main__":
    file1 = "../task_3/circuit/proof.json"
    file2 = "../task_3/circuit/public.json"
    file3 = "../task_3/circuit/verification_key.json"

    files = [file1, file2, file3]
    start_client(files)





