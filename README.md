# BrightEdge

This is a Scrapy spider for web scraping using the BrightEdgeSpider class.

## Description

The BrightEdgeSpider is a web scraping spider built with Scrapy. It extracts text from web pages, tokenizes the text, and removes stopwords.

### To Install

```
pip3 install -r requirements.txt
```

### To Run

```
scrapy crawl brightedge -o output.json 
```

### To View Results

```
black -l 80 output.json
cat output.json
```
### To View Enhancement Design

[Design Documentation](Design.md)
