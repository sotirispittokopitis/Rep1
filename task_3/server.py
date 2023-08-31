import socket
import subprocess
import os
# code from:
# https://realpython.com/python-sockets/
def start_server():
    # https://stackoverflow.com/questions/1681208/python-platform-independent-way-to-modify-path-environment-variable
    os.environ["PATH"] += os.pathsep + "../Task_Part_3/circuit"
    part1 = socket.AF_INET
    part2 = socket.SOCK_STREAM
    with socket.socket(part1, part2) as server:
        server.bind(('127.0.0.1', 65432))
        server.listen()
        print('Waiting for a connection...')
        conn, addr = server.accept()
        with conn:
            print("Received:")
            print(conn.recv(1024).decode())
            # ------
            file5 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/node"
            file1 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/snarkjs"
            file2 = "../Task_Part_3/circuit/verification_key.json"
            file3 = "../Task_Part_3/circuit/public.json"
            file4 = "../Task_Part_3/circuit/proof.json"
            # ------
            output1 = subprocess.call([file5, file1, "g16v", file2, file3, file4])
            if output1 == 0:
                print("The command is valid!")
            else:
                print("We have encountered an issue!")

if __name__ == "__main__":
    start_server()