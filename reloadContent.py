from dbco import *
from crawlContent import *
import article
from article import *

print db.qdoc.find({'content': ''}).count()

art = db.qdoc.find({'content': ''})

for ar in art:
	a = [Article('blabla', "blabla2", ar['url'], 1431243710, 'cnn', "cnnyolo")]
	a = crawlContent(a)
	db.qdoc.update({'url': ar['url']}, {'$set': {'content': a[0].content}})
	# a[0].content