from crawlFeed import *
import time, eventlet

start_time = time.time()

# Sources to add:
	# RioTimesOnline
	# UberGizmo
	# AFP

feeds = {}

feeds['anadolu'] = [{'name': 'aa_live', 'url': 'https://www.aa.com.tr/en/rss/default?cat=live'}] # Anadolu Agency english
feeds['aljazeera'] = [{'name': 'alj_allfeeds', 'url': 'http://america.aljazeera.com/content/ajam/articles.rss'}]
feeds['allafrica'] = [{'name': 'allaf_main', 'url': 'http://allafrica.com/tools/headlines/rdf/latest/headlines.rdf'},
{'name': 'allaf_africa', 'url': 'http://allafrica.com/tools/headlines/rdf/africa/headlines.rdf'}]

feeds['ap'] = [{'name': 'ap_top', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305'},
{'name': 'ap_us', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7'},
{'name': 'ap_world', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5'},
{'name': 'ap_politics', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa'},
{'name': 'ap_business', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3'},
{'name': 'ap_technology', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/495d344a0d10421e9baa8ee77029cfbd'},
{'name': 'ap_sports', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/347875155d53465d95cec892aeb06419'},
{'name': 'ap_health', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/bbd825583c8542898e6fa7d440b9febc'},
{'name': 'ap_science', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/b2f0ca3a594644ee9e50a8ec4ce2d6de'}]

feeds['austinchronicle'] = [{'name': 'austchr_main', 'url': 'http://www.austinchronicle.com/gyrobase/rss/news.xml'}]
feeds['bbc'] = [{'name': 'bbc_world', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml'},
{'name': 'bbc_business', 'url': 'http://feeds.bbci.co.uk/news/business/rss.xml'},
{'name': 'bbc_politics', 'url': 'http://feeds.bbci.co.uk/news/politics/rss.xml'},
{'name': 'bbc_science', 'url': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'},
{'name': 'bbc_technology', 'url': 'http://feeds.bbci.co.uk/news/technology/rss.xml'},
{'name': 'bbc_entertainment', 'url': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml'}]

feeds['bnamericas'] = [{'name': 'bnam_main', 'url': 'http://feeds.feedburner.com/BusinessNewsAmericas-TopStoriesEN'}]
feeds['business_insider'] = [{'name': 'bi_allfeeds', 'url': 'http://www.businessinsider.in/rss_section_feeds/2147477994.cms'}]

feeds['chinadaily'] = [{'name': 'chiday_china', 'url': 'http://www.chinadaily.com.cn/rss/china_rss.xml'},
{'name': 'chiday_world', 'url': 'http://www.chinadaily.com.cn/rss/world_rss.xml'},
{'name': 'chiday_sports', 'url': 'http://www.chinadaily.com.cn/rss/sports_rss.xml'}]

feeds['cnn'] = [{'name': 'cnn_technology', 'url': 'http://rss.cnn.com/rss/edition_technology.rss'},
{'name': 'cnn_science', 'url': 'http://rss.cnn.com/rss/edition_space.rss'},
{'name': 'cnn_world', 'url': 'http://rss.cnn.com/rss/edition_world.rss'},
{'name': 'cnn_entertainment', 'url': 'http://rss.cnn.com/rss/edition_entertainment.rss'},
{'name': 'cnn_sport', 'url': 'http://rss.cnn.com/rss/edition_sport.rss'},
{'name': 'cnn_travel', 'url': 'http://travel.cnn.com/rss.xml'},
{'name': 'cnn_us', 'url': 'http://rss.cnn.com/rss/edition_us.rss'}]

feeds['euronews'] = [{'name': 'eun_news', 'url': 'http://feeds.feedburner.com/euronews/en/home/'},
{'name': 'eun_business', 'url': 'http://feeds.feedburner.com/euronews/en/business/'},
{'name': 'eun_europe', 'url': 'http://feeds.feedburner.com/euronews/en/europa/'},
{'name': 'eun_scitech', 'url': 'http://feeds.feedburner.com/euronews/en/sci-tech/'},
{'name': 'eun_scitech', 'url': 'http://feeds.feedburner.com/euronews/en/sci-tech/'},
{'name': 'eun_lifestyle', 'url': 'http://feeds.feedburner.com/euronews/en/lifestyle/'}]

feeds['france24'] = [{'name': 'f24_livenews', 'url': 'http://www.france24.com/en/timeline/rss'}]

feeds['guardian'] = [{'name': 'gua_world', 'url': 'http://www.theguardian.com/world/rss'},
{'name': 'gua_politics', 'url': 'http://www.theguardian.com/politics/rss'},
{'name': 'gua_culture', 'url': 'http://www.theguardian.com/culture/rss'},
{'name': 'gua_business', 'url': 'http://www.theguardian.com/business/rss'},
{'name': 'gua_environment', 'url': 'http://www.theguardian.com/environment/rss'},
{'name': 'gua_travel', 'url': 'http://www.theguardian.com/travel/rss'}]

feeds['independent'] = [{'name': 'indep_news', 'url': 'http://www.independent.co.uk/news/rss'},
{'name': 'indep_sport', 'url': 'http://www.independent.co.uk/sport/rss'}]

feeds['indiatimes'] = [{'name': 'it_top', 'url': 'http://timesofindia.indiatimes.com/rssfeedstopstories.cms'},
{'name': 'it_india', 'url': 'http://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms'},
{'name': 'it_world', 'url': 'http://timesofindia.indiatimes.com/rssfeeds/296589292.cms'},
{'name': 'it_sports', 'url': 'http://timesofindia.indiatimes.com/rssfeeds/4719148.cms'},
{'name': 'it_science', 'url': 'http://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms'}]

feeds['latimes'] = [{'name': 'lat_main', 'url': 'http://www.latimes.com/rss2.0.xml'}]
feeds['mercopress'] = [{'name': 'merco_main', 'url': 'http://en.mercopress.com/rss/brazil'}]
feeds['middle_east_eye'] = [{'name': 'mee_main', 'url': 'http://www.middleeasteye.net/rss'}]

feeds['nytimes'] = [{'name': 'nyt_world', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/World.xml'},
{'name': 'nyt_us', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/US.xml'},
{'name': 'nyt_ny', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/NYRegion.xml'},
{'name': 'nyt_business', 'url': 'http://feeds.nytimes.com/nyt/rss/Business'},
{'name': 'nyt_technology', 'url': 'http://feeds.nytimes.com/nyt/rss/Technology'},
{'name': 'nyt_sports', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/Sports.xml'}]

feeds['reuters'] = [{'name': 'reuters_arts', 'url': 'http://feeds.reuters.com/news/artsculture?format=xml'},
{'name': 'reuters_business', 'url': 'http://feeds.reuters.com/reuters/businessNews?format=xml'},
{'name': 'reuters_entertainment', 'url': 'http://feeds.reuters.com/reuters/entertainment?format=xml'},
{'name': 'reuters_environment', 'url': 'http://feeds.reuters.com/reuters/environment?format=xml'},
{'name': 'reuters_money', 'url': 'http://feeds.reuters.com/news/wealth?format=xml'},
{'name': 'reuters_politics', 'url': 'http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'},
{'name': 'reuters_science', 'url': 'http://feeds.reuters.com/reuters/scienceNews?format=xml'},
{'name': 'reuters_sports', 'url': 'http://feeds.reuters.com/reuters/sportsNews?format=xml'},
{'name': 'reuters_technology', 'url': 'http://feeds.reuters.com/reuters/technologyNews?format=xml'},
{'name': 'reuters_us', 'url': 'http://feeds.reuters.com/Reuters/domesticNews?format=xml'},
{'name': 'reuters_world', 'url': 'http://feeds.reuters.com/Reuters/worldNews?format=xml'}]

feeds['russiatoday'] = [{'name': 'rt_allfeeds', 'url': 'https://www.rt.com/rss/news/'}]
feeds['techcrunch'] = [{'name': 'tc_allfeeds', 'url': 'http://feeds.feedburner.com/TechCrunch/'}]
feeds['venture_beat'] = [{'name': 'vb_allfeeds', 'url': 'http://feeds.venturebeat.com/VentureBeat'}]
feeds['wikinews'] = [{'name': 'wikinews_main', 'url': 'https://en.wikinews.org/w/index.php?title=Special:NewsFeed&feed=rss&categories=Published&notcategories=No%20publish%7CArchived%7cAutoArchived%7cdisputed&namespace=0&count=15&ordermethod=categoryadd&stablepages=only'}]

feedList = []
for source in feeds.keys():
	for feed in feeds[source]:
		feed['source'] = source
		feedList.append(feed)

requests = eventlet.import_patched('requests.__init__')

def prepareCrawlfeed(feed):
	crawlFeed(feed['source'], feed['name'], feed['url'], requests)

pool = eventlet.GreenPool()
i=0
while i < len(feedList):
	tempSize = min(50, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	for ret in pool.imap(prepareCrawlfeed, tempList):
		pass
	i += tempSize
print("--- %s seconds ---" % round(time.time() - start_time, 2))