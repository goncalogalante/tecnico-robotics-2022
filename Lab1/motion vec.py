import serial
import time
import math
from target_points_final import image_processing


def dist(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class scorbot:
    def __init__ (self):
        """Init function of the class, checks the serial connection and initializes the class variables"""
        if serial:
            self.com = serial.Serial("COM3", baudrate=9600, bytesize=8, timeout=2, parity="N", xonxoff=0)
        self.ipos=[0,0,0]
        pass
    
    def send(self, msg):
        """Takes as argument a string and sends it 
           in the proper format to the serial manipulator"""
        self.com.write(bytes(msg,'UTF-8'))
        pass

    def initpos(self,x,y,z,r):
        """Changes the reference position coordinates
           to have the home position coordinates,
           which is a centimetre above the paper's
           reference position"""
        self.ipos[0]=x
        self.ipos[1]=y
        self.ipos[2]=z + 100
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

    def movestr(self, coordi, coordf):
        """Function used in the first approach, repeatedly called for 
           all the target points in the image"""

        # sets the coordinates of the next point, always relative to the reference position
        self.send("SETPVC 1 X " + str(self.ipos[0]+int(coordf[0])) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(self.ipos[1]+int(coordf[1])) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]-100) + "\r")
        time.sleep(0.5)

        # Calculation of the time of the movement based on a fixed value of 0.3 seconds
        # plus a factor (alpha) 2 seconds per 10 cm that is multiplied by the distance in the movement
        alpha = 2/1000
        move_time = round(100*(0.3 + alpha*dist((coordi[0],coordi[1]),(coordf[0],coordf[1]))))

        # Sets the movement for the calculated time
        self.send("MOVE 1 " + str(move_time) + "\r")
        time.sleep(move_time/100)

    def movehome(self):
        """Saves the current position to have the correct pitch and pen orientation.
           Afterward moves to the home position 1 centimetre above the paper"""
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

        # sets the reference z position to the paper level
        self.send("SETPVC 1 Z " + str(self.ipos[2]-100) + "\r")
        time.sleep(0.5)
    
    def moveup(self,coord):
        """Moves vertically two centimetres relative two the
           reference position z coordinate"""
        self.send("SETPVC 1 X " + str(coord[0]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Y " + str(coord[1]) + "\r")
        time.sleep(0.5)
        self.send("SETPVC 1 Z " + str(self.ipos[2]+100) + "\r")
        time.sleep(0.5)
        self.send("MOVE 1 500" + "\r")
        time.sleep(0.6)

    def create_vector(self,N):
        """Receives the number of points of the desired vector and
           defines the name of the vector, sending a command for
           it's creation to the serial manipulator and 
           returning the name of the vector"""

        vect_name = "POSY"
        self.send("DIMP " + vect_name + " [" + str(N) + "]" + "\r")
        time.sleep(1)
        self.read_and_wait(0.5)
        return vect_name
    
    def add_vector(self,coord,n,vect_name):
        """Adds the point to the given vector on the given position"""

        # Copies the reference position and changes the x and y
        self.send("SETP " + vect_name + "[" + str(n) + "]=1" + "\r")
        time.sleep(0.5)
        self.read_and_wait(0.5)
        self.send("SETPVC " + vect_name + "[" + str(n) + "] X " + str(self.ipos[0]+int(coord[0])) + "\r")
        time.sleep(0.5)
        self.send("SETPVC " + vect_name + "[" + str(n) + "] Y " + str(self.ipos[1]+int(coord[1])) + "\r")
        time.sleep(0.5)


def start(self):
    """Start the robot, resetting both the input and output buffers,
       activating the axes and setting the speed to 1%
       The first position is beforehand manually selected"""
    
    self.com.flushInput()
    time.sleep(1)
    self.com.flushOutput()
    time.sleep(1)
    self.send("CON " + "\r")
    time.sleep(0.5)
    self.send("SPEED 1 " + "\r")

def homepos(self):
    """Recording of the home position, the reference position
       for the drawing that is beforehand defined.
       It sends the LISTPV POSITION command and
       analises the ouput, sending it as arguments
       to the initpos function"""

    # read from the buffer what there is to read
    msg = self.com.inWaiting()
    msg = self.com.read(msg)

    # send the command and wait for the full output
    self.send("LISTPV POSITION " + "\r")
    time.sleep(1)

    # reads the full output of the command
    msg = self.com.inWaiting()
    msg = self.com.read(msg)
    msg = str(msg)

    # gets only the last line of the output
    # containing the cartesian coordinates of the position
    msg = msg.split("X:")
    msg = msg[1]

    # by splitting again and having a positive x and a negative y
    # the following expressions can retrieve the coordinates
    msg = msg.split()
    x = int(msg[0])
    y = msg[1]
    y = int(y[2:])
    z = msg[3]
    z = int(z)

    # gets the coordinates to the class variables
    self.initpos(x,y,z)

def drawstr(self,pts):
    """Draw function for the first approach, repeatedly calling the
       movestr function for each point"""
    for i in range(len(pts)):
        if i==0:
            self.movestr(self,self.ipos,pts[i])
            self.read_and_wait(self,0.5)
        self.movestr(self,pts[i-1],pts[i])
    self.moveup(pts[i])

def draw(self,pts):
    """Takes the bot and the target points, creates the vector
       of points in the serial manipulator and instructs the
       movement through the points, ending on a vertical movement"""

    # initialize the vector with the required number of positions
    cnt = len(pts)
    vect_name = self.create_vector(cnt)
    self.read_and_wait(1)

    # for each set of coordinates, add them in the correct position
    # in the vector, looping through all the points
    for i in range(len(pts)+1):
        # The position indexes on the created vector start at one
        # so the position 1 of the vector corresponds to pts[0]
        if i == 0: 
            pass
        else: self.add_vector(pts[i-1],i,vect_name)
    time.sleep(0.5)

    # Calculates the movement time having 1.5 seconds per point
    move_time = cnt*150

    # Commands the serial manipulator to go through all the positions
    # in the defined movement time
    self.send("MOVES " + vect_name + " " + str(1) + " " + str(cnt) + " " + str(move_time) +"\r")
    self.read_and_wait(0.5)
    time.sleep(move_time/100)

    # reaching the final point, moves up to separate the pen from the paper
    self.moveup(pts[cnt-1])


# initializes the object
bot=scorbot()

# starts the serial manipulator
start(bot)

# registers the reference position
homepos(bot)

# moves to the home position
bot.movehome()

# Executes the image processing
pts = image_processing("test_draw_2.png")

"""To define the name of the vector go to the create_vector function"""
# Executes the drawing
draw(bot,pts)

# After the drawing, returns to the home position
bot.movehome()