import unittest
from article import Article
from crawlContent import parse
import json

INPUT_HTML = 'test/inputs/cnn_test_1.html'
INPUT_JSON = 'test/inputs/cnn_test_1.json'

class TestArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INPUT_JSON) as f:
            cls.valid_data = json.load(f)

        with open(INPUT_HTML) as f:
          html = f.read()

        article = Article()
        article.url = cls.valid_data['url']
        article.source = cls.valid_data['source']
        parse(article, html)
        cls._crawled_article = article

    def test_same_url(self):
        self.assertEquals(TestArticle.valid_data['url'], TestArticle._crawled_article.url)

    def test_same_source(self):
        self.assertEquals(TestArticle.valid_data['source'], TestArticle._crawled_article.source)

    def test_same_img(self):
        self.assertEquals(TestArticle.valid_data['img'], TestArticle._crawled_article.img)

    def test_same_content(self):
        self.assertEquals(TestArticle.valid_data['content'].encode('utf-8'), TestArticle._crawled_article.content)

if __name__ == '__main__':
    unittest.main()
