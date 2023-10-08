import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.spatial import ConvexHull

# Returns an np array of convex polygons (2D-np array)
#p is # of polygons, n_min/n_max are bounds on # of vertices, r_min/r_max are bounds on size, x/y-dim is size of grid
def make_polygons(p, n_min, n_max, r_min, r_max, xdim=2 ,ydim=2):
    # define center of all the polygons
    center_pol = []
    
    for _ in range(p):
        x,y = random.uniform(0, xdim), random.uniform(0, ydim)
        num_vertices = random.randint(n_min, n_max)
        center_pol.append((x,y, num_vertices))

    polygons = []

    for center in center_pol:
        vertices = []
        for _ in range(center[2]):
            radius = random.uniform(r_min, r_max)
            angle = random.uniform(0,2*np.pi) #get angle in radians
            x,y = center[0] + radius*np.cos(angle), center[1] + radius*np.sin(angle)
            vertices.append([x,y])

        vertices = np.array(vertices)
        hull = ConvexHull(vertices)
        polygons.append(vertices[hull.vertices])
        
    return np.array(polygons, dtype = object)

def add_polygon_to_scene(polygon, ax, fill):
    pol = plt.Polygon(polygon, closed = True, fill=fill,color = 'black',alpha = 0.4)
    ax.add_patch(pol)

def create_plot():
    fig, ax = plt.subplots(dpi=100)
    return ax

# Takes in our generated polygons and generates scene that's 800 x 800 px
def show_scene(ax):
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    ax.set_aspect('equal')
    plt.gca().set_aspect('equal', adjustable='box')  # Make sure the aspect ratio is equal
    plt.grid(True)
    plt.show()

def save_polygons(polygons, filename):
    np.save(filename,arr=polygons,allow_pickle=True)

def load_polygons(filename):
    return np.load(filename,allow_pickle=True)



if __name__ == '__main__':
    ax = create_plot()
    for p in make_polygons(2,25,50,0.3,0.6):
        add_polygon_to_scene(p,ax,True)
    show_scene(ax)