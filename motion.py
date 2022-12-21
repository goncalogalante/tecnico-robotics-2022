import numpy as np
import serial
import time
import math
import datetime

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
        self.send("SETPVC POS1 X " + str(self.ipos[0]+coordf[0]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC POS1 Y " + str(self.ipos[1]+coordf[1]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC POS1 Z " + str(self.ipos[2]) + "\r")
        time.sleep(0.5)
        # rf=roll_calc(self,coordi,coordf)
        self.send("MOVE POS1 " + "\r")
        time.sleep(1)


def roll_calc(self,i,f):
    ()


def start(self):
    """Start the robot, activating the axis and setting the speed to 50%
       The first position is beforehand manually selected"""
    self.send("CON " + "\r")
    time.sleep(0.5)
    self.send("SPEED 5 " + "\r")
    time.sleep(0.5)

# Scorbot 2
# z=-750
# X= 3767
# Y=-1727

def homepos(self):
    self.send("LISTPV POSITION " + "\r")
    msg = self.read_and_wait(self,0.1) # LISTPV POSITION
    msg = self.read_and_wait(self,0.1) # Joint coordinates
    msg = self.read_and_wait(self,0.1) # Cartesian coordinates
    msg = "X: 3767    Y:-1727    Z:-723     P:-974     R:-201"
    msg = msg.split()
    print(">> ")
    print(msg[0])
    print(msg[1])
    # x = msg[5]
    # x = x[2:]
    # y = msg[6]
    # y = y[2:]
    # z = msg[7]
    # z = z[2:]
    # p = msg[8]
    # p = p[2:]
    # r = msg[6]
    # r = r[2:]
    # self.initpos(self,x,y,z,p,r)

def draw(self,pts):
    for i in range(len(pts)):
        if i==0:
            self.movestr(self,self.ipos,pts[i])
            self.read_and_wait(self,0.5)
        self.movestr(self,pts[i-1],pts[i])
    

bot=scorbot()
start(bot)
# homepos(bot)
pts = [(88, 724), (31, 1084), (10, 1403), (22, 1784)] #(72, 2145), (137, 2391), (252, 2645), (385, 2812), (543, 2919), (704, 2970), (1726, 3186), (1977, 3224), (2239, 3237), (2744, 3201), (3882, 3005), (4740, 2901), (5167, 2794), (5351, 2712), (5513, 2612), (5539, 2414), (5524, 2147), (5350, 1409), (5283, 1270), (5193, 1198), (5105, 1204), (4992, 1277), (4607, 1715), (4441, 1852), (4351, 1884), (4270, 1882), (4184, 1847), (4115, 1780), (4092, 1696), (4118, 1594), (4483, 1030), (4563, 852), (4606, 683), (4608, 516), (4565, 364), (4470, 215), (4344, 105), (4130, 18), (3976, 7), (3866, 21), (1637, 1088), (2439, 1094), (1390, 2144), (465, 114)]
pts = [(88, 724), (31, 1084), (1726, 3186), (22, 1784)] #(72, 2145), (137, 2391), (252, 2645), (385, 2812), (543, 2919), (704, 2970), (1726, 3186), (1977, 3224), (2239, 3237), (2744, 3201), (3882, 3005), (4740, 2901), (5167, 2794), (5351, 2712), (5513, 2612), (5539, 2414), (5524, 2147), (5350, 1409), (5283, 1270), (5193, 1198), (5105, 1204), (4992, 1277), (4607, 1715), (4441, 1852), (4351, 1884), (4270, 1882), (4184, 1847), (4115, 1780), (4092, 1696), (4118, 1594), (4483, 1030), (4563, 852), (4606, 683), (4608, 516), (4565, 364), (4470, 215), (4344, 105), (4130, 18), (3976, 7), (3866, 21), (1637, 1088), (2439, 1094), (1390, 2144), (465, 114)]
bot.initpos(bot,3767,-1227,500,0,0)
bot.movestr(bot,bot.ipos,[0,0])
draw(bot,pts)