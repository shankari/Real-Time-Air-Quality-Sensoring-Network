from bs4 import BeautifulSoup	

import requests
import ast
import time
# used for logging
import logging
import sys, traceback
import simplejson as json
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# function that returns output of beautiful soup from a url
def get_web_page(url):
	web_page = requests.get(url)
	web_page_data = web_page.text
	content = BeautifulSoup(web_page_data, "lxml")
	return content

# gets the content from web page and curates it to get the string syntactically as a list
def get_content(url):
	safar_web_content = get_web_page(url)
	for script in safar_web_content.find_all('script', {'src': False}):
		if ('var markers' in script.text):
			content = script.text.strip()
			list_start = content.find('[')
			list_end = content.rfind(']')
			return content[list_start:list_end+1]

# gets the data of air quality and returns an array of dictionaries with data points 
def get_air_quality_data(opts):
	"""
	This function returns the data collected from the SAFAR Sensors and sends it to the drivers
	"""
	try:
		url = 'http://safar.tropmet.res.in/map_data.php?for=current&city_id=2'
		content = get_content(url)
		x = ast.literal_eval(content)
		air_quality_data = []
		for i in range(0, len(x)):
			try:
				air_quality_data_city ={}
				air_quality_data_city['area'] = x[i]['title']
				air_quality_data_city['latitude'] = x[i]['lat']
				air_quality_data_city['longtitude'] = x[i]['lng']
				area_web_data = BeautifulSoup(x[i]['description'], "lxml")
				data_list = []
				for data in area_web_data.find_all('td'):
					data_list.append(data.getText())
					# logging.debug(data.getText())
				air_quality_data_city['time'] = data_list[1]
				# air_quality_data_city['pm10'] = int(data_list[6])
				air_quality_data_city['pm2.5'] = int(data_list[9])
				# air_quality_data_city['pmno2'] = int(data_list[12])
				# air_quality_data_city['pmco'] = int(data_list[15])
				# air_quality_data_city['pmo3'] = int(data_list[18])
				air_quality_data.append(air_quality_data_city)
				# print air_quality_data_city
			except:
				logging.debug("Unexpected error for "+ str(i)+" : "+str(sys.exc_info()[0]))
				logging.debug("Traceback : "+ str(traceback.format_exc()))
		return air_quality_data
	except:
		logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
		logging.debug("Traceback : "+ str(traceback.format_exc()))
		air_quality_data = []
		return air_quality_data

def get_air_quality_init(opts):
	"""
	This function returns only the metadata about the sensors and hence even if the sensors are down you can setup the drivers for them.
	"""
	try:
		url = 'http://safar.tropmet.res.in/map_data.php?for=current&city_id=2'
		content = get_content(url)
		x = ast.literal_eval(content)
		air_quality_data = []
		for i in range(0, len(x)):
			try:
				air_quality_data_city ={}
				air_quality_data_city['area'] = x[i]['title']
				air_quality_data_city['latitude'] = x[i]['lat']
				air_quality_data_city['longtitude'] = x[i]['lng']
				air_quality_data.append(air_quality_data_city)
				# print air_quality_data_city
			except:
				logging.debug("Unexpected error for "+ str(i)+" : "+str(sys.exc_info()[0]))
				logging.debug("Traceback : "+ str(traceback.format_exc()))
		return air_quality_data
	except:
		logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
		logging.debug("Traceback : "+ str(traceback.format_exc()))
		air_quality_data = []
		return air_quality_data