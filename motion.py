import numpy as np
import serial
import time
import math
import datetime

# pôr pos inicial com comando (centro ou cantos)
# receber coordenadas da pos inicial
# lista de listas de pontos

# Current position of robot: LISTPV POSITION (X,Y,Z,P,R)
# drawer.send("SETPVC POS1 X " + str(int(-pixels_to_tenths_mm(points[0][1])) + drawer.initial[0]) + "\r")
class scorbot:
    def __init__ (self):
        if serial:
            self.com = serial.Serial("COM4", baudrate=9600, bytesize=8, timeout=2, parity="N", xonxoff=0)
        self.ipos=[0,0,0]
        self.pitch=0
        self.roll=0
        pass
    
    def send(self, msg):
        self.com.write(bytes(msg,'UTF-8'))
        pass

    def initpos(self,aux,x,y,z,p,r):
        self.ipos[0]=x
        self.ipos[1]=y
        self.ipos[2]=z
        self.pitch=p
        self.roll=r
        pass
    
    def read_and_wait(self, wait_time):
        """This function listens the serial port for wait_time seconds
        waiting for ASCII characters to be sent by the robot
        It returns the string of characters"""
        output = ""
        flag = True
        start_time = time.time()
        while flag:
            # Wait until there is data waiting in the serial buffer
            if self.in_waiting > 0:
                # Read data out of the buffer until a carriage return / new line is found
                selfString = self.readline()

                # Print the contents of the serial data
                try:
                    output = selfString.decode("Ascii")
                    print(selfString.decode("Ascii"))
                except:
                    pass
            else:
                deltat = time.time() - start_time
                if deltat>wait_time:
                    flag = False
        return output

    def movestr(self, coordi, coordf):
        self.send("SETPVC POS1 X " + coordf[0] + "\r")
        time.sleep(0.5)
        self.send("SETPVC POS1 Y " + coordf[1] + "\r")
        time.sleep(0.5)
        self.send("SETPVC POS1 Z " + self.ipos[2] + "\r")
        time.sleep(0.5)
        rf=roll_calc(self,coordi,coordf)
        self.send("MOVE POS1 " + "\r")
        time.sleep(0.5)


def roll_calc(self,i,f):
    ()


def start(self):
    """Start the robot, activating the axis and setting the speed to 50%
       The first position is beforehand manually selected"""
    self.send("CON " + "\r")
    time.sleep(0.5)
    self.send("SPEED 50 " + "\r")
    time.sleep(0.5)


def homepos(self):
    self.send("LISTPV POSITION " + "\r")
    msg = self.read(self)
    msg = msg.decode('UTF-8')
    msg = "1:0 2:0 3:0 4:0 5:0 X:1342 Y:2345 Z:340 P:640 R:180"
    msg = msg.split()
    x = msg[5]
    x = x[2:]
    y = msg[6]
    y = y[2:]
    z = msg[7]
    z = z[2:]
    p = msg[8]
    p = p[2:]
    r = msg[6]
    r = r[2:]
    self.initpos(self,x,y,z,p,r)

    
bot=scorbot()
start(bot)
homepos(bot)

