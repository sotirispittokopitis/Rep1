
import socket
import subprocess
import os

# code from:
# https://realpython.com/python-sockets/
# idea for subprocess:
# https://earthly.dev/blog/python-subprocess/#:~:text=To%20run%20an%20external%20command%20within%20a%20Python%20script%2C%20use,function%20returns%20a%20CompletedProcess%20object.


def start_server():
    part1 = socket.AF_INET
    part2 = socket.SOCK_STREAM
    with socket.socket(part1, part2) as server:
        server.bind(('127.0.0.1', 65432))
        server.listen()
        conn, addr = server.accept()
        with conn:
            directory = '../task_3/proof_Validation_Files'
            if not os.path.exists(directory):
                os.makedirs(directory)
            for i in range(3):
                file_size = int(conn.recv(4096).decode().strip())
                file_data = conn.recv(file_size)
                with open(f'{directory}/file{i+1}.json', 'wb') as f:
                    f.write(file_data)
                print(f"File {i+1} received")

            file2 = "../task_3/proof_Validation_Files/file3.json"
            file3 = "../task_3/proof_Validation_Files/file2.json"
            file4 = "../task_3/proof_Validation_Files/file1.json"
            # snarkjs groth16 verify verification_key.json public.json proof.json
            output1 = subprocess.call(['snarkjs', 'groth16', "verify", file2, file3, file4])
            if output1 == 0:
                print("The command is valid!")
            else:
                print("We have encountered an issue!")

if __name__ == "__main__":
    start_server()

