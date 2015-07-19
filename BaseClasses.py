#BaseClasses.py
#Contains Face and Shape classes, and MAG and DISP global functions
#The observer is at (0, 0, 0), "home" is (0, 0, 300)
from random import randint, choice
from math import sqrt, cos, sin, pi
from math import radians as rd
from turtle import *

#===============GLOBS
CURVE = 300
STRAIGHT = 900
#===============


myscrn = Screen()
myscrn.setup(1600, 900)
colormode(255)
bgcolor((10, 10, 10))
T = RawTurtle(myscrn)
T.pu()
T.pensize(1)
T.color((0, 0, 0), (40, 40, 140))
T.hideturtle()
T.pen(shown=False)
tracer(0)

#MAGNITUDE/DISTANCE FROM ANOTHER POINT - DEFAULT IS 0,0,0
def MAG(pt, compare = (0, 0, 0)):
    total = 0
    for i in range(3):
        total += (pt[i] - compare[i])**2
    return total**0.5


#FOR CALCULATING PLOT LOCATION ON SCREEN
def DISP(x, y=None, z=None):
    if y== None: #point passed in a collection
        x, y, z = x[0], x[1], x[2]
    if z <= 0:
        return None
    disp_x = (x * CURVE * (1/(1+MAG((x, y, z))))) + (x * (STRAIGHT/z))
    disp_y = (y * CURVE * (1/(1+MAG((x, y, z))))) + (y * (STRAIGHT/z))
                # position by magnitude..........position by z value
    return (disp_x, disp_y)



#===========================


class Face:
    def __init__(self, pts = None, color = None):
        if not pts:
            self.pts = []
        else:
            self.pts = pts
        if not color:
            self.color = [randint(0, 255) for x in range(3)]
        else:
            self.color = color

    def add(self, *args):
        for pt in args:
            self.pts.append(pt.copy())
            
    def center(self):
        #gives a single point - avg of x, y, z values
        totals = [0, 0, 0]
        for pt in self.pts:
            for i in range(3):
                totals[i] = totals[i] + pt[i]
        for i in range(3):
            totals[i] = totals[i]/len(self.pts)
        return totals
    
    def shift(self, vect): #shifts whole face along a vector
        for pt in self.pts:
            for i in (0, 1, 2):
                pt[i] = pt[i] + vect[i]
        
    def map(self, m, norm = (0, 0, 0)): #maps all points through a matrix, normalizing to (0, 0, 0) first.
        #NORMALIZE
        
        n1, n2, n3 = self.center()
        x, y, z = norm[0] - n1, norm[1] - n2,norm[2]- n3
        self.shift((x, y, z))
        
        ptidx = 0
        for pt in self.pts:
            newpt = []
            for row in (0, 1, 2):
                newpt.append(pt[0]*m[row][0] + pt[1]*m[row][1] + pt[2]*m[row][2])
            
            self.pts[ptidx] = newpt.copy()
            ptidx += 1
        self.shift((-x, -y, -z))

    def dist(self, compare =(0, 0, 0)):
        #distance from observer or another point - avg of points' magnitudes (not exactly center)
        #used for order of display in Shape class.
        total = 0
        for pt in self.pts:
            total += MAG(pt, compare)
        return total / len(self.pts)
    
    
    def rotate(self, a, dim, norm = (0, 0, 0)):
        #rotates through dimension by angle a.
        a = rd(a)
        if dim == "x":
            m = ((1,   0,       0,),
                 (0, cos(a), -sin(a)),
                 (0, sin(a), cos(a)))
        elif dim =="y":
            m = ((cos(a), 0, -sin(a)),
                 (0,      1,      0),
                 (sin(a), 0, cos(a)))
        elif dim == "z":
            m = ((cos(a), -sin(a), 0),
                 (sin(a), cos(a), 0),
                 (0,      0,     1))
        else:
            raise ValueError
        self.map(m, norm)
    def copy(self):
        newfc = Face([], self.color)
        for pt in self.pts:
            newfc.pts.append(pt.copy())
        return newfc
    def __str__(self):
        return str(self.pts)

