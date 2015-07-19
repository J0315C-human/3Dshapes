#Shape templates/creators
from baseclasses import *



def Recolor(Shp, color=None, gap = 20):
    #re-randomizes all face colors,
    #if color given - uses colors within 'gap' range of RGB values
    if color != None:
        for i in (0, 1, 2): #account for out of range RGBs
            if color[i]<gap:
                color[i] = gap
            elif color[i]>(255-gap):
                color[i] = (255-gap)
        r, g, b = color
        for f in Shp.fcs:
            f.color = (randint(r - gap, r+gap),
                       randint(g - gap, g+gap),
                       randint(b - gap, b+gap))
    else:
        for f in Shp.fcs:
            f.color = (randint(0, 255),
                      randint(0, 255),
                      randint(0, 255))

def Cube(vect, size, color = None, gap = 20):
    #a cube with a center at vect
    #gap is divergence width for color
    x, y, z = vect
    front = Face([[x, y, z],
                 [x + size, y, z],
                 [x + size, y + size, z],
                 [x, y+ size, z]])
    h = size/2
    front.shift((-h, -h, -h))
    back = front.copy()
    back.shift((0, 0, size))

    fb = Shape([front, back])
    rl = fb.copy()
    rl.rotate(90, "y")
    tb = fb.copy()
    tb.rotate(90, "x")
    fb.add(rl)
    fb.add(tb)
    Recolor(fb, color, gap)
   
    return fb


def CubeField(vec, size, num, space =None, color = None, gap =20):
    #cubic field of cubes
    #VEC is the original location of the center of the cube
    if not space:
        space = size*2

    ret = Shape()
    #full width is (num-1)*space + size
    shift = ((num-1)*space + size)/2
    vect = []
    for i in vec:
        vect.append(i - shift)
        
    for i in range(num):
        x = vect[0] + i*space
        for j in range(num):
            y = vect[1] + j*space
            for k in range(num):
                z = vect[2] + k*space
                ret.add(Cube((x, y, z), size))
                

    Recolor(ret, color, gap)
    return ret

def PointField(vec, num, space = 20, color=None, gap=20):

    ret = Shape()
    shift = ((num-1)*space)/2
    vect = []
    for i in vec:
        vect.append(i - shift)
    for i in range(num):
        x = vect[0] + i*space
        for j in range(num):
            y = vect[1] + j*space
            for k in range(num):
                z = vect[2] + k*space
                ret.add(Face([[x, y, z]]))
    Recolor(ret, color, gap)
    return ret


Standard = (-10, 0, 150)

d = 50
b = -1
c = 1
K = PointField((0, 0, 50), 5, 10)



def main(): #display for demo
    Matrix = [[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]]

    K.show_rot(60, 90, "y")
    K.show_rot(60, 90, "x")
    K.show_rot(60, 90, "z")
    K.show_map(400, Matrix)
    K.show_rot(60, 90, "y")
    K.show_rot(60, 90, "x")
    K.show_rot(60, 90, "z")
    


if __name__ == "__main__":
    main()


    
