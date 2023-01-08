# Uncomment this to pass the first stage
import socket
import threading


def send_pong(client_socket):
    while client_socket.recv(1024):
        client_socket.send(b"+PONG\r\n")


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=send_pong, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    main()
