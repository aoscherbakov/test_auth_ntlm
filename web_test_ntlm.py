#!/usr/bin/python

import pycurl
import ConfigParser
from StringIO import StringIO

Config = ConfigParser.ConfigParser()
Config.read("config.conf")

def read_conf(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def auth_test(username, password, address):
	curl_buffer = StringIO()
	curl = pycurl.Curl()
	curl.setopt(curl.URL, address)
	curl.setopt(curl.HTTPAUTH, curl.HTTPAUTH_NTLM)
	curl.setopt(curl.USERPWD, "{}:{}".format(username, password))
	curl.setopt(curl.FOLLOWLOCATION, True)
	curl.setopt(curl.WRITEDATA, curl_buffer)
	curl.perform()
	curl.close()
	return curl_buffer.getvalue()

username = read_conf("Main")["username"]
password = read_conf("Main")["password"]
url = read_conf("Main")["url"]

res = auth_test(username, password, url)

if "Tech_fttb_acc" in res:
    print "OK"
else:
    print "Authorization Failed, Login: %s, URL: %s" % (username, url)
