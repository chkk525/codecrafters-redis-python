# Uncomment this to pass the first stage
import socket
import threading


def send_pong(client_socket):
    while True:
        messages = client_socket.recv(1024).decode().split('\r\n')
        # -> ['*2', '$4', 'echo', '$5', 'world', '']

        for i, message in enumerate(messages):
            if message.lower() == 'ping':
                client_socket.send(b"+PONG\r\n")
            if message.lower() == 'echo':
                next_message = messages[i+2]
                # Interpolate next message into a binary value to send.
                client_socket.send(f"+{next_message}\r\n".encode())
            else:
                pass


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=send_pong, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    main()
