"""Load and save etags from RSS feeds."""

import os, time
from dbco import *

def loadLastStamp(name):
    """Load a timestamp from a RSS feed name.

    This name should be consistent with `saveLastStamp`.

    Arguments:
    name -- The name of the feed used to save the timestamp.
    """
    db_obj = list(db.rss_stamps.find({'feed': name}).limit(1))
    if len(db_obj) > 0:
        return db_obj[0]['stamp']
    return (time.time()-3600) # if we cannot find it, by default say it was an hour ago...

def saveLastStamp(name, stamp):
    """Save a timestamp from an RSS feed for later.

    This name should be consistent with `loadLastStamp`.

    Arguments:
    name -- The name of the feed to save.
    stamp -- The timestamp to store with the RSS feed.
    """
    db.rss_stamps.update({'feed': name}, {'feed': name, 'stamp': int(stamp)}, upsert=True)
