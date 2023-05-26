import os
import scrapy
import configparser
import logging
from pprint import pprint

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


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

        # Define the number of topics for topic modeling
        self.num_topics = 25

    def start_requests(self):
        # Send requests without setting headers (Scrapy settings will be used)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, errback=self.handle_failure)

    def parse(self, response):
        """
        Parse the given response using the current parser.

        Args:
            response (scrapy.http.Response): The response to parse.
        """
        # Exception handling block
        try:
            result = self.parser.parse(response)
            tokens = result["tokens"]

            # Perform topic modeling using Scikit-learn
            text = " ".join(tokens)
            vectorizer = CountVectorizer()
            X = vectorizer.fit_transform([text])

            lda_model = LatentDirichletAllocation(
                n_components=self.num_topics, random_state=0
            )
            lda_model.fit(X)

            # Get the most relevant topics
            topics = []
            feature_names = vectorizer.get_feature_names_out()
            for topic_idx, topic in enumerate(lda_model.components_):
                top_features_ind = topic.argsort()[:-6:-1]
                topic_words = [feature_names[i] for i in top_features_ind]
                topics.append(topic_words)

            # Add topics to the result
            result["topics"] = topics

            pprint(result, indent=4)  # Print the result using pprint
            yield result
        except Exception as e:
            logging.error(f"Error parsing {response.url}: {e}")

    def handle_failure(self, failure):
        # Extract the URL from the failure
        url = failure.request.url

        # Extract the reason for failure
        reason = str(failure.value)

        # Create a dictionary with URL and reason
        failure_info = {"url": url, "failure_reason": reason}

        # Print the failure information
        pprint(failure_info, indent=4)

        # Yield the failure information as the result
        yield failure_info
