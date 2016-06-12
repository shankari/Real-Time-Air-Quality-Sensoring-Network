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
def get_data_by_uuid(request, uuid, hours):
	"""
	Returns the data from quasar server using uuid of the data between now and (now - hours)
	TODO : This request must take time period in days,hours,minutes format for which data is needed and reply the data in that time
	"""
	if request.method == 'GET':
		readings = get_data_by_uuid_helper(uuid, hours)
		return Response(readings)

@csrf_exempt
@api_view(['GET'])
def get_average_by_uuid(request, uuid, hours):
	"""
	Returns the average of the data from the corresponding uuid of last 'hours' hrs
	"""
	if request.method == 'GET':
		readings = get_data_by_uuid_helper(uuid, hours)
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
	{"/safar/Colaba/pm2.5": {"uuid": "166ac024-ab8f-5f49-b29d-f7bf00199cee", "Readings": [[1456980268000, 186]]}, "/safar/Chembur/pm2.5": {"uuid": "020abd8f-5d4e-51d2-a6a1-4e1f84cf9041", "Readings": [[1456980268000, 186]]}, "/safar/Andheri/pm2.5": {"uuid": "3cd92d07-43f6-5625-aacd-430d8224ee45", "Readings": [[1456980268000, 317]]}, "/safar/Mazagaon/pm2.5": {"uuid": "bb092721-a9a5-5e0f-9941-41dcb823b153", "Readings": [[1456980268000, 215]]}, "/safar/Borivali/pm2.5": {"uuid": "3fce1865-6b2e-557a-a2ba-22b157c18275", "Readings": [[1456980268000, 176]]}, "/safar/BKC/pm2.5": {"uuid": "efb58049-2dd8-5672-b044-1d7dfd33653c", "Readings": [[1456980268000, 312]]}, "/safar/Bhandup/pm2.5": {"uuid": "9c5670ae-d360-58b7-bc27-4efffd2aee25", "Readings": [[1456980268000, 302]]}, "/safar/Navi Mumbai/pm2.5": {"uuid": "b7d15ea9-d29c-51d4-b6cc-a0cf09633887", "Readings": [[1456980268000, 318]]}, "/safar/Worali/pm2.5": {"uuid": "c73a33b2-a6b0-5ff5-a048-0c1fa01495e3", "Readings": [[1456980268000, 135]]}, "/safar/Malad/pm2.5": {"uuid": "1ea37a6e-7673-5c93-a4b2-733c43e10989", "Readings": [[1456980268000, 329]]}}
	"""
	if request.method == 'POST':
		giles_url = 'http://localhost:8079/add/MYAPIKEY'
		response = requests.post(giles_url, data=json.dumps(request.data))
		# print json.dumps(request.data)
		return Response(response.content)

def get_all_sensors():
	"""
	Returns the data of all sensors
	"""
	query_url = 'http://localhost:8079/api/query'
	query = "select *"
	r = requests.post(query_url, query)
	return r.content

def get_data_by_uuid_helper(uuid, hours):
	"""
	Returns the data of sensor specified by uuid of last 30 days
	TODO : Return the data given time in days,hours,minutes
	"""
	parser = HTMLParser()
	uuid = parser.unescape(uuid)
	query_url = 'http://localhost:8079/api/query'
	query = "select data in (now -"+hours+"h, now) where uuid='"+uuid+"'"
	r = requests.post(query_url, query)
	readings = json.loads(r.content)
	try:
		readings = readings[0]["Readings"]
	except:
		return []
	return readings
# Leave the rest of the views (detail, results, vote) unchange