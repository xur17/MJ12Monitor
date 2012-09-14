## This class enables querying an MJ12 node, and getting values from it.
import urllib2
from BeautifulSoup import BeautifulSoup, Comment

class MJ12API:
	def __init__(self, ip, port, name="", username=False, password=False):
		'''Setup a connection to the node at the given address.'''
		self.name = name
		self.url = "http://" + ip + ":" + port
		if username:
			password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
			password_mgr.add_password(None, self.url, username, password)
			handler = urllib2.HTTPBasicAuthHandler(password_mgr)
			self.opener = urllib2.build_opener(handler)
		else:
			self.opener = urllib2.build_opener()

	def getName(self):
		return self.name

	def getCrawlingResults(self):
		try:
			table = self.__removePre( self.__getCrawlingResultsSoup() )
		except:
			return {'Uptime': '-1', 'Conn errors': '-1', 'Month Down Data': '-1', 'Platform': '', 'Other': '-1', 'Uploaded Data': '-1', 'Disallowed': '-1', 'Forbidden (403)': '-1', 'Banned': '-1', 'Overall Upload': '-1', 'Total URLs': '-1', 'Current Upload': '-1', 'Current Download': '-1', 'Timed out': '-1', 'Retries': '-1', 'Downloaded Data': '-1', 'Successes': '-1', 'Not found': '-1', 'Download Limit': '-1', 'DNS errors': '-1', 'MJ12node': '-1', 'Today Down Data': '-1', 'Upload Limit': '-1', 'Overall Download': '-1', 'Month Up Data': '-1', 'Today Up Data': '-1'}
		items = self.__clean(table)
		newDict = dict( item.split(":") for item in items.split("\n") if item)
		cleanedDict = {}
		for k,v in newDict.items():
			cleanedDict[k.rstrip().lstrip()] = self.__getNumber(v)
		return cleanedDict

	def __getNumber(self, text):
		'''Returns the number from the given text'''
		return text.split(' ')[0].replace(',', '')

	def __clean(self, soup):
		return soup.replace("\r", "").replace("\t", "")

	def __removePre(self, soup):
		return self.__getCrawlingResultsSoup().replace("<pre>", "").replace("</pre>", "")

	def __getCrawlingResultsSoup(self):
		html = self.opener.open(self.url + "/tools/MJ12Monitor.jhh", timeout=1)
		soup = html.read()
		return soup

