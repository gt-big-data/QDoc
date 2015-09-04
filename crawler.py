# TODO: Figure out what these IPs and ranges are for and then probably delete them.
#128.0.0.0/8, 143.0.0.0/8, 10.0.0.0/8, 127.0.0.0/8, 24.98.127.49, 130.211.151.156, 98.251.6.21, 130.211.122.221
from feedCrawl import *
import time

start_time = time.time()

# TODO: Remove need for this array. Should be inferred from the feeds object.
sources = ['cnn', 'reuters', 'business_insider', 'venture_beat', 'techcrunch', 'bbc', 'guardian', 'aljazeera', 'france24']
# sources = ['france24']
# GUID Available: (Globally Unique IDentifier)
	# CNN: Yes
	# Reuters: Yes
	# Business Insider: Yes
	# VentureBeat: Yes
	# TechCrunch: Yes
	# BBC: Yes
	# Guardian: Yes

# Sources to add:
	# Associated Press
	# NY Times
	# EuroNews
	# AFP
	# Anadolu Agency
	# The Independent
	# UberGizmo
	# RUssia Today

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

feeds['bbc'] = []
feeds['bbc'].append({'name': 'bbc_world', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml'})
feeds['bbc'].append({'name': 'bbc_business', 'url': 'http://feeds.bbci.co.uk/news/business/rss.xml'})
feeds['bbc'].append({'name': 'bbc_politics', 'url': 'http://feeds.bbci.co.uk/news/politics/rss.xml'})
feeds['bbc'].append({'name': 'bbc_science', 'url': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'})
feeds['bbc'].append({'name': 'bbc_technology', 'url': 'http://feeds.bbci.co.uk/news/technology/rss.xml'})
feeds['bbc'].append({'name': 'bbc_entertainment', 'url': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml'})

feeds['guardian'] = []
feeds['guardian'].append({'name': 'gua_world', 'url': 'http://www.theguardian.com/world/rss'})
feeds['guardian'].append({'name': 'gua_politics', 'url': 'http://www.theguardian.com/politics/rss'})
feeds['guardian'].append({'name': 'gua_politics', 'url': 'http://www.theguardian.com/culture/rss'})
feeds['guardian'].append({'name': 'gua_business', 'url': 'http://www.theguardian.com/business/rss'})
feeds['guardian'].append({'name': 'gua_environment', 'url': 'http://www.theguardian.com/environment/rss'})
feeds['guardian'].append({'name': 'gua_travel', 'url': 'http://www.theguardian.com/travel/rss'})

feeds['aljazeera'] = []
feeds['aljazeera'].append({'name': 'alj_allfeeds', 'url': 'http://america.aljazeera.com/content/ajam/articles.rss'})

feeds['france24'] = []
feeds['france24'].append({'name': 'f24_livenews', 'url': 'http://www.france24.com/en/timeline/rss'})

for source in sources:
    for feed in feeds[source]:
        crawlFeed(source, feed['name'], feed['url'])

print("--- %s seconds ---" % round(time.time() - start_time, 2))