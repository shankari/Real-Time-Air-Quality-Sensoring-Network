from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from HTMLParser import HTMLParser
import pycurl
import simplejson as json
import ast
import requests
from StringIO import StringIO


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['GET'])
def index(request):
	"""
	Returns the metadata from quasar server
	"""
	if request.method == 'GET':
		return_json = json.loads(get_all_sensors())
		return Response(return_json)

@csrf_exempt
@api_view(['GET'])
def get_data_by_uuid(request, uuid):
	"""
	Returns the metadata from quasar server using uuid of the data
	TODO : This request must also take time period for which data is needed and reply the data in that time
	"""
	if request.method == 'GET':
		return_json = json.loads(get_data_by_uuid_helper(uuid))
		return Response(return_json)

@csrf_exempt
@api_view(['GET'])
def get_average_data_12_hrs(request, uuid):
	"""
	Returns the average of the data from the corresponding uuid of last 12 hrs
	"""
	if request.method == 'GET':
		parser = HTMLParser()
		uuid = parser.unescape(uuid)
		query_url = 'http://localhost:8079/api/query'
		query = "select data in (now -12h, now) where uuid='"+uuid+"'"
		r = requests.post(query_url, query)
		readings = json.loads(r.content)
		readings = readings[0]["Readings"]
		numObservation = 0
		totalAirQuality = 0
		for reading in readings:
			numObservation += 1
			totalAirQuality += reading[1]
		if numObservation!=0:
			return Response(totalAirQuality/numObservation)
		else:
			return Response("Data unavailable")

@csrf_exempt
@api_view(['POST'])
def post_sensor_data(request, key):
	"""
	Posts the data of the sensor to giles server
	"""
	if request.method == 'POST':
		giles_url = 'http://localhost:8079/add/MYAPIKEY'
		response = requests.post(giles_url, data=json.dumps(request.data))
		# print request.data
		return Response(response.content)

def get_all_sensors():
	"""
	Returns the data of all sensors
	"""
	query_url = 'http://localhost:8079/api/query'
	query = "select *"
	r = requests.post(query_url, query)
	return r.content

def get_data_by_uuid_helper(uuid):
	"""
	Returns the data of sensor specified by uuid of last 30 days
	TODO : Return the data given time and uuid both, right now only uuid is considered and by default last 30 days data is sent
	"""
	parser = HTMLParser()
	uuid = parser.unescape(uuid)
	query_url = 'http://localhost:8079/api/query'
	query = "select data in (now -30d, now) where uuid='"+uuid+"'"
	r = requests.post(query_url, query)
	return r.content
# Leave the rest of the views (detail, results, vote) unchanged