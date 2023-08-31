import socket
import json
import binascii
# code from:
# https://realpython.com/python-sockets/
def send(memo):
    part1 = socket.AF_INET
    part2 = socket.SOCK_STREAM
    with socket.socket(part1, part2) as server:
        server.connect(('127.0.0.1', 65432))
        server.sendall(memo.encode())
        print('The memo has been sent to the server!')

def read(file):
    with open(file, 'r') as f:
        fromJson = json.load(f)
        output = fromJson['memo']
        return output

# https://stackoverflow.com/questions/34687516/how-to-read-binary-files-as-hex-in-python
def make_memos():
    with open('../Task_Part_3/circuit/proof.json', 'rb') as f:
        hex1 = binascii.hexlify(f.read()).decode()
    # https://xrpl.org/transaction-common-fields.html#memos-field
    Memo1 = {
        "memo": hex1
    }
    with open('../Task_Part_3/circuit/public.json', 'rb') as f:
        hex2 = binascii.hexlify(f.read()).decode()
    # https://xrpl.org/transaction-common-fields.html#memos-field
    Memo2 = {
        "memo": hex2
    }
    with open('../Task_Part_3/circuit/verification_key.json',
              'rb') as f:
        hex3 = binascii.hexlify(f.read()).decode()
    # https://xrpl.org/transaction-common-fields.html#memos-field
    Memo3 = {
        "memo": hex3
    }
    with open('../Task_Part_3/memos_file/memo1.json', 'w') as f:
        json.dump(Memo1, f)

    with open('../Task_Part_3/memos_file/memo2.json', 'w') as f:
        json.dump(Memo2, f)

    with open('../Task_Part_3/memos_file/memo3.json', 'w') as f:
        json.dump(Memo3, f)

    print("The memos have been created")
    # ///////////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    make_memos()
    file1 = "../Task_Part_3/memos_file/memo1.json"
    file2 = "../Task_Part_3/memos_file/memo2.json"
    file3 = "../Task_Part_3/memos_file/memo3.json"
    memo_info1 = read(file1)
    send(memo_info1)
    memo_info2 = read(file2)
    send(memo_info2)
    memo_info3 = read(file3)
    send(memo_info3)


