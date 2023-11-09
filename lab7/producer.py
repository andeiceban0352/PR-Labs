# Import necessary libraries
from bs4 import BeautifulSoup  # For HTML parsing
import requests  # For making HTTP requests
import re  # For regular expressions
import pika  # For RabbitMQ integration

# Function to scrape car listings and return a list of links
def urlLinkExtractor(url_to_scrap, max_num_pag):
    car_links = []  # List to store extracted car links
    current_url = url_to_scrap
    # Get the HTML content from the provided URL
    html = requests.get(current_url)
    html_document = html.text

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_document, 'html.parser')
    current_page = soup.find('li', class_='current')  # Find the current page
    page_number = current_page.a.text  # Extract the page number
    # Check if the maximum number of pages is reached
    if int(page_number) > max_num_pag:
        return "max_num_page is reached"
    else:
        # Find all the anchor tags with "href" attribute starting with "/ro/" and "class" containing "js-item-ad"
        for link in soup.find_all('a', attrs={'href': re.compile("/ro/"), 'class': re.compile("js-item-ad")}):
            car_links.append("https://999.md" + link.get('href'))  # Append the complete link to the car_links list

        # Check if there is a next page link
        next_page_link = current_page.find_next('li').find('a') if current_page else None
        # If a next page link exists, extract and print the href attribute
        if next_page_link:
            next_page_url = "https://999.md" + next_page_link['href']
            urlLinkExtractor(next_page_url, max_num_pag)  # Recursively call the function with the next page URL
        else:
            print("No next page link found.")

    return car_links  # Return the list of extracted car links

# Establish a connection with RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# Extract car links from the specified URL and maximum number of pages
links = urlLinkExtractor('https://999.md/ro/list/transport/cars?hide_duplicates=no&applied=1&ef=290,260,6,5,4112,2029,1279&o_290_7=12900&r_6_2_from=&r_6_2_to=&r_6_2_unit=eur&r_6_2_negotiable=yes', 1)

# Publish each link to the RabbitMQ server
for link in links:
    message = link
    channel.basic_publish(
            exchange='logs',  # Specify the exchange name
            routing_key='',  # Set the routing key to an empty string
            body=message,  # Set the body of the message to the current link
            properties=pika.BasicProperties(  # Set the properties of the message
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # Ensure the message is persistent even if the RabbitMQ server restarts
            ))
    # Print the sent message
    print(f" [x] Sent {message}")
# Close the connection
connection.close()
