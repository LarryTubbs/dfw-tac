# displays current flight conditions info on a map

import time
import pixutils
import machine
import neopixel
import ntptime
import esp32
import socket
import json

URL = 'http://lrtenigma.z21.web.core.windows.net/AviationWeather/metars.json' 
PIN = 23
STATIONS = ['KCPT', 'KGDJ', 'KFWS', 'KGKY', 'KGPM', 'KRBD', 'KLNC', 'KHQZ', 'KF46', 'KADS', 'KDAL',  
            'KDFW', 'KAFW', 'KFTW', 'KNFW', 'KMWL', 'KXBP', 'KLUD', 'KDTO', 'KTKI', 'KGVT', 'KF00',  
            'KGYI', 'KGLE', 'K0F2']
SLEEP_MIN = 20
SLEEP_SEC = 20 * 60.0
ON = 50 # set to color intensity 1-255
SENSOR_PIN = 15

last_called = 0
count = 0

def callback(p):
    global last_called
    global count
    count += 1
    if count > 3:
        count = 0
        last_called = time.time()
        print('detected motion, resetting time to %i' % int(last_called))
    

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
    global last_called
    # initalize the neopixel strand
    print('initializaing NeoPixel Strand...')
    np = neopixel.NeoPixel(machine.Pin(PIN), len(STATIONS))
    print('complete')

    # initalize motion sensor
    p = machine.Pin(SENSOR_PIN, machine.Pin.IN)
    p.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)

    esp32.wake_on_ext0(p, esp32.WAKEUP_ANY_HIGH)

    # every SLEEP_MIN minutes
    while True:
        print('beginning map refresh...')

        try:
            # sync the time with a netowrk timeserver
            ntptime.settime()
            if last_called == 0:
                last_called = time.time()
            hour = time.localtime()[3]
        except Exception as ex:
            print('    Exception: ' + str(ex))
            hour = 3
            pixutils.fade(np, red=True)
        
        if hour >= 3 and hour < 10:
            print('outside working hours (10:00 - 03:00 UTC)')
            pixutils.clear(np)
            print('sleeping until next refresh')
            # deep sleep SLEEP_MIN
            machine.deepsleep(SLEEP_MIN * 1000 * 60) # SLEEP_MIN * 1000 ms per second * 60 sec per min
        else:
            try:
                now = time.time()
                diff = now - last_called
                print('now: %i' % int(now))
                print('last_called: %i' % int(last_called))
                print('now - last_called %i' % int(diff))
                print('DUR_SEC: %i' % int(SLEEP_SEC))
                if diff >= SLEEP_SEC:
                    print('no motion since last call, going to deep sleep for %i minutes.' % SLEEP_MIN)
                    pixutils.clear(np)
                    machine.deepsleep() # * 1000 ms per second
                else:
                    print('still alive...')
                                
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
            except Exception as ex:
                print('    Exception: ' + str(ex))
                pixutils.fade(np, red=True)

            print('sleeping until next refresh')
            time.sleep(int(SLEEP_SEC)) # 60 sec per min * SLEEP_MIN

if __name__ == "__main__":
  
    # calling main function
    main()