# Project Overview

This project consists of a Scrapy-based web scraping system, designed to gather data from a variety of URLs, and conduct text processing and topic modeling on the extracted data. The system also incorporates middleware components to manage cookies and User-Agent settings for the spider.

Here are the main components of the project:

1. **`BrightEdgeSpider` Class**: The core spider class of the project, it reads URLs from a file and sends a request to each of them. The response is processed through the `DefaultParser` class. The resulting text is then supplied to a TF-IDF vectorizer and a Non-negative Matrix Factorization (NMF) model for topic modeling.

2. **`DefaultParser` Class**: This class handles text processing. It accepts the raw HTML response, extracts the text, tokenizes it, lemmatizes the tokens, and eliminates stop words.

3. **`UserAgentMiddleware` Class**: This middleware is responsible for managing the User-Agent settings for requests, choosing a random User-Agent for each request from a predefined list.

4. **`Settings`**: This section holds global settings for your Scrapy project. These include settings relating to download delay, concurrent requests, cookies handling, retry attempts, User-Agent list, and middleware configuration.

## URL Reading

The BrightEdgeSpider class reads the target URLs from a `urls.txt` file. Each line in this file is treated as a separate URL for the spider to scrape.


### Why Scrapy ?

Scrapy is a popular, powerful, and versatile Python framework for web scraping and crawling. Here's why it's often chosen for these tasks:

1. **Powerful and Fast**: Scrapy is designed to handle large amounts of data and navigate complex websites quickly and efficiently.

2. **Middleware and Extensions Support**: Scrapy supports a large number of middlewares and extensions, and allows the development of custom ones.

3. **Handling of Request/Responses**: Scrapy handles the requests and responses in a very organized way, allowing us to apply pre-processing steps on the responses and handle different error codes without breaking the spider.

4. **Item Pipelines**: Scrapy provides the ability to write pipelines, where we can manipulate the data, validate it, and even store it in any storage system (Database, File, Cloud Storage etc.).

5. **Built-in Support for Selecting and Extracting Data**: Scrapy comes with built-in support for selecting and extracting data from sources either by XPath or CSS expressions.

6. **Robust and Scalable**: Scrapy is designed to be robust and scalable, making it suitable for large scale web scraping tasks and projects.

7. **Broad Community and Good Documentation**: Scrapy has a large community of users and contributors, and its documentation is comprehensive and well-maintained.

So, for tasks involving web scraping, Scrapy is often a top choice due to these robust features. It's especially useful in the context of this code, where it's being used to scrape text data from various web pages for further analysis.
