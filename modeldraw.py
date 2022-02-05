import pickle
import pygame
import time
import math

screensize = [256,256]

VanishingPoint = 0.001 #changes the distance of the vanishing point
#function to produce a proper triangle coordinate set for pygame
def maketriangle(points):
    global VanishingPoint
    global screensize
    newpoints = []
    for point in points:
        tmppoint = []
        tmppoint.append(point[0])
        tmppoint.append(point[1])
        tmppoint[0] -= (tmppoint[0] - (screensize[0] / 2.0)) * point[2] * VanishingPoint
        tmppoint[1] -= (tmppoint[1] - (screensize[1] / 2.0)) * point[2] * VanishingPoint
        tmppoint[0] = int(tmppoint[0])
        tmppoint[1] = int(tmppoint[1])
        newpoints.append(tmppoint[:])
    return newpoints[:]

def sorttriangles(triangles): #sorts all the individual triangle points from farthest to closest
    newtriangles = [] #new obj list for the sorted triangle points
    for itertriangle in range(0,len(triangles)):
        newtriangle = []
        triangle = triangles[itertriangle][1][:]
        while len(triangle) > 0: #make sure we get all the triangle points
            largest = 0 #variables to record which index point is the largest, and its value
            index = 0
            for points in range(0,len(triangle)):
                if(triangle[points][2] >= largest): #once we've found the largest one...
                    largest = triangle[points][2]
                    index = points
            newtriangle.append(triangle[index]) #add the farthest point to the triangle buffer
            del(triangle[index]) #then delete the point in the old triangle buffer
        newtriangles.append([triangles[itertriangle][0][:],newtriangle[:]]) #add the sorted triangle into a new OBJ list
    return newtriangles

def sortobj(triangles): #sorts the triangles themselves from farthest from the camera to closest
    newtriangles = []
    while len(triangles) > 0:
        largest = 0 #variables to keep track of the largest point value and index in "triangles"
        index = 0
        for triangle in range(0,len(triangles)):
            if(triangles[triangle][1][0][2] > largest):
                index = triangle
                largest = triangles[triangle][1][0][2]
            elif(triangles[triangle][1][0][2] == largest): #now we check, is a secondary point still farther out than another triangles'?
                if(len(triangles[triangle][1]) >= len(triangles[index][1])): #now since we might be comparing a square and a triangle, we need to compare points based on which has fewer.
                   for compare in range(0,len(triangles[index][1])):
                       if(triangles[triangle][1][compare][2] < triangles[index][1][compare][2]):
                           break
                       elif(triangles[triangle][1][compare][2] > triangles[index][1][compare][2]): #if a secondary or third point is still larger than the competitor's equivalent...
                            largest = triangles[triangle][1][0][2]
                            index = triangle
                else:
                    for compare in range(0,len(triangles[triangle][1])):
                        if(triangles[triangle][1][compare][2] < triangles[index][1][compare][2]):
                           break
                        elif(triangles[triangle][1][compare][2] > triangles[index][1][compare][2]): #if a secondary or third point is still larger than the competitor's equivalent...
                            largest = triangles[triangle][1][0][2]
                            index = triangle
        newtriangles.append(triangles[index][:])
        del(triangles[index])
    return  newtriangles[:]

#rotates a two-dimensional point
def rotatepoint(point,rotate):
    while rotate < 0: #make it so we aren't rotating something nuts like 10443 degrees and our rotations are always positive
        rotate += 360
    while rotate >= 360:
        rotate -= 360
    
    length = math.sqrt(abs(point[1] * 1.0 * point[1]) + abs(point[0] * 1.0 * point[0])) #use pythagorean theorem to get the "length" of the polar coord

    if(point[1] > 0): #above center
        if(point[0] > 0): #right of center
            rotated = abs(math.atan(point[1] / (point[0] * 1.0))) + math.radians(rotate)
        else: #left of center
            rotated = abs(math.atan((point[0] * 1.0) / point[1])) + math.radians(rotate + 90)
    else: #below center / streight center
        if(point[0] > 0): #right of center
            if(point[1] != 0): #need to avoid nasty 0div errors...
                rotated = abs(math.atan((point[0] * 1.0) / point[1])) + math.radians(rotate + 270)
            else:
                rotated = math.radians(rotate)
        else: #left of center / streight center
            if(point[0] != 0): #need to avoid nasty 0div errors...
                rotated = abs(math.atan(point[1] / (point[0] * 1.0))) + math.radians(rotate + 180)
            else:
                rotated = math.radians(rotate + 270)

    point[0] = math.cos(rotated) * length
    point[1] = math.sin(rotated) * length

    return point[:]

