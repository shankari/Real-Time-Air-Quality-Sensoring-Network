from smap.driver import FetchDriver
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleDriver(FetchDriver):
    def setup(self, opts):
        FetchDriver.setup(self, opts)
        self.add_timeseries('/pm2.5', 'ug/m3')
        self.add_collection('/data')

    def process(self, data):
    	logging.debug(data)
        self.add('/pm2.5', data[0]['pm2.5'])
        self.add('/data',data)