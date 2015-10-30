from django.shortcuts import render
import requests
import json

# Create your views here.
from django.http import HttpResponse

def index(request):
	metadata = requests.get('http://localhost:8000/raqmn_api/')
	metadata = json.loads(metadata.text)
	i = 3
	uuid = metadata[i]['uuid']
	data = {}
	data['lat'] = metadata[i]["Metadata"]["Latitude"]
	data['long'] = metadata[i]["Metadata"]["Longitude"]
	data['area'] = metadata[i]["Metadata"]["Area"]
	air_quality_data = requests.get('http://localhost:8000/raqmn_api/data/'+uuid)
	data['aqi'] = json.loads(air_quality_data.text)[0]['Readings']
	# print data
	return render(request, 'raqmn_data/plot.html', data)

