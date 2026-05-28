import logging
import logging.handlers
import boto3
import os
from time import sleep, strftime
from picamera2 import Picamera2
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun as sun_times

handler = logging.handlers.RotatingFileHandler(
    '/var/log/sunriver-upload.log', maxBytes=1_000_000, backupCount=3
)
logging.basicConfig(handlers=[handler], level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

location = LocationInfo('Sunriver', 'USA', 'US/Pacific', 43.8694, -121.4334)

pst=pytz.timezone('US/Pacific')

camera = Picamera2()
camera.configure(camera.create_still_configuration(main={"size": (1024, 768)}))
camera.start()

bucketName = 'sunriver-display-s3-prod'
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketName)

while 1:
    dateToday = datetime.date.today() # get todays date
    sunInfo = sun_times(location.observer, date=dateToday, tzinfo=pytz.timezone('US/Pacific')) # Get Sun information for Location

    pictures = 1
    now = pst.localize(datetime.datetime.now()) # get the time of now

    while now < sunInfo['dusk']: # While it is earlier than dusk repeat
        if now < sunInfo['dawn']:
            logging.info('Sun has not risen; skipping capture')
        else:
            print('Sun is up take a photo. Count: %s' % (str(pictures)))
            timeStamp = strftime("%Y-%m-%d_%X")     # YYYY-mm-dd_time
            fileName = '8_towhee_' + timeStamp + '.jpg'
            camera.capture_file(fileName)

            bucket.upload_file(fileName, 'public/current.jpg')
            os.remove(fileName)

            pictures = pictures + 1
        sleep(1800)
        now = pst.localize(datetime.datetime.now()) # get the time of now

    print('Finished Taking pictures for the day sun has gone. Total pictues: %s' % str(pictures))

    tomorrowCheck = datetime.date.today() # get todays date
    while dateToday == tomorrowCheck:
        sleep(900)
        tomorrowCheck = datetime.date.today()
