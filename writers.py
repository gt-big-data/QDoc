from os import mkdir
import json

class PrintWriter(object):
    """Class for writing JSON data to the screen."""

    def write(self, article):
        """Write an Article object to the screen.

        Arguments:
        article -- A JSON-serializable dictionary.
        """
        print(json.dumps(article.__dict__, indent=4, ensure_ascii=False))

class FileWriter(object):
    """Class for writing JSON data to a file."""

    def __init__(self):
        check_and_make_dir("./test_files/")

    def write(self, article):
        """Write an Article object to a file.

        Arguments:
        article -- A JSON-serializable dictionary.
        """
        filename = article.guid + ".json"

        try:
            filepath = "test_files/" + filename
            pretty_string = json.dumps(article.__dict__, indent=4)
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
    def __init__(self, host, port):
        from dbco import db

    def write(self, article):
        """Write an Article object to MongoDB.

        Arguments:
        article -- An article!
        """
        db.qdoc.update({'guid': article['guid']}, {'$set': article}, upsert=True)
