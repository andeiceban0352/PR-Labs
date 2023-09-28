import requests
from bs4 import BeautifulSoup

def process_product_link(url):
    # store product information
    object_info = {}

    # retrieve the HTML content
    response = requests.get(url)
    html_document = response.text

    # parse the HTML content
    soup = BeautifulSoup(html_document, 'html.parser')

    # Find all list items with class 'm-value' in the HTML
    filtered_data = soup.find_all('li', class_='m-value')

    for item in filtered_data:
        # Find the 'span' element with class 'adPage__content__features__key'
        k = item.find('span', class_='adPage__content__features__key')
        # Find the 'span' element with class 'adPage__content__features__value'
        v = item.find('span', class_='adPage__content__features__value')

        # Check if both key and value elements are found
        if k and v:
            # Extract and strip the text content of the key and value elements
            key = k.text.strip()
            value = v.text.strip()
            object_info[key] = value

    print(object_info)

process_product_link('https://999.md/ro/81949631')
