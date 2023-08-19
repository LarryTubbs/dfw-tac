# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET

stations = ['KDFW', 'KXBP', 'KFTW', 'KAFW']
  
def loadMETARs():
  
    # url of METAR data feed
    url = 'https://aviationweather.gov/adds/dataserver_current/current/metars.cache.xml'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open('metars.xml', 'wb') as f:
        f.write(resp.content)
          

def getColor(flightCategory):
    colors = {
        'LIFR': (255,0,255),
        'IFR': (255,0,0),
        'MVFR': (0,0,255),
        'VFR': (0,255,0)
    }

    color = ""
    try:
        color = colors[flightCategory]
    except KeyError:
        color = (0,0,0)

    return color
  
def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # create empty list for metar items
    metars = []
  
    # iterate metar items
    for item in root.findall('./data/METAR'):
  
        # empty metar dictionary
        metar = {}
  
        # iterate child elements of item
        for child in item:
            if child.tag == 'station_id' or child.tag == 'flight_category':
                metar[child.tag] = child.text

  
        # append metar dictionary to metar items list
        if metar['station_id'] in stations:
            metars.append(metar)
      
    # return news items list
    return metars
  
  
def savetoCSV(metars, filename):
  
    # specifying the fields for csv file
    fields = ['station_id', 'flight_category']
  
    # writing to csv file
    with open(filename, 'w') as csvfile:
  
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields)
  
        # writing headers (field names)
        writer.writeheader()
  
        # writing data rows
        writer.writerows(metars)
  
      
def main():
    # load rss from web to update existing xml file
    loadMETARs()
  
    # parse xml file
    metars = parseXML('metars.xml')
  
    # store news items in a csv file
    savetoCSV(metars, 'metars.csv')

    # test code
    print(getColor('LIFR'))
      
      
if __name__ == "__main__":
  
    # calling main function
    main()