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
	return render(request, 'index/index.html')

def api_specs(request):
	"""
	Returns the page with API Specifications
	It contains the information of all the APIs opened for public usage
	"""
	return render(request, 'api_specs/index.html')
