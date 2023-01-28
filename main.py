import numpy as np
import pandas as pd
import math
import vehicle_specs
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import cv2
import networkx as nx

from Controller_clean_v2 import kinematics, Car_controller

from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

def click_initial_goal(event):
    global clicks
    global initial_point
    global final_point
    
    # select the initial and goal points
    if clicks == 0:
        initial_point = (round(event.xdata, ndigits=2), round(event.ydata, ndigits=2))
        print("Initial point set to: ", initial_point)
        plt.scatter(event.xdata, event.ydata, color='r', marker='$i$', s=90)
        plt.draw()
    elif clicks == 1:
        goal_point = (round(event.xdata, ndigits=2), round(event.ydata, ndigits=2))
        print("Goal point set to: ", goal_point)
        plt.scatter(event.xdata, event.ydata, color='r', marker='$G$', s=85)
        plt.draw()
        print("\n> Click on E key to close the map.")
    else:
        print("You have already set the initial and final points.")
        print("> Click on E key to close the map.")
    clicks += 1


def save_to_excel(points):
    df = pd.DataFrame(points, columns=['X', 'Y'])
    
    # df.to_excel('coordiantes.xlsx', index=False)
    # print(f'Data Saved in coordinates.xlsx')
    
    df.to_excel('Nodes.xlsx', index=False)
    print(f'Data Saved in Nodes.xlsx') 


def key_press_close(event):
    if event.key == 'e':
        plt.close()         
        #save_to_excel(node_points)
        

def on_key_node(event, type):
    global clicks
    clicks += 1
    if event.key == 'n':
        max_nodes = 30
        if clicks <= max_nodes:
            if type == 1:
            
                node_point = (round(event.xdata, ndigits=2), round(event.ydata, ndigits=2))
                print("node", clicks, "set to: ", node_point)
                node_points.append(node_point)
                #plt.scatter(event.xdata, event.ydata, color='r', marker=s, s=70)
                plt.annotate(str(clicks), (event.xdata, event.ydata), textcoords="offset points",xytext=(-0.5,0.5), ha='center', fontsize=10, color='r')
                plt.draw()
    
        else:
            print("You have set all 30 the relevant nodes.")
            print("> Click on E key to close the map.")


def nodes_to_graph(node_input, node_output):
    
    # directional graph
    G = nx.DiGraph()

    # add edges to the graph
    for i in range(len(node_input)):
        G.add_edge(node_input[i], node_output[i], weight=weights[i])
        
    # print((G.edges(data=True)))
    
    # return the graph
    return G

    
def display_trajectory(path, x_nodes, y_nodes):
    
    global x_points
    global y_points 
    
    for i in range(len(path)-1):
        
        distance = math.sqrt((x_nodes[path[i]-1] - x_nodes[path[i+1]-1])**2 + (y_nodes[path[i]-1] - y_nodes[path[i+1]-1])**2)
        
        # determine the number of points between 2 consecutive nodes based on the distance between 2 nodes
        if distance < 10:
            num = 10
        elif distance < 20:
            num = 25
        elif distance < 30:
            num = 35
        elif distance < 40:
            num = 45
        elif distance < 50:
            num = 55
        elif distance < 60:
            num = 65
        elif distance < 70:
            num = 75
        elif distance < 80:
            num = 85
        elif distance < 100:
            num = 100
        elif distance < 200:
            num = 150
        elif distance < 300:
            num = 250
        elif distance < 400:
            num = 350
        else:
            num = 500
        
        # assigns the list of all points which the car will follow
        x_points += np.linspace(x_nodes[path[i]-1], x_nodes[path[i+1]-1], num=num).tolist()
        y_points += np.linspace(y_nodes[path[i]-1], y_nodes[path[i+1]-1], num=num).tolist()
    
    # plot the supposed trajectory that the car should do
    fig = plt.figure(figsize=(12, 9))
    plt.imshow(img)
    plt.title('Theoretical trajectory for the car')
    plt.scatter(x_nodes, y_nodes, s=11)
    for i, label in enumerate(labels):
        plt.annotate(label, (x_nodes[i], y_nodes[i]), color='r')
    plt.plot(x_points, y_points, color = 'r')
    plt.connect('key_press_event', key_press_close)
    plt.show()   
    

