#!/usr/bin/python

import sys,os,traceback
import pycurl
import ConfigParser
import argparse
from StringIO import StringIO


#for verbose out
def verbose_except(e):
       print str(e)
       traceback.print_exc()

#main test function
def auth_test(username, password, address):
	curl_buffer = StringIO()
	curl = pycurl.Curl()
	curl.setopt(curl.URL, address)
	curl.setopt(curl.HTTPAUTH, curl.HTTPAUTH_NTLM)
	curl.setopt(curl.USERPWD, "{}:{}".format(username, password))
	curl.setopt(curl.FOLLOWLOCATION, True)
	curl.setopt(pycurl.CONNECTTIMEOUT, int(timeout))
	curl.setopt(curl.WRITEDATA, curl_buffer)
	try:
		curl.perform()
	except Exception, e:
		print "Error to perform curl auth request"
		if args.verbose: verbose_except(e)
		os._exit(2)

	curl.close()
	user = username.split('@')
	#return web page
	if user[0] in curl_buffer.getvalue(): return True

if __name__ == '__main__':
    try:   
	parser = argparse.ArgumentParser(description="test web authorization using NTLM")
	parser.add_argument('host', type=str, help='hostname or ip for auth test')
	parser.add_argument('-v','--verbose', action='store_true', default=False, help='verbose output')
	parser.add_argument('-c','--config', help='config file')
	parser.add_argument('-t','--timeout', type=int, help='connection timeout')
	parser.add_argument('-u','--username', type=str, help='login for auth')
	parser.add_argument('-p','--password', type=str, help='password for auth')
	args = parser.parse_args()
	
	Config = ConfigParser.SafeConfigParser({'username':'no username specified','password':'no password specified','timeout': '5'})
	
	if args.config:
		Config.read(args.config)
	else:
		Config.add_section('Main')


	result = []

	#if variable in command argument, ignore config file
	for section in Config.sections():

		if args.timeout: 
			timeout = args.timeout
		else:
			timeout = Config.get(section,'timeout')
		
		if args.username and not args.config:
			username = args.username
		else:
			username = Config.get(section, 'username')

		if args.password and not args.config:
			password = args.password
		else:
			password = Config.get(section, 'password') 

		url = "http://" + args.host
	
		
		#check all config sections	
		if auth_test(username, password, url) == True:
			result.append(section+" auth is OK")
		else:
#			result.append(section+" authorization failed, Login: %s, URL: %s" % (username, url))
			result.append(section+" authorization failed")
		
	#print result
	fail = False
	for res in result:
		if "failed" in res:
			fail = True
		print res
	
	if fail == True:
		exit(2)
	else:
		exit(0)

	#exception section
    except KeyboardInterrupt, e: # Ctrl-C
       raise e
    except SystemExit, e: # sys.exit()
       raise e
    except Exception, e:
       print 'Error, UNEXPECTED EXCEPTION'
       if args.verbose: verbose_except(e)
       os._exit(2)

