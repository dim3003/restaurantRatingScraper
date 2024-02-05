import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, List

class theForkScraper:
    BASE_URL = 'https://www.thefork.ch/restaurants/lausanne-c305411?p={}'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    @staticmethod
    def get_url_content(page: int) -> Optional[BeautifulSoup]:
        """
        Returns the contents of a page given the url.
        """
        url = theForkScraper.BASE_URL.format(page)
        try:
            response = requests.get(url, headers=theForkScraper.HEADERS)
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
        return None

    @staticmethod
    def get_name(listing: BeautifulSoup) -> str:
        """
        Gets the name of the listing on local.ch item.
        """
        return None

    @staticmethod
    def get_address(listing: BeautifulSoup) -> str:
        """
        Gets the address from a listing of local.ch fetched with bs4
        """
        return None

    @staticmethod
    def get_rating(listing: BeautifulSoup) -> float:
        """
        Gets the rating out of 5 from the local.ch listing fetched with bs4
        """
        return None
    
    @staticmethod
    def get_review_count(listing: BeautifulSoup) -> int:
        """
        Gets the quantity of ratings per listing on local.ch
        """
        return None
    
    def create_dataframe_from_restaurants(self, restaurants: List[BeautifulSoup]) -> pd.DataFrame:
        """
        Makes a pandas DataFrame with: name, address, rating, review count
        from a list of restaurants gotten with BeautifulSoup.
        """
        return None

    

    def scrape_multiple_pages(self, start_page: int, end_page: int) -> pd.DataFrame:
        """
        Scrapes restaurant data from a range of pages and returns a combined DataFrame.
        """
        return None


if __name__ == "__main__":
    scraper = theForkScraper()
    print(scraper.get_url_content(1))