def update_frame(frame_number):

    x1, y1, _, __ = car_positions[frame_number-1]
    x2, y2, _, __ = car_positions[frame_number]
    x, y, theta,_ = car_positions[frame_number]
    theta = np.arctan2(y2 - y1, x2 - x1)
    rect.set_xy((x - rect_size/2, y - rect_height/2))
    rotation_transform.clear().rotate_deg_around(x, y, np.degrees(theta))    
    

def energy_budget(mass, velocity, acceleration, P0, time_interval):
    energy_used = (mass * abs(acceleration) * abs(velocity) + P0) * time_interval
    return energy_used

"""END OF FUNCTIONS"""
        
# open the map image
img = cv2.imread('google_maps_ist.jpeg')

# variable starting     
clicks = 0
initial_point = None
final_point = None

# list of all points which the car will follow
x_points = []
y_points = []

# list of the initial and goal points
init_goal_points = []

# list of node points to save to excel
node_points = []             

# nodes list | dictionary
labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
x_nodes = [695.07, 609.11, 511.57, 498.51, 476.84, 455.9, 459.26, 446.17, 475.08, 485.29, 135.97, 121.7, 127.87, 114.21, 82.73, 31.65, 121.7, 128.48, 127.8, 106.91, 105.66, 121.66, 162.73, 445.48, 458.82, 481.62, 509.21, 508.8, 496.4, 508.44, 498.27, 456.82]
y_nodes = [28.37, 32.31, 35.02 ,48.32, 36.5, 49.3, 388.78, 403.17, 441.49, 465.08, 404.39, 391.35, 63.65, 37.12, 22.86, 17.12, 417.04, 677.48, 743.1, 795.32, 961.3, 973.47, 972.74, 973.02, 984.93, 971.19, 983.61, 959.38, 438.93, 388.7, 4.95, 4.95]
node_input = [1, 2, 2, 3, 3, 3, 4, 4, 4,  5,6, 7, 7,    8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 24, 26, 26, 27, 28, 28, 29, 30, 32] # 46 connections
node_output =[2, 1, 3, 2, 5,31, 3, 5, 31, 6, 7, 8, 9, 11, 10, 29, 28, 29, 12, 17, 13, 17, 14, 12, 13, 15, 14, 16, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 25, 28, 28, 10, 26, 30, 4, 6] # 46 connections
weights =    [1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1] # 46 weights

print("\n>>> Self-Driving Car simulation <<<")


print("\n> Input below: \n 1) the inital point of the trajectory\n 2) the final point of the trajectory\n 3) the constant value PO")
print("> Advise: The points can be seen from the file 'points.png'")

# # plot the nodes on the map to chose the inicial and goal points
# fig = plt.figure(figsize=(10, 9))
# plt.imshow(img)
# plt.scatter(x_nodes, y_nodes, s=11)
# for i, label in enumerate(labels):
#     plt.annotate(label, (x_nodes[i], y_nodes[i]), color = 'r')
# fig.savefig("points.png")
# plt.show()

# define the initial point
while True:
    user_initial_point = input("\n> Enter the initial point:")
    if int(user_initial_point) > 0 and int(user_initial_point) < 32:
        print(">> Done! The initial point of the trajectory is set to: ", user_initial_point)
        break
    else:
        print(">> Error: initial point must be between 0 and 32. Enter again")

# define the final point
while True:
    user_goal_point = input("Enter the goal point: ")
    if int(user_goal_point) > 0 and int(user_initial_point) < 32:
        print(">> Done! The goal point of the trajectory is set to: ", user_goal_point)
        break
    else:
        print(">> Error: goal point must be between 0 and 32")
        

user_PO_value = input("Enter the PO constant value: ")
print(">> Done! The PO constant is set to: ", user_PO_value)

# user inputs to int
user_initial_point = int(user_initial_point)
user_goal_point = int(user_goal_point)
user_PO_value = int(user_PO_value)


# initial node and goal node 
source_node = user_initial_point
goal_node = user_goal_point

# convert nodes to a graph 
G = nodes_to_graph(node_input, node_output)

# find the shortest path with dijkstra algorithm
shortest_path = nx.dijkstra_path(G, source_node, goal_node, weight='weight')

# print the shortest path
print("\n> Shortest path is being generated..")

time.sleep(2.5)

# print the shortest path
print(">> Shortest path from ", source_node, "to", goal_node,"path:", shortest_path)

print(">> Click on E key to close the plot.")

# display supposed trajectory by the car
display_trajectory(shortest_path, x_nodes, y_nodes)



