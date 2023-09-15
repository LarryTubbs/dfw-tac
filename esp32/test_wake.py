import machine 
import ntptime
import esp32
import time

PIN = 15
DUR_MIN = 2
DUR_SEC = DUR_MIN * 60.0

last_called = time.time()

def callback(p):
    print('detected motion, resetting time')
    global last_called
    last_called = time.time()

def main():
    global last_called
    try:
        # sync the time with a netowrk timeserver
        ntptime.settime()
        last_called = time.time()
        
    except Exception as ex:
        print('    Exception: ' + str(ex))
        
    print('starting up...')

    p = machine.Pin(PIN, machine.Pin.IN)
    p.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)

    esp32.wake_on_ext0(p, esp32.WAKEUP_ANY_HIGH)

    while (True):
        now = time.time()
        diff = now - last_called
        print('now: %i' % int(now))
        print('last_called: %i' % int(last_called))
        print('now - last_called %i' % int(diff))
        print('DUR_SEC: %i' % int(DUR_SEC))
        if diff >= DUR_SEC:
            print('no motion since last call, going to deep sleep for %i minutes.' % DUR_MIN)
            machine.deepsleep(DUR_MIN * 1000 * 60) # * 60 seconds per minute * 1000 ms per second
        else:
            print('still alive...')
            time.sleep(DUR_MIN * 60)


if __name__ == "__main__":
  
    # calling main function
    main()