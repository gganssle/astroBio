#!/usr/bin/python

#this is the text parser for the astrobio experiment

import string
import nltk

#count and store names
nameFile = open("astroNamesNormalized.dat","r")
names = nameFile.read().splitlines()
count = len(names)
nameFile.close()

born = []
marry = []
edu = [0] * count

#iterate over all astros
for i in range(count) :

	#grab data from bio
	textFile = open(''.join(('raw/',names[i],'.txt')), "r")
	raw = textFile.read()
	
	#find ages
	temp = raw.find(' Born ')
	if temp == -1 :
		temp = raw.find(' born ')
	if temp == -1 :
		print "there is no birthdate for", names[i]
		born.append(0)
	if temp != -1 :
		temp2 = raw[temp:temp+40].find(' 19')
		if temp2 == -1 :
			born.append(0)
			print "cant find birthdate for", names[i]
		else :
			temp3 = raw[temp2+temp+1:temp+temp2+5]
			if (list(temp3)[2] in list(string.digits)) & (list(temp3)[3] in list(string.digits)) : #ensures this isn't grabbing the 19th day of the month
				temp3 = int(temp3)
				born.append(temp3)
			else :
				temp3 = raw[temp2+temp+1:temp2+temp+1+10].find(' 19')
				temp3 = int(raw[temp+temp2+temp3+1:temp+temp2+temp3+5])
				born.append(temp3)
	
	#determine marital status, 1 = married, 0 = not currently married
	words = ['married','Married','wife','Wife','husband','Husband']
	temp = 0
	for j in range(len(words)) :
		temp2 = raw.find(words[j])
		if temp2 >= 0 : 
			temp += 1
			break
	if temp > 0 :
		marry.append(1)
	else :
		marry.append(0)
	
	#educational status; 1 = bs, 10 = ms, 100 = md, 1000 = phd
	words = ['b.s','B.S','bachelors','bachelor','Bachelor','Bachelors']
	temp = 0
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 1
			break
	words = ['m.s','M.S','masters','Masters','master','Master']
	temp = 0
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 10
			break
	words = ['m.d','M.D','MD']
	temp = 0
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 100
			break
	words = ['phd','ph.d','Ph.D','PH.D','PHD']
	temp = 0
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 1000
			break

	#clean up
	textFile.close()

#fix inconsistencies
born[16] = 1957
born[44] = 1965

#print for QC
for i in range(47) :
	print i, names[i], edu[i]

#write out
#out = open("bday", "w")
#for i in range(count) :
#	temp = ''.join((str(born[i]), '\n'))
#	out.write(temp)
#out.close()








