import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
import numpy as np
from  create_scene import make_polygons, show_scene, create_plot, add_polygon_to_scene
from collision_checking import collides
import random
import math

#Controller to move the car using keyboard inputs
class CarController:
    def __init__(self, ax, car, obstacles):
        # Initial position of the point
        self.car = car
        self.x, self.y = car.get_x, car.get_y
        self.ax = ax
        self.obstacles = obstacles
        self.ax.add_patch(car)
        self.degrees = car.get_angle
        self.fig = ax.figure
        # Set the axis limits
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 2)
        # Connsect the event to the callback function
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def on_key_press(self, event):
        # Define step size for arrow key movement
        step = 0.01
        prev = ["x", 0]
        if event.key == 'up':
            if check_boundary(self.car,1,2):
                self.car.set_y(self.car.get_y() + step)
                prev = ["y", step*-1]
        elif event.key == 'down':
            if check_boundary(self.car, 1,0):
                self.car.set_y(self.car.get_y() - step)
                prev = ["y", step]
        elif event.key == 'right':
            if check_boundary(self.car, 0,2):
                self.car.set_x(self.car.get_x() + step)
                prev = ["x", step*-1]
        elif event.key == 'left':
            if check_boundary(self.car, 0,0):
                self.car.set_x(self.car.get_x() - step)
                prev = ["x", step]
        elif event.key == 'a':
            self.car.set(angle = self.degrees() + 10)
            prev = ["a", -10]
        elif event.key == 'd':
            self.car.set(angle = self.degrees() - 10)
            prev = ["a", 10]
        if(not check_car(self.car, self.obstacles)): 
            if prev[0] == "x": self.car.set_x(self.car.get_x() + prev[1]) 
            elif prev[0] == "a": self.car.set(angle = self.degrees() + prev[1])
            else: self.car.set_y(self.car.get_y() + prev[1]) 
            
        # Update the car's position
        self.fig.canvas.draw()
    


def check_boundary(car, i, j):
    coords = get_coords(car)
    for x in coords:
        if i == 0 and j == 2:
            if x[i] > j- .01: return False
        elif i == 0 and j == 0:
            if x[i] < j+.01: return False
        elif i == 1 and j == 2:
            if x[1] > j-.01: return False
        elif i == 1 and j == 0:
            if x[1] < j+0.01: return False
    return True
    
#Checks if the car collides with an obstacle
def check_car(car, obstacles):
    for polygon in obstacles:
        if not collides(polygon, get_coords(car)): return False
    return True

#Gets the coordinates for the car
def get_coords(r1):
    r = Affine2D().rotate_deg_around(r1.get_x(),r1.get_y(),r1.get_angle())
    coords = np.array([r1.get_xy(), [r1.get_x()+r1.get_width(), r1.get_y()],
                   [r1.get_x()+r1.get_width(), r1.get_y()+r1.get_height()],
                   [r1.get_x(), r1.get_y()+r1.get_height()]]) 

    return r.transform(coords)


       
if __name__ == '__main__':
    obstacles = np.load('assignment1_student/2d_rigid_body.npy', allow_pickle=True)
    ax = create_plot()
    for polygon in obstacles:
        add_polygon_to_scene(polygon,ax, 'blue')
    car = []
    while(True):
        x,y = random.uniform(0, 1.8), random.uniform(0, 1.8)
        car = patches.Rectangle((x,y),0.2,0.1,linewidth = 1, edgecolor = 'r', facecolor = 'blue')
        if(check_car(car, obstacles)): break
    ax.add_patch(car)
    controller = CarController(ax, car, obstacles)
    show_scene(ax)




    

        
