import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 12349

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

# Create a dictionary to store clients and their associated rooms
clients_list = {}

def handle_client(client_socket, client_address):
    print(f"Connection accepted from {client_address}")

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break

        message_json = json.loads(message)
        message_type = message_json.get('type', '')

        if message_type == 'connect':
            # Handle connection request and send acknowledgment
            client_name = message_json['payload']['name']
            room_name = message_json['payload']['room']
            print(f"{client_name} connected to {room_name}")

            info_connect_json = {
                "type": "connect_ack",
                "payload": {
                    "message": "Connected to the room."
                }
            }
            client_socket.send(json.dumps(info_connect_json).encode('utf-8'))

            # Store the client's room association
            clients_list[client_socket] = room_name

            # Send previous messages in the room to the new client
            for msg_socket, msg_room in clients_list.items():
                if msg_socket != client_socket and msg_room == room_name:
                    msg_socket.send(json.dumps(message_json).encode('utf-8'))

        elif message_type == 'message':
            sender = message_json['payload']['sender']
            room = clients_list[client_socket]
            text = message_json['payload']['text']
            print(f"Received from {sender} in {room}: {text}")

            # Broadcast the message to clients_list in the same room
            for msg_socket, msg_room in clients_list.items():
                if msg_socket != client_socket and msg_room == room:
                    msg_socket.send(json.dumps(message_json).encode('utf-8'))

    del clients_list[client_socket]
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
