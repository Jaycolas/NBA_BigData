#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

import os
import urllib
import urllib2
import time

INVALID_STRING = 'Invalid String'
User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0"
headers = {'User-Agent': User_Agent}


def getCurrentTime():
	return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime() )

def createLogFileAndRedrect():
	# Redirect the stdout to log file
	CURRENT_PATH = os.getcwd()+'/'
	LOG_PATH = CURRENT_PATH + 'Log/'
	currentTime = getCurrentTime()
	LOG_FILE = LOG_PATH + currentTime + ".log"
	print LOG_FILE
	mkdir(LOG_PATH)
	LogFileHandler = open(LOG_FILE, 'w')
	sys.stdout = LogFileHandler


#Below function are mainly for basic utilities
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)

    if not isExists:
        #If not exist then create the directory
        print u"Creating ", path, u" folder"
        os.makedirs(path)
        return True
    else:
        #if path exist then do not create
        print u"path with name ", path, " has been created"
        return False

def getHtmlFromUrl(url):
    html = INVALID_STRING
    request = urllib2.Request(url)
    request.add_header('User-Agent', User_Agent)
    print "Now start to access "+url

    try:
        page = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason
    else:
        print "Geting Url "+url+" OK"
        html = page.read()
        # Now got the html content, write it to local file system
        return html

    return html

def saveFile(filePath, content):
    f = open(filePath, 'wb')
    f.write(content)
    f.close()

def openFile(filePath):
    f = open(filePath, 'rb')
    html = f.read()
    f.close()
    return html