from crawlContent import *
from article import *

# art = [Article('blabla', "In pension battle, Illinois governor faces constitutional fight", "http://reuters.us.feedsportal.com/c/35217/f/654214/s/462e01d5/sc/7/l/0L0Sreuters0N0Carticle0C20A150C0A50C10A0Cus0Eusa0Eillinois0Epension0Econstitution0Eana0EidUSKBN0ANV0AQN20A150A510A0DfeedType0FRSS0GfeedName0FpoliticsNews/story01.htm", 1431243710, "cnn", "cnn_world")]

# url = 'http://www.businessinsider.in/People-laughed-at-this-entrepreneurs-idea-now-its-a-500-million-business-thanks-to-his-mom/articleshow/47225163.cms?utm_source=ten_minutes_with&utm_medium=Referral&utm_campaign=Content_Patnership'
# source = 'business_insider'

url = 'http://www.cnn.com/2015/05/11/europe/eu-migrants-military-action/index.html'
source = 'cnn'
# url = 'http://reuters.us.feedsportal.com/c/35217/f/654214/s/462e01d5/sc/7/l/0L0Sreuters0N0Carticle0C20A150C0A50C10A0Cus0Eusa0Eillinois0Epension0Econstitution0Eana0EidUSKBN0ANV0AQN20A150A510A0DfeedType0FRSS0GfeedName0FpoliticsNews/story01.htm'
# source = 'reuters'

art = [Article('blabla', "In pension battle, Illinois governor faces constitutional fight", url, 1431243710, source, "cnn_world")]
art = crawlContent(art)