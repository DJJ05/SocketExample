import socket
import threading

PORT = 8999
SERVER = '192.168.0.27'
ADDR = (SERVER, PORT)
HEADER = 128
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
CLIENTS = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def input_thread():
    while True:
        msg = input()
        if not len(msg) > 0:
            continue
        if msg.split(' ')[0] not in CLIENTS:
            print('[ERROR] Invalid client')
            continue
        send(CLIENTS[msg.split(' ')[0]], ' '.join(msg.split(' ')[1:]))


def send(conn, msg: str):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)
    except ConnectionResetError:
        CLIENTS.pop(f'{addr[0]}:{addr[1]}')
        print(f'[ERROR] {addr[0]}:{addr[1]} disconnected')


def handle_client(conn, addr):
    connected = True

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
        except ConnectionResetError:
            connected = False
            CLIENTS.pop(f'{addr[0]}:{addr[1]}')
            print(f'[ERROR] {addr[0]}:{addr[1]} disconnected')
        if msg_length:
            try:
                msg_length = int(msg_length)
            except:
                ...
            else:
                try:
                    msg = conn.recv(msg_length).decode(FORMAT)
                except ConnectionResetError:
                    connected = False
                    CLIENTS.pop(f'{addr[0]}:{addr[1]}')
                    print(f'[ERROR] {addr[0]}:{addr[1]} disconnected')

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    CLIENTS.pop(f'{addr[0]}:{addr[1]}')
                    print(f'[ERROR] {addr[0]}:{addr[1]} disconnected')
                else:
                    print(f'[MSG] {addr[0]}:{addr[1]}: {msg}')

    conn.close()


def start():
    server.listen()
    print(f'[STARTED] {SERVER}')

    thread = threading.Thread(target=input_thread)
    thread.start()

    while True:
        conn, addr = server.accept()
        CLIENTS[f'{addr[0]}:{addr[1]}'] = conn

        print(f'[NEW] {addr[0]}:{addr[1]}')
        print(f'[ACTIVE] {threading.activeCount()-1}')

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print('[STARTING] Server starting...')
start()
