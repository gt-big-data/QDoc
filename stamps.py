"""Load and save etags from RSS feeds."""

import os

def loadLastStamp(name):
    """Load a timestamp from a RSS feed name.

    This name should be consistent with `saveLastStamp`.

    Arguments:
    name -- The name of the feed used to save the timestamp.
    """
    path = 'stamps/'+name+'.txt'
    if os.path.isfile(path):
        # TODO: Convert to `with` syntax.
        f = open(path)
        txt = f.read()
        return float(txt)
    return 0

def saveLastStamp(name, stamp):
    """Save a timestamp from an RSS feed for later.

    This name should be consistent with `loadLastStamp`.

    Arguments:
    name -- The name of the feed to save.
    stamp -- The timestamp to store with the RSS feed.
    """
    path = 'stamps/' + name + '.txt'
    # TODO: Convert to `with` syntax.
    f = open(path,'w')
    f.write(str(stamp))