# define the trajectory without theta
trajectory = [(x, y, 0, 0) for x, y in zip(x_points, y_points)]

# define the trajectory with theta 
for i in range(len(trajectory)-1):
    x1, y1 = trajectory[i][0], trajectory[i][1]
    x2, y2 = trajectory[i+1][0], trajectory[i+1][1]
    theta = np.arctan2(y2 - y1, x2 - x1)
    trajectory[i] = (x1, y1, theta, 0)

# define initial position of the car
current_pos = trajectory[0]

# create instance for controler
car_control = Car_controller(Kv=0.5, Ks=18.5, Ki=1.9)

# create list of scores
errors_x = []
errors_y = []

# defining a time
dt = 0.95
times = []
car_positions = []
energy_spent_list = []

current_vel = 0
# control and move the car according to the kinematics
for i, desired_pos in enumerate(trajectory):
    
    # print("Trajectory points nº", i)
    print("Desired position:", (desired_pos[0], desired_pos[1],desired_pos[2]), "\nCurrent position:", current_pos)
    error_ = abs(1-(np.array(current_pos) / np.array(desired_pos)))
    
    control_signal = car_control.controlador(current_pos, desired_pos, dt)
    
    previous_vel = current_vel
    current_vel = control_signal[0]
    #print("Control signal - velocity:", current_vel)
    angular_vel = control_signal[1]
    #print("Control signal - ang velocity:", angular_vel)
    
    current_pos = kinematics(current_pos, current_vel, angular_vel, dt)
    
    acceleration = (current_vel - previous_vel) / dt
    energy_spent = energy_budget(mass=vehicle_specs.Mass, velocity=current_vel, acceleration=acceleration, P0 = user_PO_value, time_interval=dt)
    energy_spent_list.append(energy_spent)
    
    
    errors_x.append(error_[0])
    errors_y.append(error_[1])
    car_positions.append(current_pos)
    #print("----------------------------- X ------------------------------")
    times.append(dt*i)

total_energy_spent = sum(energy_spent_list)
# variables to plot
x = [point[0] for point in trajectory]
y = [point[1] for point in trajectory]
x_car = [point[0] for point in car_positions]
y_car = [point[1] for point in car_positions]
theta_car = [point[2] for point in car_positions]

# # plot the trajectory
# plt.plot(x, y)
# plt.plot(x_car, y_car)
# plt.title('Trajectory')
# plt.xlabel('Meters')
# plt.ylabel('Y')
# plt.show()

# # plot the trajectory
# plt.plot(times, theta_car)
# plt.title('Theta')
# plt.xlabel('Time (s)')
# plt.ylabel('Y')
# plt.show()

# # plot the error for x coordinate
# plt.plot(times, errors_x)
# plt.title('x-coordinate error')
# plt.xlabel('Time (s)')
# plt.ylabel('Error (m)')
# plt.show()

# # plot the error for y coordinate
# plt.plot(times, errors_y)
# plt.title('y-coordinate error')
# plt.xlabel('Time (s)')
# plt.ylabel('Error (m)')
# plt.show()

# live animation of the car
fig1, ax = plt.subplots(figsize = (12,9))
ax.imshow(img)
rect_size, rect_height = 14, 8

x, y,_,__ = trajectory[0]
rect = Rectangle((x - rect_size/2, y - rect_height/2), rect_size, rect_height, fill=True, color='r')
rotation_transform = Affine2D().rotate_deg_around(x, y, np.degrees(theta))
rect.set_transform(rotation_transform + ax.transData)

ax.add_patch(rect)

print("\n> The car is on his way..\n")
print(">> Click on E key to close the Animation.")

fig1.suptitle("Car completing the trajectory", fontsize=14, fontweight='bold')
ani = animation.FuncAnimation(fig1, update_frame, frames=range(len(trajectory)), interval=0, repeat = False)    
plt.connect('key_press_event', key_press_close)
plt.show()

print("\n> The car reached his destination.\n")

time.sleep(2)

print("\n> Generating the car's trajectory..")

time.sleep(3.5)
# plot the trajectory that the car did
fig = plt.figure(figsize=(12, 9))
plt.imshow(img)
plt.title('Car trajectory track on IST Alameda Campus')
print(">> Click on E key to close the plot.")
plt.plot(x_car, y_car)
plt.connect('key_press_event', key_press_close)
plt.show()


print("\n- Total Energy Spent:", round(total_energy_spent,ndigits=2),"Joules")
print("- Total Nº of Colisions:")