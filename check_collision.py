import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.spatial import ConvexHull

# Returns a list of len() = p of plt.Polygon objects.
def make_polygons(p, n_min, n_max, r_min, r_max, xdim ,ydim):
    # define center of all the polygons
    center_pol = []
    
    for _ in range(p):
        x,y = random.uniform(0, xdim), random.uniform(0, ydim)
        num_vertices = random.randint(n_min, n_max)
        center_pol.append((x,y, num_vertices))

    polygons = []

    for center in center_pol:
        vertices = []
        print(center[2])
        for _ in range(center[2]):
            radius = random.uniform(r_min, r_max)
            angle = random.uniform(0,2*np.pi) #get angle in radians
            x,y = center[0] + radius*np.cos(angle), center[1] + radius*np.sin(angle)
            vertices.append([x,y])

        vertices = np.array(vertices)
        hull = ConvexHull(vertices)
        polygons.append(vertices[hull.vertices])
           
    return np.array(polygons, dtype = object)

def collides(polygon1, polygon2):
    edges1 = get_edges(polygon1)
    edges2 = get_edges(polygon2)

    normals1 = get_normals(edges1)
    normals2 = get_normals(edges2)

    for normal in normals1 + normals2:
        min1, max1 = project(polygon1, normal)
        min2, max2 = project(polygon2, normal)
        if max1 < min2 or max2 < min1:
            return False
    return True

def get_edges(polygons):
    edges = []
    for i in range(len(polygons)):
        edge = polygons[i] - polygons[(i + 1) % len(polygons)]
        edges.append(edge)
    return edges  
  
  
def get_normals(edges):
    normals = [np.array([-edge[1], edge[0]]) for edge in edges]
    return normals


def project(vertices, axis):
    min_proj = np.dot(axis, vertices[0])
    max_proj = min_proj
    for vertex in vertices[1:]:
        projection = np.dot(axis, vertex)
        if projection < min_proj:
            min_proj = projection
        elif projection > max_proj:
            max_proj = projection
    return min_proj, max_proj

# Takes in our generated polygons and generates scene that's 800 x 800 px
def show_scene(polygons):
    fig, ax = plt.subplots(dpi=100)
    visited = []
    for polygon in polygons:
        check = True
        for p in visited:
            if collides(polygon, p):
                pol = plt.Polygon(polygon, closed = True, color = 'r')
                check = False
                break
        if check == True:
            pol = plt.Polygon(polygon, closed = True, color = 'b')
        visited.append(polygon)
        ax.add_patch(pol)
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 800)
    plt.gca().set_aspect('equal', adjustable='box')  # Make sure the aspect ratio is equal
    plt.grid(True)
    plt.show()


show_scene(make_polygons(5, 5, 8, 100, 200, 800, 800))
        
