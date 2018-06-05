import numpy as np
import serial, time, csv, datetime
import sys
from shutil import copyfile

def start_log(output, n_entries = 24* 60, delay = 60):
    final_output = "C:/Users/Hefty-131-1/Box/HutzlerLab/Personal/AvikarPeriwal/TemperatureLog" + "/temp-log-5-17.csv"
    ser = serial.Serial('COM3', 1200, 
                    timeout = 1,
                    parity = serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.SEVENBITS)
    out = csv.writer(open(output, 'w'))
    header = ["time"] + ['sensor ' + str(i + 1) for i in range(8)]
    out.writerow(header)
    count = 0
    while True:
        ser.write(b"KRDG?\r\n")
        time.sleep(0.1)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        reading = ser.read(100)
        s = [st] + [float(i) for i in reading.decode("utf-8").strip().split(',')]
        f = open(output, 'a')
        out = csv.writer(f)
        out.writerow(s)
        count += 1
        if count % 100 == 0:
            f2 = open(final_output, 'ab')
            f2.write(open(output, 'rb').read())
            f2.close()
            f = open(output, 'w')
            f.close()
        time.sleep(delay)
    ser.close()

def plot_log(output, n_entries = 24 * 60 * 60, delay = 60):
    raise NotImplementedError

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("Buffer at: ", sys.argv[1])
        print("Log at C:/Users/Hefty-131-1/Box/HutzlerLab/Personal/AvikarPeriwal/TemperatureLog" + "/temp-log-5-17.csv")
        start_log(sys.argv[1], delay = 0.1)