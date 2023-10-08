from create_scene import create_plot, make_polygons, show_scene, add_polygon_to_scene
import matplotlib.patches as patches
from numpy import cos, sin, degrees, pi, radians
import matplotlib.pyplot as plt

# This class is used to control the planar arm using keyboard input
class Arm_Controller:
    
    #Define a function that computes where the center of the rectangle is for some theta value (in radians)
    @staticmethod
    def compute_rect_anchor(theta, center, rad, width):
        x = rad*cos(theta)
        y = rad*sin(theta)

        vector = (x,y)
        
        # Get a vector perpendicular to radius of circle
        orth = (-y/rad, x/rad)
        scaled_orth = (orth[0] * width/2, orth[1] * width/2)
        anchor = (center[0]+vector[0]+scaled_orth[0], center[1]+vector[1]+scaled_orth[1])
        return anchor
    
    # Computes center of the next joint with respect to original joint, theta, length of the arm, and joint radii
    @staticmethod
    def compute_circle_center(theta, center, rad, rlen):
        total_rad = rad*2+rlen
        x = center[0]+total_rad*cos(theta)
        y = center[1]+total_rad*sin(theta)
        return(x,y)
    

    def __init__(self,theta1,theta2,ax):
        self.ax = ax
        self.joint1 = (1,1) #Center of the first circle
        self.rad = 0.05 #radius of all joints
        self.rwid = 0.1 #width of both rectangles
        self.rlen1 = 0.4 #Length of first rectangle
        self.rlen2 = 0.25 #Length of 2nd rectangle
        self.theta1 = theta1 #First theta value
        self.theta2 = theta2
        self.anchor1 = Arm_Controller.compute_rect_anchor(self.theta1, self.joint1, self.rad, self.rwid) #Anchor of 1st rectangle
        self.joint2 = Arm_Controller.compute_circle_center(self.theta1, self.joint1, self.rad, self.rlen1)
        self.anchor2 = Arm_Controller.compute_rect_anchor(self.theta2, self.joint2, self.rad, self.rwid)
        self.joint3 = Arm_Controller.compute_circle_center(self.theta2,self.joint2,self.rad, self.rlen2)


    def draw_arm(self):
        joint1 = patches.Circle(self.joint1, self.rad, fill=True, color='b')
        rect1 = patches.Rectangle(self.anchor1,self.rwid,self.rlen1, fill=True,color='g')
        rect1.set_angle(degrees(self.theta1 - pi/2))
        joint2 = patches.Circle(self.joint2,self.rad, fill=True,color='b')
        rect2 = patches.Rectangle(self.anchor2,self.rwid, self.rlen2, fill=True,color='g')
        rect2.set_angle(degrees(self.theta2 - pi/2))
        joint3 = patches.Circle(self.joint3,self.rad,fill=True,color='b')
        self.ax.add_patch(joint1)
        self.ax.add_patch(rect1)
        self.ax.add_patch(joint2)
        self.ax.add_patch(rect2)
        self.ax.add_patch(joint3)
        show_scene(self.ax)

    # Call this function when angles are changed to recompute the position of the anchors and joints
    def re_orient(self):
        self.anchor1 = Arm_Controller.compute_rect_anchor(self.theta1, self.joint1, self.rad, self.rwid)
        self.joint2 = Arm_Controller.compute_circle_center(self.theta1, self.joint1, self.rad, self.rlen1)
        self.anchor2 = Arm_Controller.compute_rect_anchor(self.theta2, self.joint2, self.rad, self.rwid)
        self.joint3 = Arm_Controller.compute_circle_center(self.theta2,self.joint2,self.rad, self.rlen2)

    # On arrow key click change either theta 1 or theta 2 by 5 degrees
    def on_key(self, event):
        if event.key == 'left':
            self.theta1 -= radians(5)
        elif event.key == 'right':
            self.theta1 += radians(5)
        elif event.key == 'up':
            self.theta2 += radians(5)
        elif event.key == 'down':
            self.theta2 -= radians(5)
        
        # Clear the current axis and redraw the arm
        self.ax.cla()
        self.re_orient()
        self.draw_arm()
        self.ax.figure.canvas.draw()
        




if __name__ == '__main__':
    fig,ax = plt.subplots(dpi=100)
    arm = Arm_Controller(radians(30), radians(-30),ax)
    arm.ax.figure.canvas.mpl_connect('key_press_event', arm.on_key)
    arm.draw_arm()
    show_scene(arm.ax)

    
    
