#!/usr/bin/python3
#
# new-xkcd-slack
#
# Created by Jack Hughes (github.com/jackhughesweb)
# Licensed under the MIT License
#

import feedparser
import os.path
import pycurl
import urllib
import json
import re

## Set these
slackhookurl = ''
botname = 'xkcdbot'
boticonurl = ''
##

def newxkcd(entry):
	xkcdtitle = entry.title
	xkcdlink = entry.link
	xkcddesc = entry.description
	xkcdimg = re.search('(?<=src=")[^"]*', xkcddesc).group(0)
	xkcdalt = re.search('(?<=alt=")[^"]*', xkcddesc).group(0)
	c = pycurl.Curl()
	c.setopt(c.URL, slackhookurl)
	postdataraw = {'attachments': [{'title': xkcdtitle, 'image_url': xkcdimg}], 'icon_url': boticonurl, 'username': botname}
	c.setopt(c.POSTFIELDS, json.dumps(postdataraw))
	c.perform()
	c.close()
	c = pycurl.Curl()
	c.setopt(c.URL, slackhookurl)
	postdataraw = {'attachments': [{'title': xkcdtitle, 'text': 'Alt text: ' + xkcdalt}], 'icon_url': boticonurl, 'username': botname}
	c.setopt(c.POSTFIELDS, json.dumps(postdataraw))
	c.perform()
	c.close()
	newfile = open('recent.txt', 'w')
	newfile.write(xkcdlink)
	newfile.close()


d = feedparser.parse('http://xkcd.com/rss.xml')
if os.path.isfile('recent.txt'):
	file = open('recent.txt', 'r')
	filelink = file.readline()
	file.close()
	if filelink != d.entries[0].link:
		newxkcd(d.entries[0])
else:
	newxkcd(d.entries[0])
