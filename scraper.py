import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
from typing import Optional, List

class LocalCHScraper:
    BASE_URL = 'https://www.local.ch/fr/q/lausanne/restaurant?page={}'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    @staticmethod
    def get_url_content(page: int) -> Optional[BeautifulSoup]:
        """
        Returns the contents of a page given the url.
        """
        url = LocalCHScraper.BASE_URL.format(page)
        try:
            response = requests.get(url, headers=LocalCHScraper.HEADERS)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    @staticmethod
    def get_restaurants_on_page(content: BeautifulSoup) -> List[BeautifulSoup]:
        """
        Creates a list of restaurants/items in local.ch page.
        """
        return content.find_all('div', {'class': 'SearchResultList_listElementWrapper__KRuKD'})

    @staticmethod
    def get_name(listing: BeautifulSoup) -> str:
        """
        Gets the name of the listing on local.ch item.
        """
        return listing.find('h2').find('span').text.strip()

    @staticmethod
    def get_address(listing: BeautifulSoup) -> str:
        """
        Gets the address from a listing of local.ch fetched with bs4
        """
        return listing.find('address').text.strip()

    @staticmethod
    def get_rating(listing: BeautifulSoup) -> str:
        """
        Gets the rating out of 5 from the local.ch listing fetched with bs4
        """
        # Parse the HTML content
        rating_element = listing.find('span', {'data-testid': 'average-rating'})

        # Extract the text and convert to float
        if rating_element:
            rating_text = rating_element.get_text().split('/')[0].strip()
            rating_value = float(rating_text)
            return rating_value
        else:
            return None
    
    @staticmethod
    def get_review_count(listing):
        """
        Gets the quantity of ratings per listing on local.ch
        """
        # Find the element containing the review count
        review_count_element = listing.find('span', {'data-testid': 'counter-rating'})

        # Extract the text and convert to integer
        if review_count_element:
            review_count_text = review_count_element.get_text().strip("()")
            review_count = int(review_count_text)
            return review_count
        else:
            return 0

if __name__ == "__main__":
    scraper = LocalCHScraper()

    page = 1
    content = scraper.get_url_content(page)
    if content:
        restaurants = scraper.get_restaurants_on_page(content)
        # Process each restaurant as needed

