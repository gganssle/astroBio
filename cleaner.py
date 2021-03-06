#!/usr/bin/python

#this is the text parser for the astrobio experiment

import string
import nltk

#count and store names
nameFile = open("dat/astroNamesNormalized.dat","r")
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
wings = []
hobb = [0] * count
exp = [0] * count

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
'Hindi','Arabic','Portuguese','Bengali','Javanese','Dutch','ASL']
	per = raw[raw.find('PERSONAL DATA') : raw.find('EDUCATION')]

	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			if lang[i] == 0 :
				lang[i] = di[j]
			else :
				lang[i] = ' '.join((lang[i],di[j]))
	
	#military rank and affiliation
	di = ['ENSIGN','SECOND LIEUTENANT','FIRST LIEUTENANT','LIEUTENANT',
'LIEUTENANT COMMANDER','COMMANDER','CAPTAIN','MAJOR','LIEUTENANT COLONEL','LT. COL',
'COLONEL','COL','GENERAL','ADMIRAL']
	per = raw[0 : raw.find('PERSONAL')]

	rank.append('0')
	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			rank[i] = di[j].lower()
			break

	di = ['USAF','USN','USA','USCG','U.S.N','U.S.A','U.S.A.F','U. S. NAVY', 'U.S. ARMY','U.S. MARINE CORPS','U.S. NAVY','U.S. AIR FORCE','U. S. AIR FORCE','U. S. ARMY']
	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			rank[i] = ' '.join((rank[i],di[j]))
			break

	temp = rank[i].split()
	if rank[i].find('AIR') != -1 :
		rank[i] = ' '.join((temp[0], 'USAF'))
	if rank[i].find('MARINE') != -1 :
		rank[i] = ' '.join((temp[0], 'USMC'))
	if rank[i].find('NAVY') != -1 :
		rank[i] = ' '.join((temp[0], 'USN'))
	if rank[i].find('ARMY') != -1 :
		rank[i] = ' '.join((temp[0], 'USA'))
	temp = rank[i].split()
	if rank[i].find('col') != -1 :
		rank[i] = ' '.join(('colonel', temp[1]))
	if rank[i].find('lt.') != -1 :
		rank[i] = ' '.join(('lt.col', temp[1]))

	#Did Red Bull give you wings?
	if raw.find('ilot') != -1 :
		wings.append(1)
	else :
		wings.append(0)
	
	#hobbies and interests
	di = ['camping', 'hiking', 'biking', 'kayak', 'scuba','running',
'fishing', 'reading', 'bicycling', 'ornithology', 'paleontology', 'guitar','basketball', 'softball',
'martial arts', 'cricket', 'jet skiing','writing', 'sailing', 'boat restoration','travel','music',
'photography','weight training', 'sports', 'motorcycl', 'family','church','skiing','astronomy','auto repair',
'auto restoration','geology','languages','backpacking','flying','exercise','hockey','football', 'hunting',
 'cycling','NASCAR',' baseball', 'golf','weightlifting','climbing', 'paddling','yoga','swimming','movies',
 'snowboarding','cooking','rugby','soccer','history','sewing', 'drawing','painting','piano','windsurfing',
 'woodworking','music','stamp collecting']
	per = raw[raw.find('PERSONAL DATA') : raw.find('EDUCATION')]

	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			if hobb[i] == 0 :
				hobb[i] = di[j]
			else :
				hobb[i] = ', '.join((hobb[i],di[j]))
				
	#professional experience
	di = ['marine corps, reserves','geologist','peace corps','manager','taught','oceanographic technician',
	'teacher','faculty','marine sciences','flight surgeon','physician','editor','test pilot',
	'flight test engineer','combat ready pilot','flight commander','engineering officer','executive officer',
	'project officer','flight instructor','aircraft commander','aeronautical engineering officer',
	'naval aviator','instructor pilot','founded','navy seal','operations officer','electrician','reasearch',
	'author','technical specialist','technical intelligence officer','auto mechanic','glazier','geophysicist',
	'space systems engineer','space test engineer','flight test liaison','operational pilot','project pilot',
	'air command','flight test engineer','flight test manager','exchange pilot','instructed','army aviator',
	'assistant professor','field engineer','electrical engineer','platoon leader','jumpmaster','crew surgeon',
	'emergency physician','chief scientist','helicopter pilot','staff scientist','technical staff',
	'combat engineer','crew commander','flight controller','operations engineer','dynamics engineer',
	'supervisor','diving officer','safety officer','principal investigator']
	trans = ['millitary reserves','geologist','peace corps','manager','teacher','oceanographic technician',
	'teacher','professor','marine scientist','flight surgeon','physician','editor','test pilot',
	'flight test engineer','combat ready pilot','flight commander','engineering officer','executive officer',
	'project officer','flight instructor','aircraft commander','aeronautical engineering officer',
	'naval aviator','instructor pilot','company founder','navy seal','operations officer','electrician',
	'reasearcher','author','technical specialist','technical intelligence officer','auto mechanic','glazier',
	'geophysicist','space systems engineer','space test engineer','flight test liaison','operational pilot',
	'project pilot','air command','flight test engineer','flight test manager','exchange pilot','instructor',
	'army aviator','assistant professor','field engineer','electrical engineer','platoon leader','jumpmaster',
	'crew surgeon','emergency physician','chief scientist','helicopter pilot','staff scientist','technical staff',
	'combat engineer','crew commander','flight controller','operations engineer','dynamics engineer','supervisor',
	'diving officer','safety officer','principle investigator']
	per = raw[raw.find('EXPERIENCE:') : raw.find('NASA EXPERIENCE:')].lower()
	
	for j in range(len(di)) :
		if per.find(di[j]) != -1 :
			if exp[i] == 0 :
				exp[i] = trans[j]
			else :
				exp[i] = ', '.join((exp[i],trans[j]))
	
	#clean up
	textFile.close()

#fix inconsistencies
born[16] = 1957
born[44] = 1965
wings[41] = 0
lang[11] = 'ASL Russian'
exp[32] = 'researcher'

#print for QC
for i in range(47) :
	if i == 5 :
		print i, '\t', names[i], '\t', '\t', exp[i]
	else :
		print i, '\t', names[i], '\t', exp[i]


#for i in range(count) :
#	if ((wings[i] == 1) & (rank[i] == "0")) :
#		print i, '\t', names[i]


#write out
out = open("dat/born", "w")
for i in range(count) :
	temp = ''.join((str(born[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/married", "w")
for i in range(count) :
	temp = ''.join((str(marry[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/married", "w")
for i in range(count) :
	temp = ''.join((str(marry[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/education", "w")
for i in range(count) :
	temp = ''.join((str(edu[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/eduSpec", "w")
for i in range(count) :
	temp = ''.join((str(eduSpec[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/children", "w")
for i in range(count) :
	temp = ''.join((str(kids[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/languages", "w")
for i in range(count) :
	temp = ''.join((str(lang[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/millitary", "w")
for i in range(count) :
	temp = ''.join((str(rank[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/pilot", "w")
for i in range(count) :
	temp = ''.join((str(wings[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/interests", "w")
for i in range(count) :
	temp = ''.join((str(hobb[i]), '\n'))
	out.write(temp)
out.close()

out = open("dat/experience", "w")
for i in range(count) :
	temp = ''.join((str(exp[i]), '\n'))
	out.write(temp)
out.close()





