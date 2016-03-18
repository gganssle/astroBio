#!/usr/bin/python

#this is the text parser for the astrobio experiment

import string

textFile = open("raw/acaba-jm.txt", "r")
out = open("out", "w")

temp = textFile.read()

#find ages
born = temp.find('Born in')
if born == -1:
	born = temp.find('born in')
if born == -1:
	print "cant find birthdate \n"
print 'born position is {}'.format(born)



#out.write(temp)

textFile.close()
out.close()
