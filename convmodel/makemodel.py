#simple script which dumps the contents of your input into a pickle file
import pickle

filename = input("Filename? ")

mifile = open(filename, "wb")
obj = eval(input("OBJ dump? "))

pickle.dump(obj,mifile,protocol=2)

mifile.close()
