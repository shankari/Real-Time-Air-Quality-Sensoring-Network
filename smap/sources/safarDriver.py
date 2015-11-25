from smap.driver import FetchDriver
from safarScraper import get_air_quality_data
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SafarDriver(FetchDriver):
    """
    The driver fetches the data from safar site and we store the data in format
    {
        "Path": "/safar/Worali/pm2.5",
        "uuid": "c73a33b2-a6b0-5ff5-a048-0c1fa01495e3",
        "Properties": {
            "Timezone": "India/Mumbai",
            "UnitofMeasure": "ug/m3",
            "ReadingType": "long"
        },
        "Metadata": {
            "Latitude": "19.01747",
            "SourceName": "Worali",
            "Longitude": "72.81751",
            "Area": "Worali"
        }
    }
    """
    def setup(self, opts):
    	# We setup the driver by getting the parameters of scraper first and then setting up the timeseries
        FetchDriver.setup(self, opts)
        data = get_air_quality_data(opts={})
        for i in range(0,len(data)):
            safar_city = self.add_timeseries('/'+data[i]['area']+'/pm2.5','AQI',description = 'PM2.5 readings for '+data[i]['area'])
            safar_city['Properties']['Timezone'] = 'India/Mumbai'
            safar_city['Metadata'] = {}
            safar_city['Metadata']['SourceName'] = data[i]['area']
            safar_city['Metadata']['Area'] = data[i]['area']
            safar_city['Metadata']['Latitude'] = data[i]['latitude']
            safar_city['Metadata']['Longitude'] = data[i]['longtitude']

    def process(self, data):
    	# We get the data and we set the PM2.5 for each sensor
    	logging.debug(len(data))
    	for i in range(0,len(data)):
            self.add('/'+data[i]['area']+'/pm2.5', data[i]['pm2.5'])
