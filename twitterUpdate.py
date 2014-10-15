from twython import Twython
import time
import sys

#Setup keys for UconnStixPix
APP_KEY = 'zzVYRgLPpc3cTMLEFnaQt8TVi'
APP_SECRET = 'VfeP6FlPePQipE7A3R8D2p8Rx8eT1un01RxIQLJf8otscKCB1x'

ACCESS_TOK = '2796231601-RDagOnl4umj1bmoZuZR1LyPenxRNT0c9DLuNEBw'
ACCESS_SEC = 'RKm38TrlWwHBqtPlcjzfhyqxjc452YPb76BFCyxlqaqkR'

LOG_PATH = '/home/pi/PythonSource/UconnStixPix/log.txt'

#Setup twitter
twitter = Twython(APP_KEY,APP_SECRET,ACCESS_TOK,ACCESS_SEC)
last_tweet = time.localtime()

#Define image props
current_img_num = 0
MAX_IMAGES = 74
root_img_path = '/home/pi/PythonSource/UconnStixPix/stiximages/'
img_file_path = '/home/pi/PythonSource/UconnStixPix/current_img.txt'

def postPic(img):
    
    path = root_img_path + 'image' + str(img) + '.jpg'
    print path
    try:
        photo = open(path, 'rb')
        print 'Image was opened'
        twitter.update_status_with_media(status='Here is your Pic of Stix on the hour. #PixOfStix', media=photo)
        last_tweet = time.localtime()
    except Exception,e:
        print 'Failed to post the pic'
        writeToLog(str(e))
        sys.exit(0)
        

def incrementPic(curimg, maximg):
    if(curimg < maximg):
        return (curimg + 1)
    else:
        return 0

def getCurrentImg(path):
    f = open(path, 'r+')
    raw = f.readline()
    num = int(raw)
    f.close()
    return num

def setCurrentImg(path, value):
    f = open(path,'r+')
    raw = str(value) + ' '
    f.write(raw)
    f.close()

def writeToLog(message):
    timemessage = time.strftime("%m-%d-%Y %H:%M:%S", time.localtime())
    f = open(LOG_PATH, 'r+')
    f.read()
    f.write(timemessage + message + '\n')
    f.close()

try:
    # first find where it is has left off
    current_img_num = getCurrentImg(img_file_path)
    print 'Starting with image # ' + str(current_img_num)

    while True:
        current_time = time.localtime()
        #print current_img_num
        if(current_time.tm_min == 00):
            # post pic to twitter
            postPic(current_img_num)
            current_img_num = incrementPic(current_img_num, MAX_IMAGES)
            setCurrentImg(img_file_path, current_img_num)
            print 'Next is image # ' + str(current_img_num)
            time.sleep(61)
        time.sleep(1)

except Exception,e:
    twitter.status_update(status='Something went wrong with the program')
    writeToLog(str(e))
    sys.exit(0)