"""
Shape class
has a list of Faces. Has a rawturtle object that draws it.
Has bools Wireframe - if True, no fills, just light lines.

Xsortfaces() - #sorts faces by closeness to observer.
XDrawface()- for a single face?
XShow() - draws shape faces to screen. ONLY call sortfaces() here.
X--Show also does the math for display coordinates.

- separate 'show' versions of these 3 that display the animation.
---incrementally, using Show()
---The "show" part of transformation functions are by default False.

Make a Copy constructor and a + operator.
(+ operator takes faces or other shapes)
"""
class Shape:
    def __init__(self, fcs=None, T=None, Wireframe=False):
        if not fcs:
            self.fcs = []
        else:
            self.fcs = fcs
        self.T = T
        self.Wireframe = Wireframe

    def __str__(self):
        s = ""
        for f in self.fcs:
            s += str(f) + "\n"
        return s

    def center(self):
        #center pt/vector of object x,y,z
        xtot, ytot, ztot = 0,0,0
        n = len(self.fcs)
        for f in self.fcs:
            x, y, z = f.center()
            xtot += x
            ytot += y
            ztot += z
        xtot /= n
        ytot /= n
        ztot /= n
        return (xtot, ytot, ztot)
    
    def add(self, item):
        #merges with either a face or another shape 
        if type(item) == Face:
            self.fcs.append(item)
        elif type(item) == Shape:
            for f in item.fcs:
                self.add(f)
            
    def sort_faces(self):
        #puts faces in display order (for drawing to screen)
        self.fcs.sort(key = lambda face: -face.dist())

    def draw_face(self, idx):
        #Draws a single face to screen - by index in fcs
        gotopts = []
        col = self.fcs[idx].color
        for pt in self.fcs[idx].pts:
            newpt = DISP(pt)
            if newpt != None:
                gotopts.append(newpt)
        if len(gotopts) < 1:
            return
        elif len(gotopts) == 1:
            T.goto(gotopts[0])
            T.dot(12, col)
            return
        
        T.goto(gotopts[0])
        T.color(col, col)
        T.pd()
        if not self.Wireframe:
            T.begin_fill()
        for pt in gotopts[1:]:
            T.goto(pt)
        T.goto(gotopts[0])
        if not self.Wireframe:  
            T.end_fill()
        T.pu()

    def show(self, sortFaces=True):
        #shape is drawn to screen.
        if sortFaces:
            self.sort_faces()
        T.clear()
        for i in range(len(self.fcs)):
            self.draw_face(i)
        tracer(1)
        tracer(0)#maybe do this externally later
    
    def rotate(self, a, dim:str, norm = (0,0,0)):
        #rotates all faces through dim by angle a
        x, y, z = self.center()
        
        for f in self.fcs:
            fx, fy, fz = f.center()
            n = (fx -x -norm[0], fy-y -norm[1], fz-z -norm[2]) #FIGURE THIS OUT
            f.rotate(a, dim, n)
            
    def shift(self, vect):
        #shifts all faces
        for f in self.fcs:
            f.shift(vect)
    def map(self, m, norm = (0,0,0)):
        #maps all faces through linear transformation
        x, y, z = self.center()
        for f in self.fcs:
            fx, fy, fz = f.center()
            n = (fx -x -norm[0], fy-y -norm[1], fz-z -norm[2]) #FIGURE THIS OUT
            f.map(m, n)
            
            
    def copy(self):
        newShp = Shape([], self.T, self.Wireframe)
        for f in self.fcs:
            newShp.fcs.append(f.copy())
        return newShp
    def show_rot(self, steps, a, dim:str, norm = (0, 0, 0)):
        a /= steps
    
        for i in range(steps):
            self.rotate(a, dim, norm)
            self.show()
    def show_shift(self, steps, vect):
        newvect = (vect[0]/steps, vect[1]/steps, vect[2]/steps)
        for i in range(steps):
            self.shift(newvect)
            self.show()
    def show_map(self, steps, m, norm = (0,0,0)):
        #slides all faces to a new place after a mapping
        dest = self.copy()
        size = len(self.fcs)
        dest.map(m, norm)
        diffs = []
        
        for fc in range(size):
            orig_fc = self.fcs[fc]
            dest_fc = dest.fcs[fc]
            dif = []
            for pt in range(len(orig_fc.pts)):
                dif.append([(dest_fc.pts[pt][0]-orig_fc.pts[pt][0])/steps,
                            (dest_fc.pts[pt][1]-orig_fc.pts[pt][1])/steps,
                            (dest_fc.pts[pt][2]-orig_fc.pts[pt][2])/steps])
            diffs.append(dif.copy())
        allfcs = [] #refs to all points for ordered iteration - this way sortfaces() can be called.
        j = 0
        for fc in self.fcs:
            allfcs.append([])
            for pt in fc.pts:
                allfcs[j].append(pt)
            j += 1
        
        for i in range(steps):
            for fc in range(size):
                a_fc = allfcs[fc]
                for pt in range(len(a_fc)):
                    a_fc[pt][0] += diffs[fc][pt][0]
                    a_fc[pt][1] += diffs[fc][pt][1]
                    a_fc[pt][2] += diffs[fc][pt][2]
            self.show()
        
        
if __name__ == "__main__":  #display some stuff for demo purposes
    testM = [[1, 0, 0],
             [0, -1, 0],
             [0, 0, -1]]
    x = 50
    fcs = []
    for i in range(80):
        fcs.append(Face([[randint(-x, x), randint(-x, x), randint(1, 2*x)] for i in range(1)]))
    for i in range(1):
        fcs.append(Face([[randint(-x, x), randint(-x, x), randint(1, 2*x)] for i in range(3)]))
    shp = Shape(fcs, T)
    shp.show_shift(10, (0, 0, 90))

    for i in range(3):
        shp.show_shift(100, (-20, 0, 20))
        shp.show_rot(100, 320, "x")
        shp.show_rot(100, 320, "z")
        shp.show_rot(100, 320, "y")
        shp.show_map(100, testM)

