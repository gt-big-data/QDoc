# NOTE: Running this script requires numpy which is not listed in our project's requirements.
# It is a pain to install on Windows without Anaconda and therefore will not be added any time soon.

import db
import numpy as np
import time

ONE_SECOND = 1000
ONE_MINUTE = ONE_SECOND * 60
ONE_HOUR = ONE_MINUTE * 60
ONE_DAY = ONE_HOUR * 24

def setCrawlTimeOnNewFeeds(default):
    db.feed.update_all({'crawlFreq': {'$exists': False}}, {'crawlFreq': default})

def updateCrawlTimes(defaultTime):
    shouldUpdate = False
    feedUpdate = db.feed.initialize_unordered_bulk_op()

    match = {'$match': {'timestamp': {'$gte': time.time()-30*86400}}}
    sort = {'$sort': {'timestamp': 1}}
    group = {'$group': {'_id': '$feed', 'tsVec': {'$push': '$timestamp'}, 'count': {'$sum': 1}}}
    for d in db.qdoc.aggregate([match, sort, group]):
        # print d
        updateFrequency = defaultTime # By default: update every 8 minutes
        if d['count'] > 1:
            diffVec = np.diff(d['tsVec'])
            diffVec = map(lambda x: x.total_seconds() * 1000, diffVec)

            # We want to get 90% of the cases considered
            updateFrequency = np.percentile(diffVec, 10)

            # update at most every 2 minutes, at least once per hour
            updateFrequency = int(min(max(updateFrequency, ONE_MINUTE * 2), ONE_HOUR))

        # For historical reasons, updateFrequency needs to be in seconds (not milliseconds).
        updateFrequency /= 1000

        print('Updating the crawl frequency of %s to once per %d seconds.' % (d['_id'], updateFrequency))
        feedUpdate.find({'feed': d['_id']}).update({'$set': {'crawlFreq': updateFrequency}})
        shouldUpdate = True

    if shouldUpdate: feedUpdate.execute()

if __name__ == '__main__':
    # Because Phillipe says so, update all feeds every 8 minutes by default.
    defaultTime = ONE_MINUTE * 8
    updateCrawlTimes(defaultTime)
