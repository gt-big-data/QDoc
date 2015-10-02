import unittest
from article import Article
from crawlContent import crawlContent

class TestArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # An article generated from a URL and newsource (obvious from URL).
        cls._valid_article = Article()
        cls._valid_article.guid=''
        cls._valid_article.title=''
        cls._valid_article.url='http://www.cnn.com/2015/09/17/opinions/spicer-facebook-dislike-button/index.html'
        cls._valid_article.timestamp=0
        cls._valid_article.source='cnn'
        cls._valid_article.feed=''
        cls._valid_article.content='Facebook \'dislike\' button a comeback for negative thinking \nBy Andre Spicer\nAndre Spicer\nThat is about to change. Facebook has announced it will create a "dislike button." Only last year, Mark Zuckerberg said, "Some people have asked for a dislike button because they want to be able to say \'that thing isn\'t good,\' and we\'re not going to do that ... I don\'t think that\'s socially very valuable, or great for the community."\nNow, Zuckerberg has admitted that "not every moment is good" and perhaps a dislike button isn\'t such a bad idea after all.\nZuckerberg may have changed his mind, but many other people have not. Some think the \ndislike button\naggressive behavior online\n. But the biggest worry is the button will "\nactively foster negativity\nIt seems we have become so fragile that any sign of negativity -- even a simple thumbs down on a social media website -- is something that must be avoided at all costs. All we want is a constant stream of thumbs up. The slightest sign someone might disagree with us is enough to send us into an emotional tailspin.  \nOne of the most insidious ideas of our time is positive thinking. It\'s drilled into many of us: think positive, don\'t think negative. It\'s no wonder people find the prospect of the dislike button so worrisome.  \nBeing positive certainly comes with benefits. But research is starting to reveal that all this \nupbeat thinking has some big downsides\n. When we are unable to express negative feelings, many human emotions become off limits. We avoid taking a realistic look at problems, which means we overlook risks and do stupid things. Those who don\'t feel on top of the world start to think there is something seriously wrong with them. Those in an upbeat mood tend to be more selfish and feel more socially disconnected. What is even more surprising is that people told to think positively often end up feeling worse.\nAs we start to recognize the limits of always looking on the bright side, negative thinking is making a comeback. \nIt\'s not just Facebook that will allow you to dislike things. Some companies have started to support their employees in pointing out problems. One particularly interesting method that firms are using to avoid the mistakes made by our bias toward positive thinking is the "\npre-mortem\nLiving with the thumbs down will be tough. We may get upset, be disturbed and sometimes feel gloomy. Excessive negativity can easily become bullying. But having a space to share our negative feelings every now and then can help us own up to the many problems that we face, and hopefully, deal with them in a levelheaded way.\nJoin us on Facebook.com/CNNOpinion.\nRead CNNOpinion\'s Flipboard magazine.\nPowered by Livefyre'
        cls._valid_article.img=u'http://i2.cdn.turner.com/cnnnext/dam/assets/140113112951-andre-spicer-story-top.jpg'

        other_article = Article()
        other_article.url = 'http://www.cnn.com/2015/09/17/opinions/spicer-facebook-dislike-button/index.html'
        other_article.source = 'cnn'
        articles = [other_article]
        cls._crawled_article = crawlContent(articles)[0]

    def test_same_url(self):
        self.assertEquals(TestArticle._crawled_article.url, TestArticle._valid_article.url)

    def test_same_source(self):
        self.assertEquals(TestArticle._crawled_article.source, TestArticle._valid_article.source)

    def test_same_img(self):
        self.assertEquals(TestArticle._crawled_article.img, TestArticle._valid_article.img)

    def test_same_content(self):
        self.assertEquals(TestArticle._crawled_article.content, TestArticle._valid_article.content)

if __name__ == '__main__':
    unittest.main()
