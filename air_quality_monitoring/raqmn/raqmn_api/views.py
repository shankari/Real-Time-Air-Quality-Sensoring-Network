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
import json
import ast
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
		query_url = 'http://localhost:8079/api/query'
		query = "select *"
		storage = StringIO()
		curlObj = pycurl.Curl()
		curlObj.setopt(curlObj.URL, query_url)
		curlObj.setopt(curlObj.POST, 1)
		curlObj.setopt(curlObj.POSTFIELDS, query)
		curlObj.setopt(curlObj.WRITEFUNCTION, storage.write)
		curlObj.perform()
		curlObj.close()
		return_json = ast.literal_eval(storage.getvalue().replace('"',"'"))

		return Response(return_json)

@csrf_exempt
@api_view(['GET'])
def get_data_by_uuid(request, uuid):
	"""
	Returns the metadata from quasar server using uuid of the data
	"""
	if request.method == 'GET':
		parser = HTMLParser()
		uuid = parser.unescape(uuid)
		query_url = 'http://localhost:8079/api/query'
		query = "select data in (now -30d, now) where uuid='"+uuid+"'"
		storage = StringIO()
		curlObj = pycurl.Curl()
		curlObj.setopt(curlObj.URL, query_url)
		curlObj.setopt(curlObj.POST, 1)
		curlObj.setopt(curlObj.POSTFIELDS, query)
		curlObj.setopt(curlObj.WRITEFUNCTION, storage.write)
		curlObj.perform()
		curlObj.close()
		return_json = ast.literal_eval(storage.getvalue().replace('"',"'"))
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
		storage = StringIO()
		curlObj = pycurl.Curl()
		curlObj.setopt(curlObj.URL, query_url)
		curlObj.setopt(curlObj.POST, 1)
		curlObj.setopt(curlObj.POSTFIELDS, query)
		curlObj.setopt(curlObj.WRITEFUNCTION, storage.write)
		curlObj.perform()
		curlObj.close()
		readings = ast.literal_eval(storage.getvalue().replace('"',"'"))
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

# Leave the rest of the views (detail, results, vote) unchanged