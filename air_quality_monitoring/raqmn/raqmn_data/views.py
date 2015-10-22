from django.shortcuts import render
import requests
import json

# Create your views here.
from django.http import HttpResponse

def index(request):
	metadata = requests.get('http://localhost:8000/raqmn_api/')
	metadata = json.loads(metadata.text)
	print metadata[0]
	return render(request, 'raqmn_data/plot.html')

