# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:44:26 2024

@author: Mariam
"""

from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self, url):
        self.url = url

    def scrape_content(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.get_text()
            else:
                print(f"Error: Failed to fetch page ({response.status_code})")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def save_to_text_file(self, text, file_path='web_content.txt'):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Web content saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"Error: {e}")
            return None

# url = "http://www.accel.com"
# scraper = WebScraper(url)
# web_content = scraper.scrape_content()
# if web_content:
#     scraper.save_to_text_file(web_content)