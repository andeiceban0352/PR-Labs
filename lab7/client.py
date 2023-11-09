import socket
import threading
import json
from  time import sleep
HOST = '127.0.0.1'
PORT = 12349

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")  # Move this line to the beginning

# Prompt the user for their name and desired room
name_client = input("Enter client name: ")
room_id = input("Enter room ID: ")

# Create a "connect" type message for the initial connection
connect_message = {
    "type": "connect",
    "payload": {
        "name": name_client,
        "room": room_id
    }
}
# Send the "connect" message to the server
client_socket.send(json.dumps(connect_message).encode('utf-8'))


def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break

        message_json = json.loads(message)
        message_type = message_json.get('type', '')
        if message_type == 'message':
            sender = message_json['payload']['sender']
            text = message_json['payload']['text']
            print(f"{sender}: {text}")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    message_text = input("Enter a message ('exit' to quit): ")
    if message_text.lower() == 'exit':
        break

    message_json = {
        "type": "message",
        "payload": {
            "sender": name_client,
            "room": room_id,
            "text": message_text
        }
    }

    client_socket.send(json.dumps(message_json).encode('utf-8'))
client_socket.close()
