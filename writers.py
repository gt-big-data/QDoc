from os import mkdir
import re, json

class PrintWriter(object):
    """Class for writing JSON data to the screen."""

    def write(self, article):
        """Write an Article object to the screen.

        Arguments:
        article -- An Article object.
        """
        json_data = json.dumps(article.__dict__, indent=4).encode('utf-8')
        print(json_data)

class FileWriter(object):
    """Class for writing JSON data to a file."""

    def __init__(self):
        check_and_make_dir("./test_files/")

    def write(self, article):
        """Write an Article object to a file.

        Arguments:
        article -- An Article object.
        """
        filename = re.sub(r'\W', '_', article.guid) + ".json"

        try:
            filepath = "test_files/" + filename
            pretty_string = json.dumps(article.__dict__, indent=4).encode('utf-8')
            with open(filepath, 'w') as output_file:
                output_file.write(pretty_string)
        except:
            print(article.title)
            raise

def check_and_make_dir(path):
    """Makes a directory if it doesn't already exist.

    Arguments:
    path -- The path to try creating.
    """
    try:
        mkdir(path)
    except OSError:
        pass

class MongoWriter():
    def __init__(self):
        from dbco import db
        self.db = db

    def write(self, article):
        """Write an Article object to MongoDB.
        Arguments:
        article -- An Article object.
        """
        self.db.qdoc.update({'guid': article.guid}, {'$set': article.__dict__}, upsert=True)
    def updateDuplicate(self, dupID, article):
        self.db.qdoc.update({'_id': dupID}, {'$set': {'content': article.content}}) # update the content 