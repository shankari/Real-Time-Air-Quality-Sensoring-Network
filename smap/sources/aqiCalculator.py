import requests
import simplejson as json

# used for logging
import logging
import sys, traceback
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost/raqmn_api/"

def init_aqi_drivers():
	"""
	Used to initialize AQI Driver
	Returns all the dylos sensors available with their serial number and uuid
	"""
	try:
		data = json.loads(requests.get(BASE_URL).content)
		dylosSensors = {}
		for datum in data:
			try:
				pathParts = datum['Path'].split("/") 
				if len(pathParts)==4 and pathParts[1].strip()=="dylos":
					dylosSensors[pathParts[2].strip()+"/"+pathParts[3].strip()] = datum['uuid']
					get_aqi_data(1, datum['uuid'],pathParts[3].strip())
			except:
				logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
				logging.debug("Traceback : "+ str(traceback.format_exc()))
		logging.debug(dylosSensors)
		return dylosSensors
	except:
		logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
		logging.debug("Traceback : "+ str(traceback.format_exc()))
        return {}

def get_aqi_data(hours,uuid,type):
	"""
	Returns the AQI for number of hours given for the sensor mentioned by uuid
	"""
	try:
		data = json.loads(requests.get(BASE_URL+"data/"+str(hours)+"h/"+uuid+"/").content)
		dataPoints = remove_outliers([x[1] for x in data])
		average = float(sum(dataPoints))/len(dataPoints) if len(dataPoints) > 0 else 0
		logging.debug(uuid+"/"+str(hours)+"h: "+str(average))
		aqi = convert_particle_count_to_aqi(average, type)
		return aqi
	except:
		logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
		logging.debug("Traceback : "+ str(traceback.format_exc()))
        return 0

def remove_outliers(data):
	"""
	Removes outliers from timeseries data given
	TODO: This function uses a very simple trimming algorithm for removing outliers. Need a more robust algorithm for timeseries data to remove outliers
	"""
	data.sort()
	numPointsToRemove = (5*len(data))/100
	return data[numPointsToRemove:len(data)-numPointsToRemove]

def convert_particle_count_to_aqi(average, type):
	"""
	Converts particle count in number of particles
	References:
	* http://www.fijnstofmeter.com/documentatie/Data-Validation.pdf
	* http://www.indiaenvironmentportal.org.in/files/file/Air%20Quality%20Index.pdf
	TODO: Use proper measurement of humidity to convert by using proper corrections, currently average correction value of 1.5 is used
	TODO: Validation of correction factor and creating our own
	TODO: PM10 conversion needs to be improved with help of data
	"""
	iHigh = 0
	iLow = 0
	bHigh = 0
	bLow = 0
	iPoints = [0,50,100,200,300,400,500]
	bPoints = []
	cp = 0
	if(type=="pm2.5"):
		bPoints = [0,30,60,90,120,250,350]
		cp = average*3531.5*0.000000589
		cp = cp*1.5 # correction value
	elif(type=="pm10"):
		bPoints = [0,50,100,250,350,430,550]
		cp = average*3531.5*0.000121
		cp = cp # correction value not used as no evidence found for same correction values for PM10
	for i in range(len(bPoints)):
		if(cp<=bPoints[i]):
			iHigh = iPoints[i]
			iLow = iPoints[i-1]
			bHigh = bPoints[i]
			bLow = bPoints[i-1]
			break
	if(iHigh == 0 and iLow == 0):
		iHigh = iPoints[len(bPoints)-1]
		iLow = iPoints[len(bPoints)-2]
		bHigh = bPoints[len(bPoints)-1]
		bLow = bPoints[len(bPoints)-2]
	return int(((iHigh-iLow)*(cp-bLow))/(bHigh-bLow)+iLow)
