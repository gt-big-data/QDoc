# Quick and Dirty operating crawler

## Goal of QDoc:

From a few RSS feeds from the biggest News Sources, build a database of cleaned articles.


## New here?

Here's what you can do to get started:

* Clone our github, look at what we are working on, talk to us to see how you could help.
* Follow the installation guide
* Check out our issues on Github and get started.

## Installation Guide

### Install Python 2

If you're on OSX or Linux, you already have `Python 2`. Run `python -V` in terminal and make sure that you're at least on `2.7`.

If you're on Windows, [download it](https://www.python.org/downloads/) from python.org. **Make sure to pick a `2` version and not a `3` version**.

### Install pip

If you're on OSX or Linux, you already have `pip` installed.

If you're on Windows, you might already have `pip` (or not). Go to `C:\python27\Scripts` and see if `pip.exe` is there. If it is, you already have `pip`.

If you don't, [download and install it](https://pip.pypa.io/en/latest/installing/).

You should also [add `pip` to your path](https://java.com/en/download/help/path.xml). For Windows, add `;C:\python27\Scripts` to the end of it.

### Install Mongo

Out of the box, computers generally don't ship with Mongo. Unless you know you've already installed it, you probably don't have it.

Windows and OSX: [Download and install it](https://www.mongodb.org/downloads#production)

Linux: Download and install a binary from the above link or [setup your package manager](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/) to install it. If you don't know which option to use, try setting it up with your package manager.

You also need to create the directory `/data/db`. This is where Mongo stores its data.

* OSX and Linux: `sudo mkdir -p -m 777 /data/db`
* Windows: Create the folder `C:\data` and then create the folder `C:\data\db`.

If you're on Windows, you'll also need to add Mongo to your path. It's probably located at `C:\mongodb\bin\` or `C:\Program Files\mongodb\bin`.

### Install Our Python Dependencies

Only up a terminal in this project's root directory (the folder this file is in). Then type:

    pip install -r requirements.txt

If that complains about directories not being writable (probably on OSX and Linux), type `sudo pip install -r requirements.txt` instead.

## Run the Crawler!

### Run a Local MongoDB Instance

If all of the setup stuff worked, just type `mongod` in a terminal window and you're good to go. You'll need to leave that window open in the background while you do stuff with the crawler.

### Point the Crawler to Your Local Database

By default, the crawler is pointing to the production database (this will be changed pretty soon). In the meantime, open up `dbco.py` in your text [editor of choice](https://atom.io/) and change line 4 to this:

    client = MongoClient('mongodb://127.0.0.1:27017/')

### Load the feeds from the real database

We now store the list of feeds to crawl from the production database. To get them, open up `mongo` (make sure `mongod` is still running in a separate window).

    mongo

Then switch to the `big_data` database. This is where we store all of our data. Mongo automatically makes databases that don't exist so there's no special procedure for making a new database.

    use big_data

Finally, copy the `feeds` collection from the production database to your local database.

    db.cloneCollection('api.retinanews.net', 'feed')

### Actually Run the Crawler!

    python crawler.py

The first time you run it (or the first time you run it in a while), it will take a few minutes to finish.

To check if everything's working, open up a terminal and type the following:

1. `mongo` - That will run an interactive shell that connects to your local MongoDB.
2. `use big_data` - That connects you to the database where we store all of the crawled articles.
3. `db.qdoc.findOne()` - That will split out any article in the `qdoc` collection (table).

If the last command prints out a lot of text and it looks like a news article, congrats! Otherwise, talk to someone in the `Contact` section for help.

## Contact:

If you have any questions, feel free to talk to Sam (smarder3@gatech.edu) or Matt (mersted@gatech.edu).

Also, Philippe (plaban3@gatech.edu) originally created the crawler. You should ask him about any weird things you see in the code.
