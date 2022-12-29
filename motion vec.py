import numpy as np
import serial
import time
import math
import datetime
from target_points_v2 import image_processing

# pôr pos inicial com comando (centro ou cantos)
# receber coordenadas da pos inicial
# lista de listas de pontos

# Current position of robot: LISTPV POSITION (X,Y,Z,P,R)
# flush antes de read


def dist(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class scorbot:
    def __init__ (self):
        if serial:
            self.com = serial.Serial("COM5", baudrate=9600, bytesize=8, timeout=2, parity="N", xonxoff=0)
        self.ipos=[0,0,0,0]
        self.pitch=0
        pass
    
    def send(self, msg):
        self.com.write(bytes(msg,'UTF-8'))
        pass

    def initpos(self,x,y,z,p,r):
        self.ipos[0]=x
        self.ipos[1]=y
        self.ipos[2]=z + 100
        self.ipos[3]=r
        self.pitch=p
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
            if self.com.inWaiting() > 0:
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
        self.send("SETPVC 1 Z " + str(self.ipos[2]-100) + "\r")
        time.sleep(0.5)
        # rf=roll_calc(self,coordi,coordf)
        alfa = 1.2/1000
        move_time = round(100*(0.3 + alfa*dist((coordi[0],coordi[1]),(coordf[0],coordf[1]))))
        self.send("MOVE 1 " + str(move_time) + "\r")
        time.sleep(move_time/100)

    def movehome(self):
        self.send("HERE 1 " + "\r")
        time.sleep(0.5)        
        self.send("SETPVC 1 X " + str(self.ipos[0]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(self.ipos[1]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]) + "\r")
        time.sleep(0.5)
        self.send("MOVE 1 500" + "\r")
        time.sleep(0.6)
        self.send("HERE 1 " + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]-100) + "\r")
        time.sleep(0.5)
    
    def moveup(self,coord):
        self.send("SETPVC 1 X " + str(coord[0]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(coord[1]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]+100) + "\r")
        time.sleep(0.5)
        self.send("MOVE 1 500" + "\r")
        time.sleep(0.6)

    def create_vector(self,N):
        vect_name = "POSX"
        self.send("DIMP " + vect_name + " [" + str(N) + "]" + "\r")
        time.sleep(1)
        self.read_and_wait(0.5)
        return vect_name
    
    def add_vector(self,coord,n,vect_name):
        self.send("SETP " + vect_name + "[" + str(n) + "]=1" + "\r")
        time.sleep(0.5)
        self.read_and_wait(0.5)
        self.send("SETPVC " + vect_name + "[" + str(n) + "] X " + str(self.ipos[0]+int(coord[0])) + "\r")
        time.sleep(0.5)
        # self.read_and_wait(0.5)
        self.send("SETPVC " + vect_name + "[" + str(n) + "] Y " + str(self.ipos[1]+int(coord[1])) + "\r")
        time.sleep(0.5)
        # self.read_and_wait(0.5)


def start(self):
    """Start the robot, activating the axis and setting the speed to 50%
       The first position is beforehand manually selected"""
    self.com.flushInput()
    time.sleep(1)
    self.com.flushOutput()
    time.sleep(1)
    self.send("CON " + "\r")
    time.sleep(0.5)
    self.send("SPEED [A] 1 " + "\r")
    time.sleep(0.5)
    self.send("SPEED [B] 1 " + "\r")
    time.sleep(0.5)
    self.send("SPEED [C] 1 " + "\r")
    time.sleep(0.5)

def homepos(self):
    # self.com.flush()
    msg = self.com.inWaiting()
    msg = self.com.read(msg)
    msg = str(msg)
    # print(">>" + msg)
    # time.sleep(2)
    self.send("LISTPV POSITION " + "\r")
    time.sleep(1)
    # msg = self.read_and_wait(self,2) # LISTPV POSITION
    # print(">>" + msg)
    # msg = self.read_and_wait(self,2) # Joint coordinates
    # print(">>" + msg)
    # msg = self.read_and_wait(self,2) # Cartesian coordinates
    msg = self.com.inWaiting()
    msg = self.com.read(msg)
    msg = str(msg)
    # msg = "X: 3767    Y:-1727    Z:-723     P:-974     R:-201 >"
    msg = msg.split("X:")
    msg = msg[1]
    msg = msg.split()
    # print(">>" + str(len(msg)))
    x = int(msg[0])
    y = msg[1]
    y = int(y[2:])
    z = msg[3]
    z = int(z)
    # p = msg[-3]
    # p = p[2:]
    r = msg[5]
    r = int(r[2:])
    self.initpos(x,y,z,1,r)

