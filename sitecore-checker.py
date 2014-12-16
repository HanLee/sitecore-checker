#!/usr/bin/python
import sys
from sys import version_info
import urllib2

collection = {

'Accessible debug URLs': ['/sitecore/debug/default.aspx'],
'Accessible web service URLs': ['/sitecore/shell/webservice/service.asmx'],
'XML files can be downloaded (sample)': ['/sitecore/shell/applications/shell.xml'],
'XSLT files can be downloaded (sample)': ['/xsl/system/webedit/hidden%20rendering.xslt'],
'Accessible administrative URLs': ['/sitecore/admin/cache.aspx',
'/sitecore/admin/dbbrowser.aspx',
'/sitecore/admin/login.aspx',
'/sitecore/admin/restore.aspx',
'/sitecore/admin/serialization.aspx',
'/sitecore/admin/showconfig.aspx',
'/sitecore/admin/stats.aspx',
'/sitecore/admin/unlock_admin.aspx',
'/sitecore/admin/updateinstallationwizard.aspx',
'/sitecore/admin/wizard/installupdatepackage.aspx']

}

if( len(sys.argv) < 2):
	print '[*] Usage: ' + sys.argv[0] + ' ' + 'http://www.yourURLhere.com/'
else:
	url = sys.argv[1]
	valid_status_code = None
	invalid_status_code = None

	#first check for the default status code for a valid url
	try:
		response = urllib2.urlopen(url)
		valid_status_code = response.getcode()
	except urllib2.HTTPError, e:
		if e.code:
			print '[info] The url you provided appears to be returning ' + str(e.code) + ' , is this correct?'
			py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2
			user_response = None
			while True:
				if py3:
	                                user_response = input("y/n: ")
       		                else:
                                	user_response = raw_input("y/n: ")

				if user_response.strip() == 'y' or user_response.strip() == 'n':
					break

			if user_response == 'y':
				print '[info] proceeding with test even though provided URL returns status ' + str(e.code)
				valid_status_code = e.code
			elif user_response == 'n':
				print 'invalid url inputted, quitting.'
				exit()

	#secondly check for the default status for URLs that dont exist
	try:
		random_filename = '/f7348fh3j.aspx'
		random_file_url = url + random_filename
                response = urllib2.urlopen(url + random_file_url)
                invalid_status_code = response.getcode()

        except urllib2.HTTPError, e:
                if e.code:
                        print '[info] random file check with ' + random_file_url + ' returned status ' + str(e.code)
			invalid_status_code = e.code

	if(valid_status_code == invalid_status_code):
		print '[warning] Both valid and invalid URLs return the same status code, I will not be able to identify if the pages of interest are properly loaded'
		print 'Would you like me to list out the pages of interest for manual verification?'
		while True:
			if py3:
				user_response = input("y/n: ")
			else:
				user_response = raw_input("y/n: ")

			if user_response.strip() == 'y' or user_response.strip() == 'n':
				break

		if user_response == 'y':
			for key in collection:
				payloads = collection[key]
				for payload in payloads:
						print url+payload
		elif user_response == 'n':
			print 'cya!'
			exit()
	else:
		print '[info] Valid URLs and invalid URLs return status code ' + str(valid_status_code) + ' and ' + str(invalid_status_code) + ' respectively, using ' + str(valid_status_code) + ' as baseline to check for access to test pages'
		for key in collection:
			print "\nChecking for " + key
			payloads = collection[key]
			for payload in payloads:
				full_url =  url+payload
				found = False
				try:
					response = urllib2.urlopen(full_url)
					if response.getcode() == valid_status_code:
						found = True
				except urllib2.HTTPError, e:
					#in case of weird status code being returned for valid pages
					if e.code == valid_status_code:
						found = True

				if found:
					print '\t[y] ' + full_url
				else:
					print '\t[n] ' + full_url

