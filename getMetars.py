# importing the required modules
import json
import requests
import xml.etree.ElementTree as ET
import uploadMetars
import time

DURATION = 10 # the amount of time in minutes to wait between uploads

stations = ['K0F2', 'KGLE', 'KGYI', 'KF00', 'KXBP', 'KLUD', 'KDTO', 'KTKI', 'KGVT', 'KAFW', 'KADS', 
            'KF46', 'KFTW', 'KDFW', 'KDAL', 'KMWL', 'KNFW', 'KGKY', 'KGPM', 'KRBD', 'KHQZ', 'KFWS', 
            'KLNC', 'KGDJ', 'KCPT']
  
def loadMETARs():
  
    # url of METAR data feed
    url = 'https://aviationweather.gov/adds/dataserver_current/current/metars.cache.xml'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open('metars.xml', 'wb') as f:
        f.write(resp.content)
          

def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # create empty list for metar items
    metars = {}
  
    # iterate metar items
    for item in root.findall('./data/METAR'):
  
        # empty metar dictionary
        metar = {}
  
        # iterate child elements of item
        for child in item:
            if child.tag == 'station_id' or child.tag == 'flight_category':
                metar[child.tag] = child.text

  
        # append metar dictionary to metar items list
        try:
            if metar['station_id'] in stations:
                metars[metar['station_id']] = metar['flight_category']
        except KeyError:
            metars[metar['station_id']] = ''
            
    # return metar list
    return metars
  


def saveToJson(metars, filename):
    with open(filename, 'w') as f:
        json.dump(metars, f)
    
  
      
def main():
    while True:
        print('map refresh started at ', time.asctime())

        # load rss from web to update existing xml file
        print('\tretrieving metar files from the FAA...')
        loadMETARs()
        print('\tfile retrieved.')
    
        # parse xml file
        print('\tparsing xml...')
        metars = parseXML('metars.xml')
        print('\txml file successfully parsed.')
    
        # store items in a json file
        print("\textracting flight categories for the aiports on the map, and saving them to 'metars.json'...")
        saveToJson(metars, 'metars.json')
        print("\t'metars.json' successfully written.")

        print("\tuploading 'metars.json' to azure...")
        uploadMetars.uploadMetars('metars.json')
        print("\t'metars.json' successfully uploaded")
        
        print('map refresh completed at ', time.asctime())
        print('will refresh again in %i minutes.' % DURATION)
        time.sleep(DURATION * 60)
      
      
if __name__ == "__main__":
  
    # calling main function
    main()