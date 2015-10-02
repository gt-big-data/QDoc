<<<<<<< HEAD

=======
from article import *
from crawlContent import *
from dbco import *
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

art = db.qdoc.find({'$query': {'keywords': 'google plus'}, '$orderby': {'timestamp': -1}}).limit(1)
i = 0
for a in art:
	print a['keywords']
	print datetime.datetime.fromtimestamp(int(a['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
	i += 1
	arti = [Article(a['_id'], a['title'], a['url'], a['timestamp'], a['source'], a['feed'])]
	arti = crawlContent(arti)
	soup_new = BeautifulSoup(arti[0].content, 'html.parser')
	with open(arti[0].source+"_new.txt", "w") as f:
		f.write(soup_new.prettify())
>>>>>>> a8d78967a592eb153d8ba6de1648f11042aea64f
