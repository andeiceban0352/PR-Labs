import requests
from bs4 import BeautifulSoup

HOST = "http://127.0.0.1:8019"


# Go trough the page and get the html details
def parse_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    obj_details = {}

    obj_details["name"] = soup.find('h1').text
    obj_details["price"] = float(soup.find('h4').text)

    paragraphs = soup.find_all('p')
    obj_details["description"] = paragraphs[0].text
    obj_details["author"] = paragraphs[1].text

    return obj_details

# Go trough the url and get the response
def fetch_url(path):
    url = f"{HOST}{path}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Display obj details
def get_general_details():
    print("Main Page:" , fetch_url('/'))

    print("About Page:" , fetch_url('/about'))

    print("Contacts Page:" , fetch_url('/contacts'))

# Display product page
def get_product_page():
    soup = BeautifulSoup(fetch_url('/product'), 'html.parser')
    prod_links = [a['href'] for a in soup.find_all('a', href=True)]

    print("Product Page:" , fetch_url('/product'))

    for item in prod_links:
        print("Product Details Object:" , parse_page(fetch_url(item)))

# Display result
get_general_details()
get_product_page()