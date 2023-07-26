import logging
from bs4 import BeautifulSoup
import requests

class URLScraper:
    def __init__(self) -> None:
        self.logger = logging.getLogger('logs/URLExtractor')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def extract_text_from_website(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            extracted_text = soup.get_text()

            self.logger.info(f"Successfully extracted text from: {url}")
            return extracted_text

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request Exception occurred while extracting from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error occurred while extracting from {url}: {e}")
            return None

    def extract_text_from_wiki(self, url):
        extracted_text = ""
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                for paragraph in paragraphs:
                    extracted_text += str((paragraph.get_text()))
            else:
                print(f"Failed to retrieve the URL. Status code: {response.status_code}")
                self.logger.info(f"Successfully extracted text from: {url}")
            return extracted_text

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request Exception occurred while extracting from {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error occurred while extracting from {url}: {e}")
            return None