##x = /\
##      \/
##y = |
##      |
##z = --
def rotatetriangle(points,rotate,center): #rotates a triangle's points via Sin Cos & Tan functions
    for iterpoints in range(0,len(points)): #we have to make these so the "center" offset takes effect
        points[iterpoints][0] -= center[0]
        points[iterpoints][1] -= center[1]
        points[iterpoints][2] -= center[2]
    for iterpoints in range(0,len(points)): #iterate through all points in triangle - one thing to remember is that the Y axis is inverted in trigonometry equations...
        #start by getting a single dimension's points in polar coorinates.
        #**** X AXIS **** (circle from 2d perspective)
        tmppoint = rotatepoint([points[iterpoints][0],points[iterpoints][2]],rotate[0]) #rotate the point
        points[iterpoints][0] = tmppoint[0] #store the results
        points[iterpoints][2] = tmppoint[1]
                    
        #**** Y AXIS **** (vertical line from 2d perspective)
        tmppoint = rotatepoint([points[iterpoints][2],points[iterpoints][1]],rotate[1]) #rotate the point
        points[iterpoints][2] = tmppoint[0] #store the results
        points[iterpoints][1] = tmppoint[1]

        #****Z AXIS**** (horizontal line from 2d perspective)
        tmppoint = rotatepoint([points[iterpoints][0],points[iterpoints][1]],rotate[2]) #rotate the point
        points[iterpoints][0] = tmppoint[0] #store the results
        points[iterpoints][1] = tmppoint[1]
        
    for iterpoints in range(0,len(points)): #undo the center offset once we're done with this stuff
        points[iterpoints][0] += center[0]
        points[iterpoints][1] += center[1]
        points[iterpoints][2] += center[2]
    #return the triangle once we're DONE WITH IT
    return points[:]

def drawmodel(model,pos):
    for triangles in range(0,len(model)):
        tmptriangle = model[triangles][1]
        for translate in range(0,len(tmptriangle)):
            tmptriangle[translate][0] += pos[0]
            tmptriangle[translate][1] += pos[1]
            tmptriangle[translate][2] += pos[2]
        pygame.draw.polygon(screen,model[triangles][0],maketriangle(model[triangles][1]))

#we get a filename of a model
filename = input("Give me a object's filename: ")
try:
    mifile = open(filename,"rb")
except IOError:
    print("This isn't a valid filename. Exiting...")
    raise IOError
obj = pickle.load(mifile)

#get an offset point for rotation
rotateoffset = eval(input("Please give an XYZ rotation offset as a 3 item list: "))

#create a screen object
screen = pygame.display.set_mode([256,256], pygame.RESIZABLE)

#clock our FPS
clock = pygame.time.Clock()

#a translation position for an object
pos = [0,0,0]
rotate = [0,0,0]

#get a key repeat turned on for easy GUI setup
pygame.key.set_repeat(200,10)

#mouse grab goes brrrr
#pygame.event.set_grab(True)

while True:
    screen.fill([0,0,0]) #fill the screen with black to start

    newobj = eval(str(obj)) #create a fresh manipulable copy of our object
    
    for triangles in range(0,len(newobj)): #iterate through all triangles in the obj and manipulate them
        newobj[triangles][1] = rotatetriangle(newobj[triangles][1],rotate,rotateoffset)
    newobj = sortobj(sorttriangles(newobj)) #sort the object's triangles
    drawmodel(newobj,pos)
    pygame.display.flip()

    #get our FPS
    clock.tick(120)
    pygame.display.set_caption(str(int(clock.get_fps())))

    #get our screen height/width
    screensize[0] = screen.get_width()
    screensize[1] = screen.get_height()

    #event loop
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
        if(event.type == pygame.MOUSEMOTION):
            tmprotate = pygame.mouse.get_rel()
            rotate[0] += tmprotate[0]
            rotate[1] += -tmprotate[1]
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_DOWN):
                rotate[1] -= 1
            elif(event.key == pygame.K_UP):
                rotate[1] += 1
            elif(event.key == pygame.K_RIGHT):
                rotate[0] += 1
            elif(event.key == pygame.K_LEFT):
                rotate[0] -= 1
            elif(event.key == pygame.K_LSHIFT):
                pos[2] += -3
            elif(event.key == pygame.K_SPACE):
                pos[2] += +3
            elif(event.key == pygame.K_a):
                pos[0] += -3
            elif(event.key == pygame.K_d):
                pos[0] += +3
            elif(event.key == pygame.K_w):
                pos[1] += -3
            elif(event.key == pygame.K_s):
                pos[1] += +3

time.sleep(1)
pygame.quit()
