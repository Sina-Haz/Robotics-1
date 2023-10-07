import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
import numpy as np
from  create_scene import make_polygons, show_scene, create_plot, add_polygon_to_scene
from collision_checking import collides
import random

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
        step = 0.05
        if self.x() >= 0.02 and self.x() <= 1.8 and self.y() >= .02 and self.y() <= 1.85 : #see if the car moved beyond the grid
            if event.key == 'up':
                self.car.set_y(self.car.get_y() + step)
            elif event.key == 'down':
                self.car.set_y(self.car.get_y() - step)
            elif event.key == 'right':
                self.car.set_x(self.car.get_x() + step)
            elif event.key == 'left':
                self.car.set_x(self.car.get_x() - step)
            elif event.key == 'd':
                self.car.set(angle = self.degrees() + 45)
            elif event.key == 'a':
                self.car.set(angle = self.degrees() - 45)
            if(check_car(self.car, self.obstacles)): self.car.set(facecolor = "blue") #check if the car collides with any obstacle
            else: self.car.set(facecolor = "red")
        else:
            if self.x() < 0.02: self.car.set_x(0.02)
            elif self.x() > 1.8: self.car.set_x(1.8)
            elif self.y() < 0.02: self.car.set_y(0.02)
            elif self.y() >1.85: self.car.set_y(1.85)
        # Update the car's position
        self.fig.canvas.draw()
    

#Checks if the car collides with an obstacle
def check_car(car, obstacles):
    for polygon in obstacles:
        if not collides(polygon, get_coords(car)): return False
    return True

#Gets the coordinates for the car
def get_coords(r1):
    path = r1.get_path()
    vertices = path.vertices
    coords = np.array([r1.get_xy(), [r1.get_x()+r1.get_width(), r1.get_y()],
                   [r1.get_x()+r1.get_width(), r1.get_y()+r1.get_height()],
                   [r1.get_x(), r1.get_y()+r1.get_height()]]) 
    print(vertices)
    return coords


       
if __name__ == '__main__':
    obstacles = np.load('2d_rigid_body.npy', allow_pickle=True)
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




    

        
