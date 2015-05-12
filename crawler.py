from feedCrawl import *
import time

start_time = time.time()

sources = ['cnn', 'reuters', 'business_insider', 'venture_beat', 'techcrunch'] # 'financial_times'
# Sources to add:
	# Financial Times
	# Associated Press
	# NY Times

feeds = {}

feeds['cnn'] = [] # http://edition.cnn.com/services/rss/
feeds['cnn'].append({'name': 'cnn_world', 'url': 'http://rss.cnn.com/rss/edition_world.rss'})
feeds['cnn'].append({'name': 'cnn_technology', 'url': 'http://rss.cnn.com/rss/edition_technology.rss'})
feeds['cnn'].append({'name': 'cnn_science', 'url': 'http://rss.cnn.com/rss/edition_space.rss'})
feeds['cnn'].append({'name': 'cnn_entertainment', 'url': 'http://rss.cnn.com/rss/edition_entertainment.rss'})
feeds['cnn'].append({'name': 'cnn_sport', 'url': 'http://rss.cnn.com/rss/edition_sport.rss'})
feeds['cnn'].append({'name': 'cnn_travel', 'url': 'http://travel.cnn.com/rss.xml'})
feeds['cnn'].append({'name': 'cnn_us', 'url': 'http://rss.cnn.com/rss/edition_us.rss'})

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

feeds['business_insider'] = [] # http://www.businessinsider.in/rss_feeds.cms
feeds['business_insider'].append({'name': 'bi_allfeeds', 'url': 'http://www.businessinsider.in/rss_section_feeds/2147477994.cms'})

feeds['venture_beat'] = []
feeds['venture_beat'].append({'name': 'vb_allfeeds', 'url': 'http://feeds.venturebeat.com/VentureBeat'})

feeds['techcrunch'] = []
feeds['techcrunch'].append({'name': 'tc_allfeeds', 'url': 'http://feeds.feedburner.com/TechCrunch/'})

# feeds['financial_times'] = [] # not possible, "not free"
# feeds['financial_times'].append({'name': 'ft_world', 'url': 'http://www.ft.com/rss/world'})
# feeds['financial_times'].append({'name': 'ft_companies', 'url': 'http://www.ft.com/rss/companies'})
# feeds['financial_times'].append({'name': 'ft_arts', 'url': 'http://www.ft.com/rss/arts'})

for source in sources:
	for feed in feeds[source]:
		crawlFeed(source, feed['name'], feed['url'])

print("--- %s seconds ---" % round(time.time() - start_time, 2))