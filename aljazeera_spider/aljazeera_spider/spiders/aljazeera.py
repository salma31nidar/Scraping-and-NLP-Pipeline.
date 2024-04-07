import scrapy
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class AljazeeraSpider(scrapy.Spider):
    name = 'aljazeera'
    start_urls = ['https://www.aljazeera.net/news/']
    max_clicks = 10

    def __init__(self, *args, **kwargs):
        super(AljazeeraSpider, self).__init__(*args, **kwargs)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['lab1']
        self.collection = self.db['eljazzira']
        self.driver = webdriver.Chrome()  # Initialize WebDriver (you can use other browsers as well)

    def parse(self, response):
        self.driver.get(response.url)

        # Scroll to the bottom of the page multiple times to ensure the button is in view
        for _ in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Wait for a moment after each scroll

        # Initialize counter for button clicks
        click_count = 0

        # Find and click the "See More" button multiple times
        try:
            while click_count < self.max_clicks:
                show_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@class="show-more-button big-margin"]'))
                )
                self.driver.execute_script("arguments[0].click();", show_more_button)
                print("Clicked 'See More' button successfully")
                click_count += 1
                time.sleep(5)  # Wait for some time after clicking the button
        except Exception as e:
            self.logger.error(f"Error: Could not find or click the 'See More' button: {e}")

        # Wait for some time to let the page load after clicking the button
        time.sleep(5)  # Adjust the waiting time as needed

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Find all <a> tags with class "u-clickable-card__link"
        links = soup.find_all('a', class_='u-clickable-card__link', href=True)

        # Loop through each link found
        for link in links:
            href = link['href']
            # Check if the URL is relative, if so, join it with the base URL
            if not href.startswith('http'):
                href = urljoin(response.url, href)

            # Send a request to the link URL
            yield scrapy.Request(href, callback=self.parse_article, meta={'link_url': href})

    def parse_article(self, response):
        # Extract the URL of the article
        article_url = response.meta.get('link_url')

        # Parse the HTML content of the article page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the header (h1)
        header = soup.find('h1').text.strip()

        # Extract paragraphs (p)
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in paragraphs])

        # Insert data into MongoDB
        news_item = {
            'url': article_url,
            'header': header,
            'content': content
        }
        self.collection.insert_one(news_item)

        # Output the results
        self.logger.info(f"Article URL: {article_url}")
        self.logger.info(f"Header: {header}")
        self.logger.info(f"Content: {content}")

    def closed(self, reason):
        self.driver.quit()  # Close WebDriver when spider is closed
