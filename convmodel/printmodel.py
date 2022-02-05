#simple script which prints the contents of a pickle file
import pickle

filename = raw_input("Filename? ")

mifile = open(filename,"r")

print(pickle.load(mifile))

mifile.close()
