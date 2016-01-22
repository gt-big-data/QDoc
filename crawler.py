from crawlFeed import *
import time, eventlet

start_time = time.time()

# Sources to add:
	# The Independent
	# Russia Today
	# UberGizmo
	# AFP

feeds = {}

feeds['anadolu'] = [] # Anadolu Agency english
feeds['anadolu'].append({'name': 'aa_live', 'url': 'https://www.aa.com.tr/en/rss/default?cat=live'})

feeds['aljazeera'] = []
feeds['aljazeera'].append({'name': 'alj_allfeeds', 'url': 'http://america.aljazeera.com/content/ajam/articles.rss'})

feeds['ap'] = []
feeds['ap'].append({'name': 'ap_top', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305'})
feeds['ap'].append({'name': 'ap_us', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/386c25518f464186bf7a2ac026580ce7'})
feeds['ap'].append({'name': 'ap_world', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/cae69a7523db45408eeb2b3a98c0c9c5'})
feeds['ap'].append({'name': 'ap_politics', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/89ae8247abe8493fae24405546e9a1aa'})
feeds['ap'].append({'name': 'ap_business', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/f70471f764144b2fab526d39972d37b3'})
feeds['ap'].append({'name': 'ap_technology', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/495d344a0d10421e9baa8ee77029cfbd'})
feeds['ap'].append({'name': 'ap_sports', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/347875155d53465d95cec892aeb06419'})
feeds['ap'].append({'name': 'ap_health', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/bbd825583c8542898e6fa7d440b9febc'})
feeds['ap'].append({'name': 'ap_science', 'url': 'http://hosted2.ap.org/atom/APDEFAULT/b2f0ca3a594644ee9e50a8ec4ce2d6de'})

feeds['bbc'] = []
feeds['bbc'].append({'name': 'bbc_world', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml'})
feeds['bbc'].append({'name': 'bbc_business', 'url': 'http://feeds.bbci.co.uk/news/business/rss.xml'})
feeds['bbc'].append({'name': 'bbc_politics', 'url': 'http://feeds.bbci.co.uk/news/politics/rss.xml'})
feeds['bbc'].append({'name': 'bbc_science', 'url': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'})
feeds['bbc'].append({'name': 'bbc_technology', 'url': 'http://feeds.bbci.co.uk/news/technology/rss.xml'})
feeds['bbc'].append({'name': 'bbc_entertainment', 'url': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml'})

feeds['business_insider'] = [] # http://www.businessinsider.in/rss_feeds.cms
feeds['business_insider'].append({'name': 'bi_allfeeds', 'url': 'http://www.businessinsider.in/rss_section_feeds/2147477994.cms'})

feeds['cnn'] = [] # http://edition.cnn.com/services/rss/
feeds['cnn'].append({'name': 'cnn_world', 'url': 'http://rss.cnn.com/rss/edition_world.rss'})
feeds['cnn'].append({'name': 'cnn_technology', 'url': 'http://rss.cnn.com/rss/edition_technology.rss'})
feeds['cnn'].append({'name': 'cnn_science', 'url': 'http://rss.cnn.com/rss/edition_space.rss'})
feeds['cnn'].append({'name': 'cnn_entertainment', 'url': 'http://rss.cnn.com/rss/edition_entertainment.rss'})
feeds['cnn'].append({'name': 'cnn_sport', 'url': 'http://rss.cnn.com/rss/edition_sport.rss'})
feeds['cnn'].append({'name': 'cnn_travel', 'url': 'http://travel.cnn.com/rss.xml'})
feeds['cnn'].append({'name': 'cnn_us', 'url': 'http://rss.cnn.com/rss/edition_us.rss'})

feeds['euronews'] = []
feeds['euronews'].append({'name': 'eun_news', 'url': 'http://feeds.feedburner.com/euronews/en/home/'})
feeds['euronews'].append({'name': 'eun_business', 'url': 'http://feeds.feedburner.com/euronews/en/business/'})
feeds['euronews'].append({'name': 'eun_europe', 'url': 'http://feeds.feedburner.com/euronews/en/europa/'})
feeds['euronews'].append({'name': 'eun_scitech', 'url': 'http://feeds.feedburner.com/euronews/en/sci-tech/'})
feeds['euronews'].append({'name': 'eun_scitech', 'url': 'http://feeds.feedburner.com/euronews/en/sci-tech/'})
feeds['euronews'].append({'name': 'eun_lifestyle', 'url': 'http://feeds.feedburner.com/euronews/en/lifestyle/'})

feeds['france24'] = []
feeds['france24'].append({'name': 'f24_livenews', 'url': 'http://www.france24.com/en/timeline/rss'})

feeds['guardian'] = []
feeds['guardian'].append({'name': 'gua_world', 'url': 'http://www.theguardian.com/world/rss'})
feeds['guardian'].append({'name': 'gua_politics', 'url': 'http://www.theguardian.com/politics/rss'})
feeds['guardian'].append({'name': 'gua_culture', 'url': 'http://www.theguardian.com/culture/rss'})
feeds['guardian'].append({'name': 'gua_business', 'url': 'http://www.theguardian.com/business/rss'})
feeds['guardian'].append({'name': 'gua_environment', 'url': 'http://www.theguardian.com/environment/rss'})
feeds['guardian'].append({'name': 'gua_travel', 'url': 'http://www.theguardian.com/travel/rss'})

feeds['middle_east_eye'] = []
feeds['middle_east_eye'].append({'name': 'mee_main', 'url': 'http://www.middleeasteye.net/rss'})

feeds['nytimes'] = []
feeds['nytimes'].append({'name': 'nyt_world', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/World.xml'})
feeds['nytimes'].append({'name': 'nyt_us', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/US.xml'})
feeds['nytimes'].append({'name': 'nyt_ny', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/NYRegion.xml'})
feeds['nytimes'].append({'name': 'nyt_business', 'url': 'http://feeds.nytimes.com/nyt/rss/Business'})
feeds['nytimes'].append({'name': 'nyt_technology', 'url': 'http://feeds.nytimes.com/nyt/rss/Technology'})
feeds['nytimes'].append({'name': 'nyt_sports', 'url': 'http://www.nytimes.com/services/xml/rss/nyt/Sports.xml'})

feeds['reuters'] = [] # http://www.reuters.com/tools/rss
feeds['reuters'].append({'name': 'reuters_arts', 'url': 'http://feeds.reuters.com/news/artsculture?format=xml'})
feeds['reuters'].append({'name': 'reuters_business', 'url': 'http://feeds.reuters.com/reuters/businessNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_entertainment', 'url': 'http://feeds.reuters.com/reuters/entertainment?format=xml'})
feeds['reuters'].append({'name': 'reuters_environment', 'url': 'http://feeds.reuters.com/reuters/environment?format=xml'})
feeds['reuters'].append({'name': 'reuters_money', 'url': 'http://feeds.reuters.com/news/wealth?format=xml'})
feeds['reuters'].append({'name': 'reuters_politics', 'url': 'http://feeds.reuters.com/Reuters/PoliticsNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_science', 'url': 'http://feeds.reuters.com/reuters/scienceNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_sports', 'url': 'http://feeds.reuters.com/reuters/sportsNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_technology', 'url': 'http://feeds.reuters.com/reuters/technologyNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_us', 'url': 'http://feeds.reuters.com/Reuters/domesticNews?format=xml'})
feeds['reuters'].append({'name': 'reuters_world', 'url': 'http://feeds.reuters.com/Reuters/worldNews?format=xml'})

feeds['techcrunch'] = []
feeds['techcrunch'].append({'name': 'tc_allfeeds', 'url': 'http://feeds.feedburner.com/TechCrunch/'})

feeds['venture_beat'] = []
feeds['venture_beat'].append({'name': 'vb_allfeeds', 'url': 'http://feeds.venturebeat.com/VentureBeat'})

feeds['wikinews'] = []
feeds['wikinews'].append({'name': 'wikinews_main', 'url': 'https://en.wikinews.org/w/index.php?title=Special:NewsFeed&feed=rss&categories=Published&notcategories=No%20publish%7CArchived%7cAutoArchived%7cdisputed&namespace=0&count=15&ordermethod=categoryadd&stablepages=only'})

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
	tempSize = min(30, (len(feedList)-i))
	tempList = feedList[i:(i+tempSize)]
	for ret in pool.imap(prepareCrawlfeed, tempList):
		pass
	i += tempSize
print("--- %s seconds ---" % round(time.time() - start_time, 2))