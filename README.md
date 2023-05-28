# BrightEdge

This is a Scrapy spider named BrightEdgeSpider that performs advanced natural language processing on web pages.

## Description

BrightEdgeSpider is a powerful web scraper that doesn't just extract text, but also cleans, tokenizes, and lemmatizes it. It uses Natural Language Toolkit (NLTK) and Scikit-Learn for natural language processing, removing stopwords, lemmatizing words, and performing topic modeling using Non-negative Matrix Factorization (NMF).

This spider is capable of handling multiple URLs at a time and returning detailed analysis for each page, including the most relevant topics based on the page's content.

### To Install

```
pip3 install -r requirements.txt
```

### To Add URL's

```
vim urls.txt
```

### To Run

```
cd brightedge
scrapy crawl brightedge -o output.json 
```

### To View Results

```
black -l 80 output.json
cat output.json
```

### To Run via Docker

```
docker build -t brightedge .
docker run -v "$(pwd)/brightedge/urls.txt:/app/brightedge/urls.txt" -v "$(pwd)/brightedge/output.json:/app/brightedge/output.json" brightedge
```

### To Test

```
pytest brightedge/spiders/tests
```

### To View Implementation

Please see the [Implementation Document](Implementation.md)

### To View Enhancement Design

For more details about the design and enhancement of this spider, please see the [Design Documentation](Design.md)
