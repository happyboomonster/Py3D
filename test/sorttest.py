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

#tested: works with other polygons other than triangles too!
obj = [['color',[[4,2,3],[3,2,4],[3,4,3]]],['color',[[4,2,3],[3,2,4],[3,4,2]]],['color',[[4,2,4],[3,2,3],[3,4,3]]]]

#result is that the point with the farthest Z value comes first.
print(sorttriangles(obj))
print("\n\n\n")
#result is that the triangle with the farthest Z value comes first.
print(sortobj(sorttriangles(obj)))
