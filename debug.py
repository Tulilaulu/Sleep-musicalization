"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Prints a lot of stuff about the data and the generation results. Used for debugging. 
"""
import reader
import music
import generateKunquat

#def debugRythm(music):
#	for voice in music.music:
#		for note in voice:
#			#print note[0] TODO

def debugprint(music):
	print ""
	print "DEGUB PRINTS: "
	print ""
	print "Actigram (ticks per beat -version):"
	print reader.actigram
	print ""
	print "Respiration: "+str(reader.respiration)
	print "Data in respiration that is not < 0.5 long..:"
	for a in range(len(reader.respiration)):
		if (a != len(reader.respiration)-1 and reader.respiration[a+1][0] - reader.respiration[a][0] > 0.5):
			print reader.respiration[a]
	print ""
	print "Respiration length: "+str(len(reader.respiration))
	print ""
	print "IHR: "+str(reader.IHR)
	print "Data in IHR that is not < 0.5 long..:"
	for a in range(len(reader.IHR)):
		if (a != len(reader.IHR)-1 and reader.IHR[a+1][0] - reader.IHR[a][0] > 0.5):
			print reader.IHR[a]
	print ""
	print "IHR length: "+str(len(reader.IHR))
	print ""
	print "Chords: "+str(music.chorddata)
	print "Number of chords: "+str(len(music.chorddata))
	print ""
	print "Scale type: "+music.scaletype
	print ""
	print "Start: "+str(reader.getStart())
	print "End: "+str(reader.getEnd())
	print "Difference: "+str(reader.getEnd() - reader.getStart())
	print ""
	length = 0
	stages = reader.getStages()
	for a in stages:
		length= length + a[1]
	print "Sleep stages (prosessed): "+str(stages)
	print "Combined length of stages: "+str(length)
	print ""
	print "Night Length: "+str(reader.getNightLength())+" beats"
	print "Really its "+str(reader.getNightLength()-reader.getNightLength()%music.bar)
	print ""
	print "A bar is "+str(music.bar)+" beats"
	print ""
	for i in range(music.howManyVoices()):
		voice = music.getVoice(i)
		print "Last events for voice "+str(i)+":  "+str(voice[-3])+str(voice[-2])+str(voice[-1])
		print ""
