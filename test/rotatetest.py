import pygame
import math

#point we're gonna rotate
point = [-200,0]

#set up pygame's screen
screen = pygame.display.set_mode([600,600])

def rotate_point(point,rotate):
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
    else: #below center
        if(point[0] > 0): #right of center
            if(point[1] != 0): #need to avoid nasty 0div errors...
                rotated = abs(math.atan((point[0] * 1.0) / point[1])) + math.radians(rotate + 270)
            else:
                rotated = math.radians(rotate)
        else: #left of center
            if(point[1] != 0): #need to avoid nasty 0div errors...
                rotated = abs(math.atan(point[1] / (point[0] * 1.0))) + math.radians(rotate + 180)
            else:
                rotated = math.radians(rotate + 180)

    point[0] = math.cos(rotated) * length
    point[1] = math.sin(rotated) * length

    return point[:]

#clock so I can see what i'm doing
clock = pygame.time.Clock()

rotate = 0 #rotation variable
while True:
    rotate += 2
    tmppoint = rotate_point(point[:],rotate)
    pygame.draw.circle(screen,[0,255,0],[int(tmppoint[0]) + 300, int(-tmppoint[1]) + 300],10)
    pygame.display.flip()
    screen.fill([0,0,0])

    clock.tick(120)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
