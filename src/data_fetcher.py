import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
from openai import OpenAI

client = OpenAI(api_key='')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFetcher:
    def __init__(self):
        self.base_url = "https://fbref.com"
        self.last_request_time = 0
        self.min_request_interval = 3  # Minimum 3 seconds between requests
          # Replace with your actual API key

    def _rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def _make_request(self, url):
        self._rate_limit()
        logging.info(f"Making request to: {url}")
        response = requests.get(url)
        logging.info(f"Response status code: {response.status_code}")
        return response

    def convert_nickname_to_fullname(self, nickname):
        try:
            response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts football player nicknames to their full names."},
                {"role": "user", "content": f"Convert the football player nickname '{nickname}' to their full name."}
            ])
            full_name = response.choices[0].message.content.strip()
            logging.info(f"Converted nickname '{nickname}' to full name: {full_name}")
            return full_name
        except Exception as e:
            logging.error(f"Error converting nickname to full name: {str(e)}", exc_info=True)
            return nickname  # Return the original nickname if conversion fails

    def get_player_stats(self, player_name):
        try:
            logging.info(f"Fetching stats for player: {player_name}")

            # Convert nickname to full name
            full_name = self.convert_nickname_to_fullname(player_name)
            logging.info(f"Using full name for search: {full_name}")

            # Search for the player
            search_url = f"{self.base_url}/search/search.fcgi?search={full_name}"
            response = self._make_request(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the first search result
            search_results = soup.find_all('div', class_='search-item-name')
            logging.info(f"Found {len(search_results)} search results")

            if not search_results:
                logging.warning(f"No search results found for {full_name}")
                return None

            player_link = search_results[0].find('a')['href']
            logging.info(f"Selected player link: {player_link}")

            # Get the player's stats page
            player_url = f"{self.base_url}{player_link}"
            response = self._make_request(player_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the stats table
            stats_table = soup.find('table', id='stats_standard_dom_lg')

            if stats_table:
                df = pd.read_html(str(stats_table))[0]
                logging.info(f"Stats table found. Shape: {df.shape}")

                # Get the most recent season's stats (last row)
                latest_stats = df.iloc[-1]
                logging.info(f"Latest stats: {latest_stats.to_dict()}")

                return {
                    'name': full_name,  # Include the full name in the returned stats
                    'goals': int(latest_stats.get('Gls', 0)),
                    'assists': int(latest_stats.get('Ast', 0)),
                    'passes_completed': int(latest_stats.get('Cmp', 0)),
                    'passes_attempted': int(latest_stats.get('Att', 0)),
                }
            else:
                logging.warning(f"Could not find stats table for {full_name}")
                return None

        except Exception as e:
            logging.error(f"Error fetching data for {player_name}: {str(e)}", exc_info=True)
            return None