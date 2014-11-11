#!/usr/bin/python

import sys,os,traceback
import pycurl
import ConfigParser
import argparse
from StringIO import StringIO



def verbose_except(e):
       print str(e)
       traceback.print_exc()

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
	try:
		curl.perform()
	except Exception, e:
		print "Error to perform curl auth request"
		if args.verbose: verbose_except(e)
		os._exit(2)

	curl.close()
	if username in curl_buffer.getvalue(): return True

if __name__ == '__main__':
    try:   
	parser = argparse.ArgumentParser(description="test web authorization using NTLM")
	parser.add_argument('host', type=str, help='hostname or ip for auth test')
	parser.add_argument('-v','--verbose', action='store_true', default=False, help='verbose output')
	parser.add_argument('-c','--config', help='config file', required = True)
	args = parser.parse_args()
	
	Config = ConfigParser.ConfigParser()
	Config.read(args.config)

	username = read_conf("Main")["username"]
	password = read_conf("Main")["password"]
	url = "http://" + args.host

	if auth_test(username, password, url) == True:
		print "OK"
		exit(0)
	else:
		print "Authorization Failed, Login: %s, URL: %s" % (username, url)
		exit(2)

    except KeyboardInterrupt, e: # Ctrl-C
       raise e
    except SystemExit, e: # sys.exit()
       raise e
    except Exception, e:
       print 'Error, UNEXPECTED EXCEPTION'
       if args.verbose: verbose_except(e)
       os._exit(2)

