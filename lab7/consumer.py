import os  # For operating system related operations
import json  # For JSON operations
import pika  # For RabbitMQ integration
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For HTML parsing

# Function to parse product details from a given URL
def productDetailParser(url_scrap):
    # Get the HTML content from the provided URL
    html = requests.get(url_scrap)
    html_document = html.text

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_document, 'html.parser')
    data_dict = {}  # Dictionary to store extracted data

    # Find all elements with class 'm-value'
    m_value_elements = soup.find_all('li', class_='m-value')

    # Iterate through the elements and extract the key-value pairs to populate data_dict
    for element in m_value_elements:
        key_element = element.find('span', class_='adPage__content__features__key')
        value_element = element.find('span', class_='adPage__content__features__value')

        # If both key and value are found, extract and store them in data_dict
        if key_element and value_element:
            key = key_element.text.strip()
            value = value_element.text.strip()
            data_dict[key] = value

    # Generate the output file name based on the product's brand
    output_file_name = data_dict["Marcă"] + '  '  + str(id(data_dict)) + '.json'
    output_file_path = os.path.join('Parsed_Objects', output_file_name)  # Specify the directory path

    # Ensure the "Parsed_Objects" directory exists, if not, create it
    if not os.path.exists('Parsed_Objects'):
        os.makedirs('Parsed_Objects')

    # Write the extracted data to a JSON file
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=4, ensure_ascii=False)


# Set up RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Declare a queue with a random name
result = channel.queue_declare(queue='', durable=True)
queue_name = result.method.queue

# Bind the queue to the exchange
channel.queue_bind(exchange='logs', queue=queue_name)
print(' [*] Waiting for messages ... ')


# Function to handle incoming messages from RabbitMQ
def callback(ch, method, properties, body):
    # Print the received message
    print(f" [x] Received {body.decode()}")

    # Call the productDetailParser function with the received URL
    productDetailParser(f'{body.decode()}')

    # Print a message indicating the task is done
    print(" [x] Done")

    # Acknowledge the message is processed and remove it from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Set the prefetch count to 1 to ensure fair distribution of tasks among consumers
channel.basic_qos(prefetch_count=1)

# Set up a consumer to receive messages from the queue and invoke the callback function
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
