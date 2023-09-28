from bs4 import BeautifulSoup
import requests
import re , json

links = []  # store links

def process_url(url, max_page):
    rez = requests.get(url) 
    html_doc = rez.text  

    # Parse the HTML content using BeautifulSoup and find the current page
    soup = BeautifulSoup(html_doc, 'html.parser') 
    current_page = soup.find('li', class_='current') 

    # Get the page nr from the current page
    page_nr = current_page.a.text 

    if int(page_nr) > max_page:
        return "The last page was reached"
    else:
        # Find all anchor tags with 'href' attribute starting with "/ro/" and 'class' containing "js-item-ad"
        for link in soup.find_all('a', attrs={'href': re.compile("/ro/"), 'class': re.compile("js-item-ad")}):
            links.append("https://999.md" + link.get('href'))  # Append the complete URL to the links list

        next_page = current_page.find_next('li').find('a') if current_page else None 

        if next_page:
            next_url = "https://999.md" + next_page['href'] 


    # Recursively call the function with the URL of the next page
    return process_url(next_url, max_page)


process_url('https://999.md/ru/list/real-estate/apartments-and-rooms?o_30_241=894&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776', 1)
print('The links are: ', links)

# with open('links', 'w', encoding='utf-8') as json_file:
#     json.dump(links, json_file, indent=4, ensure_ascii=False)
