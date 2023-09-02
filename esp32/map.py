# displays current flight conditions info on a map

import time
import pixutils
import machine
import neopixel
import socket
import json

URL = 'http://lrtenigma.z21.web.core.windows.net/AviationWeather/metars.json' 
PIN = 23
STATIONS = ['KCPT', 'KGDJ', 'KFWS', 'KGKY', 'KGPM', 'KRBD', 'KLNC', 'KHQZ', 'KF46', 'KADS', 'KDAL',  
            'KDFW', 'KAFW', 'KFTW', 'KNFW', 'KMWL', 'KXBP', 'KLUD', 'KDTO', 'KTRI', 'KGVT', 'KF00',  
            'KGYI', 'KGLE', 'K0F2']
SLEEP_MIN = 5
ON = 255 # set to color intensity 1-255

def getColor(flightCategory):
    colors = {
        'LIFR': (ON,0,ON),
        'IFR': (ON,0,0),
        'MVFR': (0,0,ON),
        'VFR': (0,ON,0)
    }

    color = ""
    try:
        color = colors[flightCategory]
    except KeyError:
        color = (ON,ON,ON)

    return color

def http_get(url):
    ret = ""
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(4096)
        if data:
            ret += str(data, 'utf8')
        else:
            break
    s.close()
    response = ret.split('\r\n\r\n')
    return response[1]

def main():

    # initalize the neopixel strand
    print('initializaing NeoPixel Strand...')
    np = neopixel.NeoPixel(machine.Pin(PIN), len(STATIONS))
    print('complete')

    # every 5 minutes
    while True:
        print('beginning map refresh...')

        # Do an animation
        print('    beginning animation...')
        # pixutils.cycle(np, rep_count=1)
        pixutils.fade(np)
        pixutils.clear(np)
        print('    animation complete')

        # Retrieve the current metars object
        print('    retrieving current metars.json file...')
        # res = requests.get(URL)
        res = http_get(URL)
        print('    file retrieved')
        print(res)
        
        print('    loading jason into metars dictionary...')
        metars = json.loads(res)
        print('    dictionary parsed')
        print(metars)

        # repaint the map
        print('    repainting the map...')
        i = 0
        for itm in STATIONS:
            try:
                np[i] = getColor(metars[itm])
            except KeyError:
                np[i] = (ON, ON, ON)
            i += 1
        np.write()
        print('    map repainted')

        print('sleeping until next refresh')
        time.sleep(60 * SLEEP_MIN)

if __name__ == "__main__":
  
    # calling main function
    main()