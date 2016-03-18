#!/usr/bin/python

#this is the text parser for the astrobio experiment

text = open("acaba-jm.txt", "r")

out = open("out", "w")

temp = text.read(10)

out.write(temp)

text.close()
out.close()
