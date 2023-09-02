
import socket
import subprocess
import os
# code from:
# https://realpython.com/python-sockets/
# idea for subprocess:
# https://earthly.dev/blog/python-subprocess/#:~:text=To%20run%20an%20external%20command%20within%20a%20Python%20script%2C%20use,function%20returns%20a%20CompletedProcess%20object.

import os
import socket

HOST = "127.0.0.1"
PORT = 65432

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # create directory if it doesn't exist
            directory = '../new2/proof_Validation_Files'
            if not os.path.exists(directory):
                os.makedirs(directory)
            for i in range(3):
                # receive the file size followed by a newline character
                file_size = int(conn.recv(4096).decode().strip())
                # receive the file
                file_data = conn.recv(file_size)
                # save the file in the directory
                with open(f'{directory}/file{i+1}.json', 'wb') as f:
                    f.write(file_data)
                print(f"File {i+1} received")

            file5 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/node"
            file1 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/snarkjs"
            file2 = "../new2/proof_Validation_Files/file3.json"
            file3 = "../new2/proof_Validation_Files/file2.json"
            file4 = "../new2/proof_Validation_Files/file1.json"
            # snarkjs groth16 verify verification_key.json public.json proof.json
            output1 = subprocess.call([file5, file1, "g16v", file2, file3, file4])
            if output1 == 0:
                print("The command is valid!")
            else:
                print("We have encountered an issue!")

if __name__ == "__main__":
    start_server()













# def start_server():
#     # https://stackoverflow.com/questions/1681208/python-platform-independent-way-to-modify-path-environment-variable
#     os.environ["PATH"] += os.pathsep + "../Task_Part_3/circuit"
#     part1 = socket.AF_INET
#     part2 = socket.SOCK_STREAM
#     with socket.socket(part1, part2) as server:
#         server.bind(('127.0.0.1', 65432))
#         server.listen()
#         print('Waiting for a connection...')
#         conn, addr = server.accept()
#         with conn:
#             print("Received:")
#             while True:
#                 data = conn.recv(4096)
#                 if not data:
#                     break
#                 conn.sendall(data)
#             # ------
#             file5 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/node"
#             file1 = "/Users/sotirispittokopitis/.nvm/versions/node/v14.21.3/bin/snarkjs"
#             file2 = "../Task_Part_3/circuit/verification_key.json"
#             file3 = "../Task_Part_3/circuit/public.json"
#             file4 = "../Task_Part_3/circuit/proof.json"
#             # ------
#             output1 = subprocess.call([file5, file1, "g16v", file2, file3, file4])
#             if output1 == 0:
#                 print("The command is valid!")
#             else:
#                 print("We have encountered an issue!")
#
# if __name__ == "__main__":
#     start_server()