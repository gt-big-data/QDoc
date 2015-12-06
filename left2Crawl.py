from dbco import *

match = {'$match': {'recrawled': {'$exists': False}}}
group = {'$group': {'_id': '$source', 'count': {'$sum': 1}}}
sort = {'$sort': {'count': -1}}

recrawls = list(db.qdoc.aggregate([match,group,sort]))
print recrawls

print sum([r['count'] for r in recrawls])