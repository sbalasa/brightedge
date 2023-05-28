import os
import re
import nltk
import scrapy
import logging


from nltk.corpus import stopwords
from sklearn.decomposition import NMF
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Global
URLS_FILE = "urls.txt"


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
    """Default parser, tokenizes text, lemmatizes and removes stopwords."""

    def clean_text(self, text):
        # Remove HTML entities
        text = re.sub(r"&[a-z]+;", " ", text)

        # Remove non-alphanumeric characters
        text = re.sub(r"\W", " ", text)

        # Replace multiple spaces with a single space
        text = re.sub(r"\s+", " ", text)

        return text

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

        # Clean the text
        text = self.clean_text(text)

        # Tokenize the text (split it into individual words)
        tokens = word_tokenize(text)

        # Lemmatize and remove the stopwords
        lemmatizer = WordNetLemmatizer()
        filtered_tokens = [
            lemmatizer.lemmatize(word)
            for word in tokens
            if word.casefold() not in stop_words
        ]

        # Create dictionary with URL and filtered tokens
        return {"url": response.url, "tokens": filtered_tokens}


class BrightEdgeSpider(scrapy.Spider):
    name = "brightedge"

    def __init__(self, *args, **kwargs):
        super(BrightEdgeSpider, self).__init__(*args, **kwargs)
        self.parser = DefaultParser()  # Use the default parser

        # Read URLs from a text file
        with open(URLS_FILE, "r") as f:
            self.start_urls = [line.strip() for line in f]

        # Define the number of topics for topic modeling
        self.num_topics = 25

    def start_requests(self):
        # Send requests without setting headers (Scrapy settings will be used)
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, callback=self.parse, errback=self.handle_failure
            )

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
            vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
            X = vectorizer.fit_transform(tokens)

            nmf_model = NMF(n_components=self.num_topics, random_state=0)
            nmf_model.fit(X)

            # Get the most relevant topics
            topics = []
            feature_names = vectorizer.get_feature_names_out()
            for topic_idx, topic in enumerate(nmf_model.components_):
                top_features_ind = topic.argsort()[:-6:-1]
                topic_words = [feature_names[i] for i in top_features_ind]
                topics.append(topic_words)

            # Add topics to the result
            result["topics"] = topics
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

        # Yield the failure information as the result
        yield failure_info