def draw(self,pts):
    cnt = len(pts)
    vect_name = self.create_vector(cnt)
    # if ((self.read_and_wait(self,0.5)) == ">"):
    self.send("SPEED [A] 1 " + "\r")
    time.sleep(0.5)
    self.read_and_wait(1)
    for i in range(len(pts)+1):
        if i == 0:
            pass
        else: self.add_vector(pts[i-1],i,vect_name)
        # self.read_and_wait(self,0.5)
    self.send("SPEED [A] 1 " + "\r")
    time.sleep(0.5)
    max = math.floor(cnt/5)
    j=0

    if max!=0:
        for i in range(max):
            self.send("MOVES " + vect_name + " " + str(i*5 +1) + " " + str((i+1)*5) + "\r")
            # waitt = cnt*0.1
            self.read_and_wait(0.5)
            j=j+5

        if (((cnt-j) == 4) or ((cnt-j) == 3) or ((cnt-j) == 2)):
            dif = cnt-j
            self.send("MOVES " + vect_name + " " + str(cnt-dif+1) + " " + str(cnt) + "\r")
        else:
            self.send("MOVED " + vect_name + "[" + str(cnt) + "] 100" + "\r")   
    else:
        self.send("MOVES " + vect_name + " " + str(1) + " " + str(cnt) + "\r")
        self.read_and_wait(0.5)

    self.moveup(pts[cnt-1])
    

bot=scorbot()
start(bot)
homepos(bot)
# bot.initpos(4281,-353,1100,0,-201) # Scorbot 1
# bot.initpos(4953,-353,233,0,0) # Scorbot 2
# bot.com.flush()
print("X:" + str(bot.ipos[0]))
print("Y:" + str(bot.ipos[1]))
print("Z:" + str(bot.ipos[2]))
print("R:" + str(bot.ipos[3]))
bot.movehome()

# N=bot.create_vector(40)
# bot.add_vector((300,0),1,N)
# bot.add_vector((300,300),2,N)
# bot.add_vector((0,300),3,N)
# bot.add_vector((0,0),4,N)
# bot.add_vector((300,0),5,N)
# bot.add_vector((300,300),6,N)
# bot.add_vector((0,300),7,N)
# bot.add_vector((0,0),8,N)
# bot.add_vector((300,0),9,N)
# bot.add_vector((300,300),10,N)
# bot.add_vector((0,300),11,N)
# bot.add_vector((0,0),12,N)
# bot.add_vector((300,0),13,N)
# bot.add_vector((300,300),14,N)
# bot.add_vector((0,300),15,N)
# bot.add_vector((0,0),16,N)
# bot.add_vector((300,0),17,N)
# bot.add_vector((300,300),18,N)
# bot.add_vector((0,300),19,N)
# bot.add_vector((0,0),20,N)
# bot.add_vector((300,0),21,N)
# bot.add_vector((300,300),22,N)
# bot.add_vector((0,300),23,N)
# bot.add_vector((0,0),24,N)
# bot.add_vector((300,0),25,N)
# bot.add_vector((300,300),26,N)
# bot.add_vector((0,300),27,N)
# bot.add_vector((0,0),28,N)
# bot.add_vector((300,0),29,N)
# bot.add_vector((300,300),30,N)
# bot.add_vector((0,300),31,N)
# bot.add_vector((0,0),32,N)
# bot.add_vector((300,0),33,N)
# bot.add_vector((300,300),34,N)
# bot.add_vector((0,300),35,N)
# bot.add_vector((0,0),36,N)
# bot.add_vector((300,0),37,N)
# bot.add_vector((300,300),38,N)
# bot.add_vector((0,300),39,N)
# bot.add_vector((0,0),40,N)

# bot.read_and_wait(0.5)
# bot.send("MOVES " + "POSP " + str(1) + " " + str(10) + "\r")
# bot.read_and_wait(0.5)
# bot.send("MOVES " + "POSP " + str(11) + " " + str(20) + "\r")
# bot.read_and_wait(0.5)
# bot.send("MOVES " + "POSP " + str(21) + " " + str(30) + "\r")
# bot.read_and_wait(0.5)
# bot.send("MOVES " + "POSP " + str(31) + " " + str(40) + "\r")
# bot.read_and_wait(0.5)

pts = image_processing("test_draw_1.png")
draw(bot,pts)
bot.movehome()