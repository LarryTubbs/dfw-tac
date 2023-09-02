import time

def cycle(np, rep_count = 4, cycle_time = 60):
    n = np.n

 
    # cycle
    for i in range(rep_count * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (0, 255, 0)
        np.write()
        time.sleep_ms(cycle_time)
    clear(np)

def bounce(np, rep_count = 4, cycle_time = 60):
    n = np.n 
 
    # bounce
    for i in range(rep_count * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(cycle_time)
    clear(np)

def fade(np, cycle_time=10):
    n = np.n
    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (0, val, 0)
        np.write()
        time.sleep_ms(cycle_time)
    clear(np)

def all_on(np, color=(255, 255, 255)):
    n = np.n
    for i in range(n):
        np[i] = color
    np.write()

def clear(np):
    n = np.n

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


def demo(np):
   
    cycle(np)
    bounce(np)
    fade(np)
    clear(np)

