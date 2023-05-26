import os
import scrapy
import configparser
from pprint import pprint

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class Parser:
    """Base parser class, defines the interface."""

    def parse(self, response):
        """
        Parse the given response.

        Args:
            response (scrapy.http.Response): The response to parse.

        Raises:
            NotImplementedError: This method must be overwritten by subclasses.
        """
        raise NotImplementedError


class DefaultParser(Parser):
    """Default parser, tokenizes text and removes stopwords."""

    def parse(self, response):
        """
        Parse the given response, tokenize the text and remove stopwords.

        Args:
            response (scrapy.http.Response): The response to parse.

        Returns:
            dict: A dictionary with the url and the tokens extracted from the text.
        """
        # Define the list of stopwords
        stop_words = set(stopwords.words("english"))

        # Find all paragraph tags and extract the text
        text = " ".join(response.css("p::text").getall())

        # Tokenize the text (split it into individual words)
        tokens = word_tokenize(text)

        # Remove the stopwords
        filtered_tokens = [
            word for word in tokens if word.casefold() not in stop_words
        ]

        # Create dictionary with URL and filtered tokens
        return {"url": response.url, "tokens": filtered_tokens}


class BrightEdgeSpider(scrapy.Spider):
    name = "brightedge"

    def __init__(self, *args, **kwargs):
        super(BrightEdgeSpider, self).__init__(*args, **kwargs)
        self.parser = DefaultParser()  # Use the default parser

        # Read URLs from configuration file
        config = configparser.ConfigParser()
        config.read("scrapy.cfg")

        urls = [
            config.get("urls", "url1"),
            config.get("urls", "url2"),
            config.get("urls", "url3"),
        ]

        self.start_urls = urls

    def start_requests(self):
        # Set User-Agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Cookie": "accept-cookies=yes"
        }

        # Send requests with headers
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        """
        Parse the given response using the current parser.

        Args:
            response (scrapy.http.Response): The response to parse.
        """
        # Exception handling block
        try:
            result = self.parser.parse(response)
            pprint(result, indent=4)  # Print the result using pprint
            yield result
        except Exception as e:
            self.log(
                f"Error parsing {response.url}: {e}", level=scrapy.log.ERROR
            )
