# displays current flight conditions info on a map

import time
import pixutils
import machine
import neopixel
import socket
import json

URL = 'http://lrtenigma.z21.web.core.windows.net/AviationWeather/metars.json' 
PIN = 23
STATIONS = ['K0F2', 'KGLE', 'KGYI', 'KF00', 'KXBP', 'KLUD', 'KDTO', 'KTKI', 'KGVT', 'KAFW', 'KADS', 
            'KF46', 'KFTW', 'KDFW', 'KDAL', 'KMWL', 'KNFW', 'KGKY', 'KGPM', 'KRBD', 'KHQZ', 'KFWS', 
            'KLNC', 'KGDJ', 'KCPT', 'KSEP', 'KINJ']
SLEEP_MIN = 5
INTENSITY = 8  # 1 full bright, 2 dimmer, 4 even dimmer, 8 even dimmer 

def getColor(flightCategory):
    colors = {
        'LIFR': (255 // INTENSITY,0,255 // INTENSITY),
        'IFR': (255 // INTENSITY,0,0),
        'MVFR': (0,0,255 // INTENSITY),
        'VFR': (0,255 // INTENSITY,0)
    }

    color = ""
    try:
        color = colors[flightCategory]
    except KeyError:
        color = (255,255,255)

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
        pixutils.cycle(np, rep_count=1)
        pixutils.clear(np)
        print('    animation complete')

        # Retrieve the current metars object
        print('    retrieving current metars.json file...')
        # res = requests.get(URL)
        res = http_get(URL)
        print('    file retrieved')
        print(res)
        
        print('    loading jason into metars dictionary...')
        metars = json.loads(res, )
        print('    dictionary parsed')
        print(metars)

        # repaint the map
        print('    repainting the map...')
        i = 0
        for itm in STATIONS:
            try:
                np[i] = getColor(metars[itm])
            except KeyError:
                np[i] = (255, 255, 255)
            i += 1
        np.write()
        print('    map repainted')

        print('sleeping until next refresh')
        time.sleep(60 * SLEEP_MIN)

if __name__ == "__main__":
  
    # calling main function
    main()