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



1. Run `python crawler.py`.

Contact:
===========

* plaban3@gatech.edu
* smarder3@gatech.edu
* mersted@gatech.edu
