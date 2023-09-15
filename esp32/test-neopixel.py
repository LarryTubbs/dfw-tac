import machine, neopixel, pixutils, time

def main():
    np = neopixel.NeoPixel(machine.Pin(23), 25)
    pixutils.all_on(np)
    time.sleep(5)
    pixutils.clear(np)

if __name__ == "__main__":
  
    # calling main function
    main()