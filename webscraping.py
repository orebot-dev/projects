import requests
from bs4 import BeautifulSoup

# website I want to scrape 
url = 'https://www.baseball-reference.com/'

# get request for raw html content
response = requests.get(url)

# check if the request code was successful (status code 200)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    headings = soup.find_all('h1')

    for heading in headings:
        print(heading.text)
    
    links = soup.find_all('a')

    for link in links:
        pass #print(link.get('href'))

    def is_good_link(a):
        href = a.get('href')
        if len(href) == 0:
            return False
        if not href[0] == "/":
            return False
        if href[0:1] == "//":
            return False
        if "sports-reference" in href:
            return False
        return True

    filtered_links = filter(is_good_link, links)
    for link in filtered_links:
        print(link.get('href'))

else:
    print(f"failed to retrieve the page. Status code: {response.status_code}")