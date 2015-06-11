from dbco import *
from urllib import urlopen
from bs4 import BeautifulSoup
from crawlContent import *
from article import *
import sys

src = 'guardian'

# art = db.qdoc.find({'$query': {'source': src}, '$orderby': {'timestamp': -1}}).skip(1).limit(1)

reload(sys)
sys.setdefaultencoding('utf-8')

cont_old = ''
url = 'http://www.theguardian.com/environment/ng-interactive/2015/mar/16/the-biggest-story-in-the-world'
# for a in art:
# 	cont_old = a['content']
# 	url = a['url']

print url
art = [Article('blabla', "blabla2", url, 1431243710, src, src+"yolo")]
art = crawlContent(art)

soup_old = BeautifulSoup(cont_old, 'html.parser')

# with open(src+"_old.txt", "w") as f:
# 	f.write(soup_old.prettify())

soup_new = BeautifulSoup(art[0].content, 'html.parser')

with open(src+"_new.txt", "w") as f:
	f.write(soup_new.prettify())
