import unittest
import article

class TestArticle(unittest.TestCase):
    # def __init__(self):
    #     self.valid_article = null

    def setUp(self):
        # A random article taken from Mongo with the id field removed.
        self.valid_article = article.Article(**{
            "guid" : "http://www.cnn.com/2015/09/17/opinions/spicer-facebook-dislike-button/index.html",
            "title" : "Facebook 'dislike' button a comeback for negative thinking",
            "url" : "http://rss.cnn.com/c/35494/f/676977/s/4a0b2f94/sc/15/l/0L0Scnn0N0C20A150C0A90C170Copinions0Cspicer0Efacebook0Edislike0Ebutton0Cindex0Bhtml0Deref0Frss0Itech/story01.htm",
            "timestamp" : 1442860397,
            "source" : "cnn",
            "feed" : "cnn_technology",
            "content" : "Facebook 'dislike' button a comeback for negative thinking \nBy Andre Spicer\nAndre Spicer\nThat is about to change. Facebook has announced it will create a \"dislike button.\" Only last year, Mark Zuckerberg said, \"Some people have asked for a dislike button because they want to be able to say 'that thing isn't good,' and we're not going to do that ... I don't think that's socially very valuable, or great for the community.\"\nNow, Zuckerberg has admitted that \"not every moment is good\" and perhaps a dislike button isn't such a bad idea after all.\nZuckerberg may have changed his mind, but many other people have not. Some think the \ndislike button\naggressive behavior online\n. But the biggest worry is the button will \"\nactively foster negativity\nIt seems we have become so fragile that any sign of negativity -- even a simple thumbs down on a social media website -- is something that must be avoided at all costs. All we want is a constant stream of thumbs up. The slightest sign someone might disagree with us is enough to send us into an emotional tailspin.  \nOne of the most insidious ideas of our time is positive thinking. It's drilled into many of us: think positive, don't think negative. It's no wonder people find the prospect of the dislike button so worrisome.  \nBeing positive certainly comes with benefits. But research is starting to reveal that all this \nupbeat thinking has some big downsides\n. When we are unable to express negative feelings, many human emotions become off limits. We avoid taking a realistic look at problems, which means we overlook risks and do stupid things. Those who don't feel on top of the world start to think there is something seriously wrong with them. Those in an upbeat mood tend to be more selfish and feel more socially disconnected. What is even more surprising is that people told to think positively often end up feeling worse.\nAs we start to recognize the limits of always looking on the bright side, negative thinking is making a comeback. \nIt's not just Facebook that will allow you to dislike things. Some companies have started to support their employees in pointing out problems. One particularly interesting method that firms are using to avoid the mistakes made by our bias toward positive thinking is the \"\npre-mortem\nLiving with the thumbs down will be tough. We may get upset, be disturbed and sometimes feel gloomy. Excessive negativity can easily become bullying. But having a space to share our negative feelings every now and then can help us own up to the many problems that we face, and hopefully, deal with them in a levelheaded way.\nJoin us on Facebook.com/CNNOpinion.\nRead CNNOpinion's Flipboard magazine.\nPowered by Livefyre",
            "img" : "http://i2.cdn.turner.com/cnnnext/dam/assets/140113112951-andre-spicer-story-top.jpg",
            "keywords" : [ ]
        })

    def test_isValid_true(self):
        self.assertTrue(article.isValid(self.valid_article))

    def test_isValid_guid_empty(self):
        invalid_article = self.valid_article._replace(guid='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_guid_none(self):
        invalid_article = self.valid_article._replace(guid=None)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_title_empty(self):
        invalid_article = self.valid_article._replace(title='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_title_none(self):
        invalid_article = self.valid_article._replace(guid=None)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_url_empty(self):
        invalid_article = self.valid_article._replace(url='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_url_none(self):
        invalid_article = self.valid_article._replace(url=None)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_timestamp_tiny(self):
        invalid_article = self.valid_article._replace(timestamp=100)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_source_empty(self):
        invalid_article = self.valid_article._replace(source='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_source_none(self):
        invalid_article = self.valid_article._replace(source=None)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_feed_empty(self):
        invalid_article = self.valid_article._replace(feed='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_feed_none(self):
        invalid_article = self.valid_article._replace(feed=None)
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_content_empty(self):
        invalid_article = self.valid_article._replace(content='')
        self.assertFalse(article.isValid(invalid_article))

    def test_isValid_content_none(self):
        invalid_article = self.valid_article._replace(content=None)
        self.assertFalse(article.isValid(invalid_article))

if __name__ == '__main__':
    unittest.main()
