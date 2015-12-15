from smap.driver import SmapDriver
from smap.util import periodicSequentialCall
from smap.contrib import dtutil

from datetime import datetime
from twisted.internet import threads
from twisted.python import log

import pytz, time
import twitter
import simplejson as json
import requests
import sys, traceback
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TwitterDriver(SmapDriver):
    """
    The driver queries the database with UUIDs to get the last 12hr average of PM2.5 Air Quality Data
    """
    def setup(self, opts):
        self.add_timeseries('/twitterFeed', 'C')
        self.counter = 0
        self.rate = float(opts.get('Rate', 1))
        self.consumer_key = str(opts.get('consumer_key', 1))
        self.consumer_secret = str(opts.get('consumer_secret', 1))
        self.access_token_key = str(opts.get('access_token_key', 1))
        self.access_token_secret = str(opts.get('access_token_secret', 1))
        self.tz = pytz.timezone(opts.get('Timezone', 1))

    def start(self):
        # Call post_to_twitter after every 12 hrs
        periodicSequentialCall(self.post_to_twitter).start(self.rate)

    def post_to_twitter(self):
        # Posting last 12hour average to twitter after every 12hours
        r = requests.get('http://localhost/raqmn_api/')
        contents = json.loads(r.content)
        dt = datetime.now(self.tz)
        logging.debug(dt)
        for content in contents:
            logging.debug(content['uuid'])
            req_data = requests.get('http://localhost/raqmn_api/data/12h/'+content['uuid'])
            self.tweet(req_data.content, dt, content['Metadata']['SourceName'], (content['Path'].split('/'))[3].strip())
            time.sleep(5)

    def tweet(self, measure, dt, place, pollutant):
        try:
            unit = self.get_unit(pollutant)
            level = self.get_level(int(float(measure)), pollutant)
            time_print = dt.strftime('%a, %d %b %Y %H:%M')
            tweet_content = time_print + ", Location : " + place + ", " + str.upper(pollutant) + " : "+measure+" "+unit+" (Last 12hr average), Level : " + level +", Sources : SAFAR"
            api = twitter.Api(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret,access_token_key=self.access_token_key,access_token_secret=self.access_token_secret)
            logging.debug(tweet_content)
            # status = api.PostUpdate(tweet_content)
        except:
            logging.debug("Unexpected error : "+ str(sys.exc_info()[0]))
            logging.debug("Traceback : "+ str(traceback.format_exc()))

    def get_unit(self,pollutant):
        return "AQI"

    def get_level(self,measure, pollutant):
        # Source : http://www.indiaenvironmentportal.org.in/files/file/Air%20Quality%20Index.pdf
        if measure <= 50 :
            return 'Good'
        elif measure <= 100 :
            return 'Satisfactory'
        elif measure <= 250 :
            return 'Moderately polluted'
        elif measure <= 350 : 
            return 'Poor'
        elif measure <= 430 :
            return 'Very Poor'
        else :
            return 'Severe'

    def load(self, st, et, cache=None):
        d = threads.deferToThread(self.load_data, st, et)
        return d

    def load_data(self, st, et):
        st_utc = dtutil.dt2ts(st)
        et_utc = dtutil.dt2ts(et)
        ts = int(st_utc / 120) * 120 # round down to nearest 2-min increment
        while ts <= et_utc:
            self.add('/twitterFeed', ts, self.counter)
            self.counter += 1
            ts += 120 # 2-min increments