import matplotlib.pyplot as plt
import numpy as np
from  create_scene import make_polygons, show_scene, create_plot, add_polygon_to_scene

box_collisions = []
polygon_collisions = []

def bound_polygons(polygons):
    # List comprehension of polygons -> For each we get min and max vertices
    bbs = [np.array([polygon.min(axis=0), polygon.max(axis=0)]) for polygon in polygons]
    return bbs

#checks if 2 boxes intersect
def check_box_collision(bbox1, bbox2):
    return not (bbox1[1][0] < bbox2[0][0] or 
                bbox1[0][0] > bbox2[1][0] or 
                bbox1[1][1] < bbox2[0][1] or 
                bbox1[0][1] > bbox2[1][1])

# Loop over all pairs of polygons -> bound + check for intersection
def check_all_boxes(polygons):
    bb = bound_polygons(polygons) #bb is 2D array w/ same len() as polygons
    for i in range(len(bb)):
        for j in range(i+1, len(bb)):
            if check_box_collision(bb[i], bb[j]):
                box_collisions.append((polygons[i], polygons[j]))

#Helper method for getting edges of a polygon as list
def get_edges(polygons):
    edges = []
    for i in range(len(polygons)):
        edge = polygons[i] - polygons[(i + 1) % len(polygons)] #?
        edges.append(edge)
    return edges 

#Helper method for getting normal vector to edge as np-array
def get_normals(edges):
    normals = [np.array([-edge[1], edge[0]]) for edge in edges]
    return normals

# Helper method that projects polygon along an axis
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

# Using Separating axis theorem to check if 2 polygons collide with each other
def SAT_Collides(polygon1, polygon2):
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

if __name__ == '__main__':
    polygons = make_polygons(10, 4, 15, 80, 160, 800, 800)
    check_all_boxes(polygons) #broad-phase collision
    for pair in box_collisions:
        p1, p2 = pair #unpack polygons
        if SAT_Collides(p1, p2): polygon_collisions.append(pair) #SAT fine checking

    unique_colliding_polygons = set(tuple(str(polygon.tolist())) for pair in polygon_collisions for polygon in pair) #use list-comp to unpack tuples
    ax = create_plot()
    for polygon in polygons:
        if tuple(str(polygon.tolist())) in unique_colliding_polygons:
            add_polygon_to_scene(polygon, ax, 'red')
        else:
            add_polygon_to_scene(polygon, ax, 'blue')
    show_scene(ax)



    

        
