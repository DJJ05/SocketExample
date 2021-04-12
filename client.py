import socket
import sys
import threading

PORT = 8999
HEADER = 128
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '192.168.0.27'
ADDR = (SERVER, PORT)


def input_thread():
    while True:
        msg = input()
        if not len(msg) > 0:
            continue
        send(msg)
        if msg == DISCONNECT_MESSAGE:
            sys.exit()


def send(msg: str):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

thread = threading.Thread(target=input_thread)
thread.start()

try:
    client.connect(ADDR)
except ConnectionRefusedError:
    print('[ERROR] Server not online...')
    sys.exit()

while True:

    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        try:
            msg_length = int(msg_length)
        except:
            ...
        else:
            msg = client.recv(msg_length).decode(FORMAT)
            print(f'[MSG] {msg}')
