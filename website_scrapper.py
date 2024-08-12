from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from loguru import logger

# from selenium import webdriver
# selenium is used when the page is loaded through javascript and html parser cannot obtain all
# the content on the website


class get_HTML_tags(object):
    def __init__(self, url):
        self.url = url
        self.df = None

    def extract_links_and_text(self):
        """Extracts href links and corresponding text from a webpage and stores them in a pandas DataFrame.

        Args:
          url: The URL of the webpage to scrape.

        Returns:
          A pandas DataFrame containing the extracted href links and text.
        """
        # driver = webdriver.Firefox()
        page = requests.get(self.url)
        # html = driver.page_source
        soup = BeautifulSoup(page.text, "html")
        # driver.quit

        links_data = []
        for link in soup.find_all("a"):
            href = link.get("href")
            text = link.text.strip()
            links_data.append({"text": text, "href": href})

        self.df = pd.DataFrame(links_data)
        logger.debug("extracting urls is completed")

    def extract_headings_paragraphs(url, output_file):
        """Scrapes a webpage and saves the content to a text file.

        Args:
          url: The URL of the webpage to scrape.
          output_file: The path to the output text file.
        """

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        text_content = ""
        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
            text_content += element.text + "\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text_content)

    def is_valid_url(self, url):
        """Checks if the given URL is valid using a regular expression.

        Args:
          url: The URL to check.

        Returns:
          True if the URL is valid, False otherwise.
        """

        # Basic URL validation regex
        url_regex = r"https?://(?:www\\.)?[hackerearth./]?[ a-zA-Z0-9./]+"
        # url_regex = r"^(http|https)://?([\w.-]+(?:\.[\w.-]+)+)/?([\w.-]*)(/\w+(?:/\w+)*)*((\?\w+(=\w+)?(&\w+(=\w+)?)*)|(\#\w+)?)?$"
        return bool(re.match(url_regex, str(url)))

    def validate_urls(self):
        """Validates the 'href' column in a pandas DataFrame.

        Args:
          df: The pandas DataFrame containing the 'href' column.

        Returns:
          A new DataFrame with an additional column 'is_valid_url' indicating the validity of each URL.
        """
        if self.df.shape[0] == 0:
            return None

        self.df["is_valid_url"] = self.df["href"].apply(self.is_valid_url)
        self.df = self.df[self.df.is_valid_url == True].reset_index(drop=True)
        self.df.drop(columns=["is_valid_url"], inplace=True)
        logger.debug("Valid URLs are filtered")
