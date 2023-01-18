#
# Test the Novatel Flexpak G2L GPS  for position simplified reading mode
# It receives the data from the GPS and stores the string in a file
# No processing to extract the latitude, longitude, and height is made
#

import serial
import time
from datetime import datetime

def read_and_wait(ser, wait_time):
    output = ""
    flag = True
    start_time = time.time()

    while flag:
        # Wait until there is data waiting in the serial buffer
        # and keep concatenating until the max time is reached
        if ser.in_waiting > 0:
            try:
                serString = ser.read()
                output = output + serString.decode("Ascii")
            except:
                pass
        else:
            deltat = time.time() - start_time
            if deltat>wait_time:
                flag = False
    output = output + "\n"
    return output        



def main():
    print("Starting")

    ser = serial.Serial('COM12', baudrate=115200, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
    print("COM port in use:  {0}".format(ser.name))
    
    serString = ""  # Used to hold data coming over UART

    
    
    for k in range(1,10000):

        # ask the GPS for the best position info
        ser.write(b'LOG BESTPOS\r')
        cmd_answer = read_and_wait(ser,1)
        print(cmd_answer)

        # save the data in a file
        rec_file = open("reta_passadeirapf.txt", "a")
        tstamp = datetime.now()
        tstamp= str(tstamp)
        tstamp = tstamp[10:]
        rec_file.write(cmd_answer + 'iteration' + str(k) + " " + tstamp)

        rec_file.close()

        # work in progress
        #idx = cmd_answer.find("INSUFFICIENT_OBS", 0, len(cmd_answer))
        #if idx>=0:
        #    cmd_answer.find(" ", idx, len(cmd_answer))
        #elif idx<0:
        #    print("INSUFFICIENT OBS\n")
        #else:
        #    print("Abnormal condition\n")

        print('iteration ', k)
    
    # closing and housekeeping
    ser.close()

    print('housekeeping completed - exiting')


########################################################################    
if __name__ == "__main__":
    main()
