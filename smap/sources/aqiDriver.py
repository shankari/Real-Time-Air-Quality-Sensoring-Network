from smap.driver import SmapDriver
from smap.util import periodicSequentialCall
from smap.contrib import dtutil
from aqiCalculator import init_aqi_drivers, get_aqi_data

# logging
import sys, traceback
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AQIDriver(SmapDriver):
	"""
	This Driver computes hourly average of data from Dylos Sensors and converts it to AQI and posts it to server
	"""
	def setup(self, opts):
		self.rate = int(opts.get('Rate', 3600))
		self.dylosSensors = init_aqi_drivers()
		for key, value in self.dylosSensors.iteritems():
			dylosAQIDriver = self.add_timeseries("/"+key,'AQI',description='Air Quality Index - India')
			
	def start(self):
		self.process = periodicSequentialCall(self.read)
		self.process.start(self.rate)

	def read(self):
		"""
		Reads the data giving time and uuid
		"""	
		for key, value in self.dylosSensors.iteritems():
			aqi = get_aqi_data(1,value,key.split("/")[1].strip())
			if (aqi>0):
				logging.debug(key+" : "+str(aqi))
				self.add("/"+key,aqi)