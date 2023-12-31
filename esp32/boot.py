# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import webrepl

def do_connect():
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('TP-LINK_CECC', '1Cor13:4-13')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_connect()
webrepl.start()
