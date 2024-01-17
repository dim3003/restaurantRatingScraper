import requests
import pandas as pd
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
    def get_rating(listing: BeautifulSoup) -> float:
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
    def get_review_count(listing: BeautifulSoup) -> int:
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
    
    def create_dataframe_from_restaurants(self, restaurants: List[BeautifulSoup]) -> pd.DataFrame:
        """
        Makes a pandas DataFrame with: name, address, rating, review count
        from a list of restaurants gotten with BeautifulSoup.
        """
        dataframe = pd.DataFrame(columns=['name', 'address', 'rating', 'review_count'])
        for restaurant in restaurants:
            name = self.get_name(restaurant)
            address = self.get_address(restaurant)
            rating = self.get_rating(restaurant)
            review_count = self.get_review_count(restaurant)

            # Create a new DataFrame for each restaurant
            new_row_df = pd.DataFrame([{
                'name': name, 
                'address': address, 
                'rating': rating, 
                'review_count': review_count
            }])

            # Concatenate the new DataFrame to the existing one
            dataframe = pd.concat([dataframe, new_row_df], ignore_index=True, encoding='utf-8-sig')

        return dataframe

    

    def scrape_multiple_pages(self, start_page: int, end_page: int) -> pd.DataFrame:
        """
        Scrapes restaurant data from a range of pages and returns a combined DataFrame.
        """
        all_restaurants_df = pd.DataFrame()

        for page in range(start_page, end_page + 1):
            print(f"Scraping page {page}...")
            content = self.get_url_content(page)
            if content:
                restaurants = self.get_restaurants_on_page(content)
                page_df = self.create_dataframe_from_restaurants(restaurants)
                all_restaurants_df = pd.concat([all_restaurants_df, page_df], ignore_index=True)

        return all_restaurants_df


if __name__ == "__main__":
    scraper = LocalCHScraper()

    # Define the range of pages you want to scrape
    start_page = 1
    end_page = 37  

    # Scrape data and create a DataFrame
    full_data = scraper.scrape_multiple_pages(start_page, end_page)

    # Save the DataFrame to a CSV file
    csv_file_path = 'scraped_restaurants.csv'  # You can change the file path and name as needed
    full_data.to_csv(csv_file_path, index=False)

    print(f"Data successfully saved to {csv_file_path}")

