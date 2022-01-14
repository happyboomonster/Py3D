#program which creates a 3D model in a Pickle dump.
import pickle

#*********IMPORTANT******#
PYTHON2 = True

#we need to define "raw_input" if we are on python 3
if(PYTHON2 != True):
    def raw_input(string):
        return input(string)

#our list holding our model data
model = []

#all the colors available for use
colors = ["red","blue","green","yellow","orange","brown","black","pink"]
matchingvalues = [[255,0,0],[0,0,255],[0,255,0],[255,255,0],[255,200,0],[100,100,0],[50,40,0],[0,0,0],[255,0,255]]

#we don't want to get out of here this fast, do we?
Exit = False

#flag which is set temporarily when removing something from a OBJ
remove = False

#flag for setting when we're going to edit the points of a triangle rather than append more points to the end of the OBJ
EditPoints = False

#do we want to import a model, or make a new one?
if(PYTHON2):
    importq = raw_input("Do you want to import a model, or start a new one? Any answer other than 'NEW' will be taken as a filename for an Object: ")
    if(importq == "NEW"): #continue with an empty model[] list
        pass
    else:
        try:
            infile = open(importq,"r+")
            model = pickle.load(infile)
        except IOError:
            print("***ERROR*** - You didn't provide a proper filename. Exiting...")
            Exit = True
else:
    pass

#main modelmaking loop
while not Exit:
    if(PYTHON2):
        #get a color value or an EXIT command.
        while True:
            color = raw_input("Give me a color out of these options or type EXIT to finish, REMOVE/EDIT to manipulate a triangle: " + str(colors) + " : ")
            if(color == "EXIT"): #do we want to leave?
                #get a filename and dump stuff there...
                filename = raw_input("Filename? ")
                mifile = open(filename,"w+")
                pickle.dump(model,mifile)
                mifile.flush()
                Exit = True #then exit from loop...
                break
            elif(color == 'REMOVE'): #we want to remove a part of our object?
                remove = True
                print("Here's your 3D object:")
                for x in range(0,len(model)):
                    print(str(model[x]) + ",")
                removal = raw_input("Which index do you want to remove? ")
                try: #make sure we got an integer, or a float which can be truncated
                    int(removal)
                except:
                    print("***ERROR*** - You didn't give an integer value. That's what I need.")
                    continue
                try: #did we give a valid index?
                    model.pop(int(removal))
                except IndexError:
                    print("***ERROR*** - You didn't give a valid index value. Cancelled...")
                continue
            elif(color == "EDIT"): #allow someone to change color/coords of a point
                print("Here's your 3D object:")
                for x in range(0,len(model)):
                    print(str(model[x]) + ",")
                edit = raw_input("Which index do you want to edit? ")
                print("Here's the triangle you picked: " + str(model[int(edit)]))
                edittype = raw_input("What modification do you want to make? Remake 'points', or change 'color'? ")
                if(edittype == 'points'): #now we break from the loop to get coordinates using the below method, but instead insert them back into the triangle
                    EditPoints = True     #that we're editing.
                    break
                else: #we're modifyin' the color
                    newcolor = raw_input("Please specify the new color: " + str(colors) + " ")
                    if(newcolor not in colors):
                        print("***ERROR*** - Invalid color...Try again.")
                        continue
                    else:
                        model[int(edit)][0] = matchingvalues[colors.index(newcolor)][:]
                    continue
            if(color not in colors): #deal with our color input...
                print("***ERROR*** - Invalid color...Try again.")
                continue
            actualcolor = matchingvalues[colors.index(color)]
            break
        #get a triangle to map the color to...
        triangle = [] #temporary list which stores one triangle's points before getting appended to the main model[] list
        while not Exit and not remove:
            triangleA = raw_input("Please give triangle coords as positions from 0-255. (coordX-" + str(len(triangle)) + "): ")
            triangleB = raw_input("Please give triangle coords as positions from 0-255. (coordY-" + str(len(triangle)) + "): ")
            triangleC = raw_input("Please give triangle coords as positions from 0-255. (coordZ-" + str(len(triangle)) + "): ")
            try:
                apoint = [float(triangleA),float(triangleB),float(triangleC)]
                triangle.append(apoint)
            except TypeError:
                print("Something wasn't a number value. Please retry...")
                continue
            if(len(triangle) >= 3): #exit getting polygon coords once we've got enough points
                print("Successfully obtained triangle coordinates.")
                break
        if(remove == False and EditPoints == False):
            model.append([actualcolor,triangle])
        elif(EditPoints == True):
            model[int(edit)][1] = triangle[:]
        remove = False
        EditPoints = False
    else:
        pass
