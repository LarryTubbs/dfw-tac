import time

def cycle(np, rep_count = 4):
    n = np.n
 
    # cycle
    for i in range(rep_count * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (0, 255, 0)
        np.write()
        time.sleep_ms(25)

def bounce(np, rep_count = 4):
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
        time.sleep_ms(60)

def fade(np):
    n = np.n
    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
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

