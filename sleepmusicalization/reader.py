"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Here are the functions for getting and processing the input data. Commented lines are mostly debug prints that can be uncommented if this start going wrong.
"""
import csv
import numpy
import datetime
import json
import time

#In order to get decent lenghts for music, I estimated that 120 seconds of sleep should equal 1 second of music.
#thus: 8h sleep = 4 min music, 6h sleep = 3 min music, 10h sleep = 5 min music
IHR = []
length = 0
stages = []
actigram = []
start = 0
starttime = None
end = 0
respiration = []
stages = [] #[[stage, lenght],[stage, lenght]]

def getStages():
	return stages

def getStart():
	return start

def getEnd():
	return end

def getSignalAnalysisResults(json_string):
	json_document = json.loads(json_string)
    
	respiration_data = json_document['respiration']
	ihr_data = json_document['ihr']
	actigram_data = json_document['binary_actigram']
	
	# Take the timestamp (index=0) and minimum-to-minimum cycle length (index=2)
	respiration_timestamps = [row[0] for row in respiration_data]
	respiration_cycle_lengths = [row[2] for row in respiration_data]
	
	ihr_timestamps = [row[0] for row in ihr_data]
	ihr_values = [row[1] for row in ihr_data]
	
	return respiration_timestamps, respiration_cycle_lengths, ihr_timestamps, ihr_values, actigram_data

def getSleepData(json_string):
	json_document = json.loads(json_string)
	sleepstages = json_document['sleep_stages']
	timestamps = [row[0] for row in sleepstages]
	stagelist = [row[1] for row in sleepstages]
	return timestamps, stagelist

def processIHR(timestamps, ihr_values):
	global start
	global end
	global IHR
	average = 0
	items = 0
#	smallest = 100000
#	biggest = 0
	startpoint = ihr_values[0] #average start
	startpointtime = timestamps[0] #average starttime
#	print len(timestamps)#debug
	for i in range(len(timestamps)):
#		if (ihr_values[i] > biggest): #debug
#			biggest = ihr_values[i]#debug
#		if (ihr_values[i] < smallest):#debug
#			smallest = ihr_values[i]#debug
		if (timestamps[i] > start and timestamps[i] < end): 
			if (abs(startpoint - ihr_values[i]) > 15 and items != 0):				
				IHR.append([(startpointtime-start)/120, average/items])
				startpoint = ihr_values[i]
				startpointtime = timestamps[i]
				average = ihr_values[i]
				items = 1
			else:
				items = items + 1
				average = average + ihr_values[i]
#			print timestamps[i]/120#debug
#			print ihr_values[i]#debug
#	print len(IHR)#debug
#	print smallest#debug
#	print biggest#debug
	for item in IHR:
#		item[1] = item[1] *2-50 #scale a bit old version
		item[1] = item[1]*4-180 #new version
		if (item[1] < 30):
			item[1] = 30
		if (item[1] > 150):
			item[1] = 150
	IHR[0][0] = 0
	return IHR

def processRespirationVariability(json_string):
	global respiration
	global start
	global end
	timestamps, cycle_lengths = getRespirationVariability(json_string)
	average = 0
	items = 0
	startpoint = cycle_lengths[0] #average start
	startpointtime = timestamps[0] #average starttime
#	biggest = 0
#	smallest = 200000
	for i in range(len(timestamps)):
		if (timestamps[i] > start and timestamps[i] < end): 
			if (abs(startpoint - cycle_lengths[i]) > 5 and items != 0):				
#				if (average/items > biggest):
#					biggest = average/items
#				if (average/items < smallest):
#					smallest = average/items
				respiration.append([(startpointtime-start)/120, average/items])
				startpoint = cycle_lengths[i]#start next
				startpointtime = timestamps[i] 
				average = cycle_lengths[i]
				items = 1
			else:
				items = items + 1
				average = average + cycle_lengths[i]
#	print biggest
#	print smallest
	respiration[0][0] = 0
	for item in respiration:#scale
#		item[1] = item[1]*10+9 #old version
		item[1] = (item[1]**3)*4-110#new version
	return respiration

def getRespirationVariability(json_string):
	json_document = json.loads(json_string)
	respiration_data = json_document['respiration']
	
	# Take the timestamp (index=0) and minimum-to-minimum cycle length (index=2)
	timestamps = [row[0] for row in respiration_data]
	respiration_cycle_lengths = [row[2] for row in respiration_data]
    
	return timestamps, respiration_cycle_lengths


#this is the version to be used when using actigram as a noise element
#def processActigram(actigram_times): #only after processSleepData has been called
#	global actigram
#	global start
#	global end
#	for value in actigram_times:
#		if (value > start and value < end):
#			actigram.append((value-start)/120)
#	return actigram

#this is the version to be used when using actigram for modulating
def processActigram(actigram_times): #only after processSleepData has been called
	global actigram
	global start
	global end
	beat = 0
	ticksperbeat = 0
	for value in actigram_times:
		if (value > start and value < end):
			realtime = (value-start)/120
			if (realtime - beat < 1):
				ticksperbeat = ticksperbeat + 1
			else:
				actigram.append([beat, ticksperbeat])
				beat = beat + 1
				ticksperbeat = 1
	return actigram

def getTempo():
	tempos = []
	return tempos

def getNightLength():
	return length

def processSleepData(json_string):
	timestamps, stagelist = getSleepData(json_string)
	global start
	global end 
	global length
	global starttime
	last = None
	lasttime = 0
	secondlast = None 
	secondlasttime = 0
	thistime = None
	setStartandEnd(timestamps, stagelist)	
	starttime = datetime.datetime.strptime(timestamps[0], "%Y-%m-%dT%H:%M:%S")
	for i in range (0, len(timestamps)): 
		thistime = toSeconds(timestamps[i])
		if (i == 2): #to insure that they get a value in the start
			secondlasttime = lasttime
			secondlast = last
		if (i > 2): #all variables dont have non-zero values before this point
			if (abs(thistime-lasttime) > 5):
				if (secondlast != 'A'):
					stages.append([secondlast, abs(lasttime-secondlasttime)])
				secondlast = last
				secondlasttime = lasttime
		lasttime = thistime
		last = stagelist[i]
	if (abs(lasttime-secondlasttime)>10): #secondlast datapoint
		stages.append([secondlast, abs(lasttime-secondlasttime)])
	else:
		stages[-1][1] = stages[-1][1]+abs(lasttime-secondlasttime)
	#last datapoint is assumed to be 'A'
	for a in range(0, len(stages)): #make stages int so generation will be easier
#		stages[a][1] = int(stages[a][1]) don't need this cause of the syncking 
		length = length+stages[a][1]
	length = int(length)
#		print length
#		print start
#		print end
	#120 seconds of sleep should equal about 1 second of music
	#later tempos should be taken into account here somehow (1s != 1beat :P)
	return length

def setStartandEnd(timestamps, stagelist):
	global start
	global end
	first = toUnixSeconds(timestamps[0])
	for i in range (0, len(timestamps)): #get start and endtimes counting from signal start
		time = toUnixSeconds(timestamps[i])
		if (stagelist[i] != 'A' and start==0):
			if (stagelist[i-1] == 'A'):
				start = time - first
		if (stagelist[i] == 'A' and i>3):
			end = toUnixSeconds(timestamps[i]) - toUnixSeconds(timestamps[0])

def toUnixSeconds(t):
	t = datetime.datetime(*time.strptime(t, "%Y-%m-%dT%H:%M:%S")[0:6])
	return time.mktime(t.timetuple())

def toSeconds(time):#converts times to second of music (seconds/120)
	time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
	time = (time-starttime).total_seconds()
	time = float(time)/120
	return time

def syncStages(tempos): #tempos will be trated as theyre timestamps are in second or otherwise this is not possible!
	global stages
	stagestart = 0
	index = 0
	leftovertime = 0
	
	def getTempo(i):
		i = min(len(tempos)-1, i)
		return tempos[i][1];
	
	for item in stages:
		stageLength = item[1]
		summa = 0
		
		while (summa < stageLength):
			if (leftovertime <= 0):
				if index+2 < len(tempos):
					tempoLength = tempos[index+1][0]-tempos[index][0]
				else:
					tempoLength = stageLength-summa
				if (stageLength-summa < tempoLength):
					leftovertime = tempoLength - (stageLength-summa)
					summa = summa + (((stageLength-summa)/60 ) * getTempo(index))
				else:
					summa = summa + ((tempoLength/60 ) * getTempo(index))
					index = index + 1	
					leftovertime = 0
			elif (index < len(tempos)): 
				if (stageLength-summa < leftovertime): #too much time in this tempo left over
					leftovertime = leftovertime - (item[1]-summa)
					summa = summa + (((stageLength-summa)/60) * getTempo(index))
				else: #all time used, none left over
					summa = summa + ((leftovertime/60 ) * getTempo(index))
					index = index + 1	
					leftovertime = 0	
#			print "leftovertime: "+str(leftovertime)
#			print "item: "+str(item)
#			print "summa: "+str(summa)
		item[1] = summa
		stagestart = stagestart + summa
#		print "Stagestart: "+str(stagestart)
	next = 0
	for a in range(len(tempos)-1):
		currentTime = tempos[a][0]		
		tempos[a][0] = next
		if (a > 0):
			tempos[a][0] = tempos[a][0] + tempos[a-1][0]
		next = ((tempos[a+1][0] - currentTime)/60) * tempos[a][1]
	tempos[len(tempos)-1][0] = next + tempos[len(tempos)-2][0]
	global length
	length = 0
	for item in stages:
		item[1] = int(round(item[1]))
		length = length + item[1]#compute length again cause it has changed:
#	for item in stages:
#		for a in range(len(tempos)):
#			if (a != 0 and tempos[a][0] > stagestart):
#				timedifference = tempos[a-1][0] - tempos[a][0]
#				tempodifference = tempos[a-1][1] - 60
#				percentage = abs(timedifference/item[1])
#				if (percentage > 1):
#					percentage = 1
#				item[1] = item[1] + (item[1] * (percentage * tempodifference))
#				print "Stagestart: "+str(stagestart)
#				print "timedifference: "+str(timedifference)
#				print "percentage: "+str(percentage)
#				print tempos[a]
#				print item
#			if (a < len(tempos)-1 and tempos[a+1][0] > stagestart+item[1]):
#				break
#		stagestart = stagestart + item[1]
	return stages
