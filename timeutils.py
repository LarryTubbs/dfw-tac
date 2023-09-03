import datetime
import time

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
    

def main():
    start = datetime.time(22,0,0)
    end = datetime.time(5,0,0)
    print(time.asctime() + ': ' + str(time_in_range(start, end, datetime.datetime.now().time())))
    print('22:30: ' + str(time_in_range(start, end, datetime.time(22,30,0))))

if __name__ == "__main__":
  
    # calling main function
    main()