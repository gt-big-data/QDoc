# -*- coding: utf-8 -*-
from dbco import *
import sys

def avgNbEntities():
	match = {'$match': {'entities': {'$exists': True}}}
	proj = {'$project': {'entCount': {'$size': '$entities'}}}
	group = {'$group': {'_id': '$entCount', 'count': {'$sum': 1}}}
	sort = {'$sort': {'_id': 1}}

	each = list(db.qdoc.aggregate([match, proj, group, sort]))
	avg = 0.0; total = 0.0
	for e in each:
		avg += e['count']*e['_id']
		total += e['count']
	avg /= total
	print avg

def popularKeywords():
	match = {'$match': {'keywords': {'$exists': True, '$ne': []}}}
	unwind = {'$unwind': '$keywords'}
	group = {'$group': {'_id': '$keywords', 'count': {'$sum': 1}}}	
	sort = {'$sort': {'count': -1}}
	limit = {'$limit': 100}

	ret = list(db.qdoc.aggregate([match, unwind, group, sort, limit]))
	for r in ret:
		print r

def popularEntities():
	match = {'$match': {'entities': {'$exists': True, '$ne': []}}}
	unwind = {'$unwind': '$entities'}
	group = {'$group': {'_id': '$entities.wdid', 'text': {'$first': '$entities.text'}, 'count': {'$sum': 1}}}	
	sort = {'$sort': {'count': -1}}
	limit = {'$limit': 100}

	ret = list(db.qdoc.aggregate([match, unwind, group, sort, limit]))
	for r in ret:
		print r

def contentRegexSource(st):
	match = {'$match': {'content': {'$regex': st}}}
	group = {'$group': {'_id': '$source', 'count': {'$sum': 1}}}
	sort = {'$sort': {'count': -1}}

	ret = list(db.qdoc.aggregate([match, group, sort]))
	for r in ret:
		print r

	print [a['_id'] for a in list(db.qdoc.find(match['$match'], {'_id': 1}).sort('timestamp', -1).limit(10))]

def kw(st):
	match = {'$match': {'keywords': st}}
	group = {'$group': {'_id': '$source', 'count': {'$sum': 1}}}
	sort = {'$sort': {'count': -1}}

	ret = list(db.qdoc.aggregate([match, group, sort]))
	for r in ret:
		print r

	print [a['_id'] for a in list(db.qdoc.find(match['$match'], {'_id': 1}).sort('timestamp', -1).limit(10))]

def recrawlRegex(st):
	print db.qdoc.update({'content': {'$regex': st}}, {'$set': {'recrawl': True}}, multi=True)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf8') # magic sauce

	if len(sys.argv) > 1:
		if sys.argv[1] == 'avgEntity':
			avgNbEntities()
		elif sys.argv[1] == 'popKeyword':
			popularKeywords()
		elif sys.argv[1] == 'popEntity':
			popularEntities()
		elif sys.argv[1] == 'contRegex':
			contentRegexSource(sys.argv[2])
		elif sys.argv[1] == 'recrawlRegex':
			recrawlRegex(sys.argv[2])
		elif sys.argv[1] == 'kw':
			kw(sys.argv[2])
	else:
		print "python fun.py avgEntity"
		print "python fun.py popEntity"
		print "python fun.py contRegex Reuters"
		print "python fun.py recrawlRegex Reuters"