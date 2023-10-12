import socket
import signal
import sys
import json
import re

# define the server's IP and port
HOST = "127.0.0.1"
PORT = 8019

# create a socket object ip4, tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the specified host and port
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen(5)
print(f"[*] Listening as {HOST}:{PORT}")


# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


# function to handle clients' requests
def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    with open('products.json', 'r') as file:
        products_json = json.load(file)

    cnt = 1

    if path == '/':
        response_content = '<h2>Main page</h2>'
        response_content += '<a href="/product">Products</a><br></br>'
        response_content += '<a href="/about">About</a><br></br>'
        response_content += '<a href="/contacts">Contacts</a>'
    elif path == '/about':
        response_content = '<h2>About</h2>'
    elif path == '/contacts':
        response_content = '<h2>Contacts</h2>'
    elif path == '/product':
        response_content = '<h2>Product</h2>'
        for item in products_json:
            response_content += '<a href="/product/' + str(cnt) + '">'+item["name"]+'</a> <br></br>'
            cnt += 1
    elif re.match('/product/\d+',path):

        list = path.split('/')
        index =int(list[2]) -1

        if(index >= len(products_json)):
            response_content = '<h1>404 Not Found</h1'
        else:
            name = products_json[index]['name']
            price = products_json[index]['price']
            description = products_json[index]['description']
            author = products_json[index]['author']

            response_content = '<h1>'+name+'</h1>'
            response_content += '<h4>' + str(price) + '</h4>'
            response_content += '<p>' + description + '</p>'
            response_content += '<p>' + author + '</p>'

    else:
        response_content = '<h1>404 Not Found</h1'
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    client_socket.close()


while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        # Handle the client's request in a separate thread
        handle_request(client_socket)
    except KeyboardInterrupt:
        pass