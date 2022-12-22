import numpy as np
import serial
import time
import math
import datetime
from target_points import image_processing

# pôr pos inicial com comando (centro ou cantos)
# receber coordenadas da pos inicial
# lista de listas de pontos

# Current position of robot: LISTPV POSITION (X,Y,Z,P,R)
# flush antes de read

class scorbot:
    def __init__ (self):
        if serial:
            self.com = serial.Serial("COM3", baudrate=9600, bytesize=8, timeout=2, parity="N", xonxoff=0)
        self.ipos=[0,0,0,0]
        self.pitch=0
        pass
    
    def send(self, msg):
        self.com.write(bytes(msg,'UTF-8'))
        pass

    def initpos(self,aux,x,y,z,p,r):
        self.ipos[0]=x
        self.ipos[1]=y
        self.ipos[2]=z
        self.ipos[3]=r
        self.pitch=p
        pass
    
    def read_and_wait(self, aux, wait_time):
        """This function listens the serial port for wait_time seconds
        waiting for ASCII characters to be sent by the robot
        It returns the string of characters"""
        output = ""
        flag = True
        start_time = time.time()
        while flag:
            # Wait until there is data waiting in the serial buffer
            if self.com.in_waiting > 0:
                # Read data out of the buffer until a carriage return / new line is found
                selfString = self.com.readline()

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

    def movestr(self, aux, coordi, coordf):
        self.send("SETPVC 1 X " + str(self.ipos[0]+int(coordf[0])) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(self.ipos[1]+int(coordf[1])) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]) + "\r")
        time.sleep(0.5)
        # rf=roll_calc(self,coordi,coordf)
        self.send("MOVE 1 " + "\r")
        time.sleep(1)

    def movehome(self,aux):
        self.send("SETPVC 1 X " + str(self.ipos[0]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(self.ipos[1]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]) + "\r")
        time.sleep(0.5)
        # rf=roll_calc(self,coordi,coordf)
        self.send("MOVE 1 " + "\r")
        time.sleep(1)
    

def roll_calc(self,i,f):
    ()


def start(self):
    """Start the robot, activating the axis and setting the speed to 50%
       The first position is beforehand manually selected"""
    self.send("CON " + "\r")
    time.sleep(0.5)
    self.send("SPEED 1 " + "\r")
    time.sleep(0.5)


def homepos(self):
    # self.com.flush()
    # msg = self.read_and_wait(self,2) # LISTPV POSITION
    # msg = self.read_and_wait(self,2) # Joint coordinates
    # msg = self.read_and_wait(self,2) # Cartesian coordinates
    # self.send("LISTPV POSITION " + "\r")
    # msg = self.com.in_waiting
    # msg = self.com.read(msg)
    # msg = "X: 3767    Y:-1727    Z:-723     P:-974     R:-201 >"
    # msg = msg.split("X")
    msg = msg.split()
    # print(">> ")
    x = int(msg[-6])
    y = msg[-5]
    y = int(y[2:])
    z = msg[-4]
    z = int(z[2:])
    # p = msg[-3]
    # p = p[2:]
    r = msg[-2]
    r = int(r[2:])
    self.initpos(self,x,y,z,1,r)

def draw(self,pts):
    for i in range(len(pts)):
        if i==0:
            self.movestr(self,self.ipos,pts[i])
            self.read_and_wait(self,0.5)
        self.movestr(self,pts[i-1],pts[i])
    

bot=scorbot()
start(bot)
# homepos(bot)
# bot.initpos(bot,5155,-464,1084,0,0) # Scorbot 1
bot.initpos(bot,4499,-847,-730,0,0) # Scorbot 2
# bot.com.flush()
bot.movehome(bot)

pts = image_processing("test_draw_1.png")
draw(bot,pts)
# print(bot.ipos[0])
# print(bot.ipos[1])
# print(bot.ipos[2])
# print(bot.ipos[3])