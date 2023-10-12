import socket
import threading
import json
import os

HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")  # Move this line to the beginning

# Prompt the user for their name and desired room
name_client = input("Enter your name: ")
room = input("Enter the room you want to connect: ")

# Create a "connect" type message for the initial connection
connect_message = {
    "type": "connect",
    "payload": {
        "name": name_client,
        "room": room
    }
}
# Send the "connect" message to the server
client_socket.send(json.dumps(connect_message).encode('utf-8'))


# receive the message
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            response_json = json.loads(message.decode('utf-8'))
            message_type = response_json.get('type', '')

            # check the message type
            if message_type == 'message':
                client_sender = response_json['payload']['client_sender']
                client_message = response_json['payload']['client_message']
                print(f"{client_sender}: {client_message}")
            elif message_type == 'notification':
                notification_message = response_json['payload']['message']
                print(f"Notification: {notification_message}")

        except UnicodeDecodeError:
            pass

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()


while True:
    message_input = input("Enter: message / download: / upload: / exit  : ")

    if message_input.lower() == 'exit':
        break

    # upload type of input
    if message_input.startswith('upload:'):
        file_path = message_input.split(': ')[1]
        if os.path.exists(file_path):
            response_json = {
                "type": "file",
                "payload": {
                    "path": f"upload: {file_path}"
                }
            }
            client_socket.send(json.dumps(response_json).encode('utf-8'))
        else:
            print(f"File {file_path} doesn't exist.")

    # download type of input
    elif message_input.startswith('download:'):
        response_json = {
            "type": "file",
            "payload": {
                "path": message_input
            }
        }
        client_socket.send(json.dumps(response_json).encode('utf-8'))

    #message type of input
    else:
        response_json = {
            "type": "message",
            "payload": {
                "client_sender": name_client,
                "room": room,
                "client_message": message_input
            }
        }
        client_socket.send(json.dumps(response_json).encode('utf-8'))

client_socket.close()