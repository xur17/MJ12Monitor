from MJ12API import *
from configobj import ConfigObj
import time

###################

def getTotalUrls(data):
	return int( data['Total URLs'] )

def getCurDownload(data):
	return int( data['Current Download'] )

def getOverallDownload(data):
	return int( data['Overall Download'] )

def getServers(configFile):
	'''Creates the file objects from the given config file'''
	config = ConfigObj('settings.conf')
	servers = []
	for server in config:
		if "username" in config[server]:
			username = config[server]['username']
		else:
			username = False
		if "password" in config[server]:
			password = config[server]['password']
		else:
			password = False
		ip = config[server]['ip']
		port = config[server]['port']
		new = MJ12API(ip, port, server, username, password)
		servers.append(new)
	return servers

####### Main Part #################
servers = getServers('settings.conf')

oldUrls = 0

while True:
	theSum = 0
	overall = 0
	outputBuffer = ""
	outputBuffer += "\n%20s\t%10s\t%10s\n" % ("Server", "Cur Speed", "Overall Speed")
	for server in servers:
		data = server.getCrawlingResults()
		newUrls = getTotalUrls(data)
		outputBuffer += "%20s:\t%5d kbps\t%5d kbps\n" % (server.getName(), getCurDownload(data), getOverallDownload(data))
		#print newUrls - oldUrls
		oldUrls = newUrls
		theSum += getCurDownload(data)
		overall += getOverallDownload(data)
	outputBuffer += "%20s:\t%5d kbps\t%5d kbps" % ("Sum", theSum, overall)
	print outputBuffer
	time.sleep(5)

