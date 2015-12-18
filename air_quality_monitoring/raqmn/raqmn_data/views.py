from django.shortcuts import render
import requests
import simplejson as json
import raqmn_api.views as raqmn_api

# Create your views here.
from django.http import HttpResponse

def index(request):
	"""
	This acts as a testing platform for using different plottig libraries
	TODO : Create a visualization or inforgraphic site for data collected by raqmn project
	"""
	metadata = json.loads(raqmn_api.get_all_sensors())
	i = 3
	uuid = metadata[i]["uuid"]
	data = {}
	data['lat'] = metadata[i]["Metadata"]["Latitude"]
	data['long'] = metadata[i]["Metadata"]["Longitude"]
	data['area'] = metadata[i]["Metadata"]["Area"]
	air_quality_data = raqmn_api.get_data_by_uuid_helper(uuid)
	data['aqi'] = json.loads(air_quality_data)[0]['Readings']
	# print data
	return render(request, 'raqmn_data/plot.html', data)

