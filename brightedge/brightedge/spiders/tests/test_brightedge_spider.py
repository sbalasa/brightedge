import unittest
from scrapy.http import Response
from ..brightedge_spider import BrightEdgeSpider, DefaultParser

class BrightEdgeSpiderTests(unittest.TestCase):
    def setUp(self):
        self.spider = BrightEdgeSpider()

    def test_clean_text(self):
        parser = DefaultParser()
        text = "<p>Sample&nbsp;text!</p>"
        cleaned_text = parser.clean_text(text)

        # Assert the expected output
        self.assertEqual(cleaned_text.strip(), "p Sample text p")

    def test_parse(self):
        # Create a sample response for testing
        url = "http://example.com"
        body = "<html><body><p>Sample text</p></body></html>"
        response = Response(url=url)

        # Parse the response
        results = list(self.spider.parse(response))

        # Assert the expected output
        self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()
