import numpy as np
import pandas as pd
import math
import vehicle_specs
import matplotlib.pyplot as plt
import time

def generate_trajectory(type):
    
    if type == 1:
        trajectory = [(i/10, 5, 0, 0) for i in range(8000)]
    
    # trajectory = [(i, (i/50)**2, 0, 0) for i in range(8000)]
    
    # 2 levels
    if type == 2:
        trajectory = []
        x = 0
        y = 0
        counter = 0
        for i in range(15000):
            point = (x, y, 1, 0)
            trajectory.append(point)
            x += 0.1
            if y == 10:
                counter += 1
                if counter == 4000:
                    y = 0
                    counter = 0
            else:
                counter += 1
                if counter == 4000:
                    y = 10
                    counter = 0
     
    # 3 levels               
    if type == 3:
        trajectory = []
        x = 0
        y = 5
        counter = 0
        for i in range(15000):
            point = (x, y, 0, 0)
            trajectory.append(point)
            x += 0.1
            if y == 5:
                counter += 1
                if counter == 700:
                    y = 3
                    counter = 0
            elif y == 3:
                counter += 1
                if counter == 3500:
                    y = 0
                    counter = 0
            else:
                counter += 1
                if counter == 3500:
                    y = 5
                    counter = 0
    # curve
    if type == 4:
        trajectory = []
        x = 0
        counter = 0
        for i in range(2000):
            y = 2.5 * (1 + math.sin(0.01*x))
            point = (x, y, 0, 0)
            trajectory.append(point)
            x += 0.1
            counter += 1

    return trajectory


def kinematics(current_pos, current_vel, ws, dt):
    
    # print("Current position:", current_pos, "Current velocity:", current_vel, "Angular velocity", ws)
    x_now = current_pos[0] # current x
    y_now = current_pos[1] # current y
    theta_now = current_pos[2] # current theta
    phi_now = current_pos[3] # current phi
    
    if phi_now > math.pi/8:
        phi_now = math.pi/8
    elif phi_now < -math.pi/8:
        phi_now = -math.pi/8
    
    # mobile robot kinematics
    vel_x, vel_y, vel_theta, vel_phi = np.array([[np.cos(theta_now), 0], [np.sin(theta_now), 0], [(np.tan(phi_now)/vehicle_specs.L), 0], [0, 1]])* np.array([current_vel, ws])
    
    # compute new positions    
    # x_new = x_now + vel_x[0]
    # y_new = y_now + vel_y[0]
    # theta_new = theta_now + vel_theta[0]
    # phi_new = phi_now + vel_phi[1]
    
    x_new = x_now + vel_x[0] * dt
    y_new = y_now + vel_y[0] * dt
    theta_new = theta_now + vel_theta[0] * dt
    phi_new = phi_now + vel_phi[1] * dt
    
    if phi_new > math.pi/8:
        phi_new = math.pi/8
    elif phi_new < -math.pi/8:
        phi_new = -math.pi/8
    
    # vector of new positions
    new_pos = (x_new, y_new, theta_new, phi_new)
    
    return new_pos     

class Car_controller():

    def __init__(self, Kv, Ks, Ki):
        self.Kv = Kv
        self.Ks = Ks
        self.Ki = Ki
        self.integral_error = [0,0,0]
        
    def controlador(self, current_pos, trajectory, dt):
        
        x_now = current_pos[0] # current x
        y_now = current_pos[1] # current y
        theta_now = current_pos[2] # current theta
        phi_now = current_pos[3] # current phi
        
        x_ref = trajectory[0] # trajectory x
        y_ref = trajectory[1] # trajectory y
        theta_ref = trajectory[2] # trajectory theta
        
       
        
        we = [x_ref - x_now, y_ref - y_now, theta_ref - theta_now]
        
        u = [[np.cos(theta_now), np.sin(theta_now), 0], [-np.sin(theta_now), np.cos(theta_now), 0], [0, 0, 1]]
        
        be = np.matmul(u, we)
        
        self.integral_error += be * dt

        v = self.Kv * be[0]
        ws = self.Ks * be[2] + self.Ki * be[1]
      
        output = (v, ws)

        return output
   