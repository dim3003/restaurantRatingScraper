import requests
from bs4 import BeautifulSoup

# Setting up the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Setting up the url
baseURL = 'https://www.local.ch/fr/q/lausanne/restaurant?page={}'


# Returns the contents of a page given the url
def getURLContent(url):
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(url)

        if response.status_code == 200:
            # Get the page content as a beautiful soup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print("Failed to retrieve the page: Status code", response.status_code)
            return None

def getRestaurantsOnPage(content):
    return content.find_all('div', {'class': 'SearchResultList_listElementWrapper__KRuKD'})



if __name__ == "__main__":
    page = 1
    url = baseURL.format(page)
    content = getURLContent(url)
    print(getRestaurantsOnPage())
