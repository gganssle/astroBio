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
eduSpec = [[0] * 4 for i in range(count)]
kids = [[0] * 3 for i in range(count)]
lang = [0] * count
rank = []

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
#		print "there is no birthdate for", names[i]
		born.append(0)
	if temp != -1 :
		temp2 = raw[temp:temp+40].find(' 19')
		if temp2 == -1 :
			born.append(0)
#			print "cant find birthdate for", names[i]
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
	per = raw[raw.find('EDUCATION') : ]

	words = ['b.s','B.S','bachelor','Bachelor']
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 1
			break
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 :
			temp = per[temp : temp + 80].split()
			temp2 = 0
			for k in range(len(temp)) :
				if temp[k] == 'in' :
					temp2 = k
					break
			eduSpec[i][0] = ''.join((temp[temp2+1],' ',temp[temp2+2]))

	words = ['m.s','M.S','master','Master']
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 10
			break
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 :
			temp = per[temp : temp + 80].split()
			temp2 = 0
			for k in range(len(temp)) :
				if temp[k] == 'in' :
					temp2 = k
					break
			eduSpec[i][1] = ''.join((temp[temp2+1],' ',temp[temp2+2]))

	words = ['m.d','M.D','MD']
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 100
			break
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 :
			temp = per[temp : temp + 80].split()
			temp2 = 0
			for k in range(len(temp)) :
				if temp[k] == 'in' :
					temp2 = k
					break
			eduSpec[i][2] = ''.join((temp[temp2+1],' ',temp[temp2+2]))

	words = ['phd','ph.d','Ph.D','PH.D','PHD']
	for j in range(len(words)) :
		temp = raw.find(words[j])
		if temp >= 0 : 
			edu[i] += 1000
			break
	words = ['phd','ph.d','Ph.D','PH.D','PHD','octorate']
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 :
			temp = per[temp : temp + 80].split()
			temp2 = 0
			for k in range(len(temp)) :
				if temp[k] == 'in' :
					temp2 = k
					break
			eduSpec[i][3] = ''.join((temp[temp2+1],' ',temp[temp2+2]))

	#how many kids? column 1 is daughters, second = sons, 3rd = unknown gender
	per = raw[raw.find('PERSONAL DATA') : raw.find('EDUCATION')]
	num = ['two','three','four','five','six','seven','eight','nine']

	words = ['daughter','Daughter']
	temp = 0
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 : 
			temp2 = per[temp - 10 : temp].split()
			kids[i][0] = 1
			for k in range(len(num)) :
				if (num[k] in temp2) :
					kids[i][0] = k + 2
			break

	words = ['son','Son']
	temp = 0
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 : 
			temp2 = per[temp - 10 : temp].split()
			kids[i][1] = 1
			for k in range(len(num)) :
				if (num[k] in temp2) :
					kids[i][1] = k + 2
			break

	words = ['Kid','kid','Child','child']
	temp = 0
	for j in range(len(words)) :
		temp = per.find(words[j])
		if temp >= 0 : 
			temp2 = per[temp - 10 : temp].split()
			for k in range(len(num)) :
				if (num[k] in temp2) :
					kids[i][2] = k + 2
			break
	
	#Que idiomas (otra que ingles) habla usted?
	di = ['Swedish','Russian','Spanish','French','Italian','Japanese','German','Mandarin',
'Hindi','Arabic','Portuguese','Bengali','Javanese','Dutch']
	per = raw[raw.find('PERSONAL DATA') : raw.find('EDUCATION')]

	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			if lang[i] == 0 :
				lang[i] = di[j]
			else :
				lang[i] = ' '.join((lang[i],di[j]))
	
	#military rank and affiliation
	di = ['ENSIGN','SECOND LIEUTENANT','FIRST LIEUTENANT','LIEUTENANT',
'LIEUTENANT COMMANDER','COMMANDER','CAPTAIN','MAJOR','LIEUTENANT COLONEL','LT. COL.',
'COLONEL','COL','GENERAL','ADMIRAL']
	per = raw[0 : raw.find('PERSONAL')]

	rank.append('0')
	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			rank[i] = di[j].lower()
			break

	di = ['USAF','USN','USA','USCG','U.S.N','U.S.A','U.S.A.F','U. S. NAVY', 'U.S. ARMY','U.S. MARINE CORPS','U.S. NAVY','U.S. AIR FORCE','U. S. ARMY']
	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			rank [i] = ' '.join((rank[i],di[j]))
			break

	#clean up
	textFile.close()

#fix inconsistencies
born[16] = 1957
born[44] = 1965

#print for QC
for i in range(47) :
	if i == 5 :
		print i, '\t', names[i], '\t', '\t', rank[i]
	else :
		print i, '\t', names[i], '\t', rank[i]

#write out
#out = open("bday", "w")
#for i in range(count) :
#	temp = ''.join((str(born[i]), '\n'))
#	out.write(temp)
#out.close()








