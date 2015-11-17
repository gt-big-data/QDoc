__author__ = 'steven'
from dbco import *
from datetime import datetime
import pytz


cursor = db.qdoc.find({"timestamp": {"$gt": 0.0}})

for document in cursor:
    ts = document.get("timestamp")
    
    db.qdoc.update_many(
        {"timestamp": ts},
        {
            "$rename": {"timestamp": "date"}
        }
    )

    db.qdoc.update_many(
        {"date": ts},
        {
            "$set": {"timestamp": datetime.fromtimestamp(ts).replace(tzinfo=pytz.utc)},
        }
    )
