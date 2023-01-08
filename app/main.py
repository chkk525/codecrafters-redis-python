import socket
import threading
import time

# Expiry
# In this stage, you'll need to support setting a key with an expiry. The expiry is provided using the "PX" argument to the SET command.
# The tester will first send a SET command with an expiry, like this: SET <key> <value> PX <expiry>.
# Then, it will send a GET command to retrieve the value, like this: GET <key>.

# If the key has expired, the tester will expect a Null value as the response. Read about "Null Bulk Strings" here to know how to send a Null value.
# https://redis.io/docs/reference/protocol-spec/#resp-bulk-strings
# Null is represented as: "$-1\r\n"


data = {}


def response(client_socket):
    while True:
        messages = client_socket.recv(1024).decode().split('\r\n')

        # pass if messages is empty or the first element is blank
        if messages and messages[0]:

            n = int(messages[0].replace('*', ''))
            for i in range(2, n*2 + 1, 2):
                v = messages[i].lower()
                if v == 'ping':
                    # Return PONG
                    client_socket.send(b"+PONG\r\n")
                elif v == 'echo':
                    # Return the argument
                    argument = messages[i+2].lower()
                    client_socket.send(f"+{argument}\r\n".encode())
                elif v == 'set':
                    # Store the provided key/value
                    key = messages[i+2]
                    value = messages[i+4]

                    # Check if the message contains expire time.
                    # Set None if no PX command found.
                    try:
                        if messages[i+6].lower() == 'px':
                            ttl = int(messages[i+8])
                            milliseconds = int(round(time.time() * 1000))
                            valid_until = milliseconds + ttl
                        else:
                            valid_until = None
                    except IndexError:
                        valid_until = None

                    data[key] = {
                        "value": value,
                        "valid_until": valid_until
                    }

                    client_socket.send(b"+OK\r\n")

                elif v == 'get':
                    key = messages[i+2]
                    stored_values = data[key]
                    value = stored_values['value']
                    valid_until = stored_values['valid_until']
                    now = int(round(time.time() * 1000))

                    if valid_until is None or now <= valid_until:
                        client_socket.send(f"+{value}\r\n".encode())
                    else:
                        client_socket.send(b"$-1\r\n")
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
