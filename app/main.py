# Uncomment this to pass the first stage
import socket
import threading


def response(client_socket):
    data = {}
    while True:
        messages = client_socket.recv(1024).decode().split('\r\n')

        if messages and messages[0]:
            n = int(messages[0].replace('*', ''))
            for i in range(2, n*2 + 1, 2):
                v = messages[i].lower()
                if v == 'ping':
                    client_socket.send(b"+PONG\r\n")
                elif v == 'echo':
                    argument = messages[i+2].lower()
                    client_socket.send(f"+{argument}\r\n".encode())
                elif v == 'set':
                    key = messages[i+2]
                    value = messages[i+4]
                    data[key] = value
                    client_socket.send(b"+OK\r\n")
                elif v == 'get':
                    key = messages[i+2]
                    client_socket.send(f"+{value}\r\n".encode())
                else:
                    pass


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=response, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    main()
