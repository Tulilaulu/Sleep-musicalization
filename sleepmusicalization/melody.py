"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Generates melodies, adjustements to the generation are done mostly in probabilities.py.
Commented lines are just debugs.
"""
from kunquat.editor.timestamp import Timestamp
import random
import voice
import music
import probabilities

lastInterval = 0

#does not care about the fitting of the theme into chords at the moment! It should be implemented or there should be a method for varying the theme.
def generateTheme(bar, length, scale, chords):#does not use all info at the moment
	global lastInterval
	theme = []
	space = length
	lastnote = 0
	note = 0
	while (space > 0):
		if (theme == []):
			rythm = 0
			lastnote = scale[0]
		else:
			rythm = probabilities.getRythm(space, theme[-1][0])
			lastnote = theme[-1][1]
		space = space - rythm
		while True:
			interval = probabilities.getInterval(lastInterval)
			note = lastnote + interval
			lastInterval = interval
			if (note%1200 in scale and note > -1000 and note < 3000):
				break
		theme.append([rythm, note])
		lastnote = note
	return theme

def generateMelody(bar, length, scale, chords, start = 0, theme = None):
	melody = voice.Voice(start)
	templength = 0
	beat = start #monesko isku menossa
	spaceInFrase = 0
	oddsAndEnds = 0
	length = length + beat
	#append theme to the start
#	print theme
	for note in theme: #theme syntax : [[rythm, note],[rythm,note]]
#		print "beat: "+str(beat)
		if (length > beat):
			melody.nextRythm(note[0])
			melody.nextNote(note[1])
			beat = beat + note[0]#Tee tahan esim. transponointi sointuihin.
#			print note
		else:
			break
	while (length > beat): 
		frase = nextFrase(bar)
#		print "frase first: "+str(frase)
#		print "length-beat: "+str(length-beat)
		if (frase > (length-beat)):
			frase = length - beat
		spaceInFrase = frase
#		print "frase: "+str(frase)
		while (spaceInFrase > 0): #one frase at a time
			templength = probabilities.getRythm(spaceInFrase, melody.getLastRythm())#, music.IHRatTheMoment(beat))
			spaceInFrase = spaceInFrase - templength
			melody.nextRythm(templength)
			melody.nextNote(getNextNote(melody, beat, scale, chords, bar))
			if (beat%bar == 0):
				force = 4
			else:
				force = 0
			melody.forceEvent(music.getForce(force, beat))
			#beats must be counted in ints, because you can't use a float as the index of chords[]
			if (templength == int(templength)): 
				beat = beat + templength
			else:
				oddsAndEnds = oddsAndEnds + templength
				beat = beat + int(oddsAndEnds)
				oddsAndEnds = oddsAndEnds - int(oddsAndEnds)#remember the remainder of the beat, so we don't mess up calculations
	return melody.getMusic()


def getNextNote(melody, beat, scale, chords, bar): #gives a note
	global lastInterval
	beat = int(beat)#just making sure there is not a value like 3.0
	if (melody.getLastNote() == None):
		return scale[chords[beat/bar]]
	else:
		while True: #remove this, and you will get worse dissonances
			interval = probabilities.getInterval(lastInterval)
			note = melody.getLastNote() + interval
			lastInterval = interval
			if (beat/bar < len(chords)):
				difference = abs(note-scale[chords[beat/bar]])
			else:	
				difference = 0 #this is just stupid, but is not used anymore
			if (note%1200 in scale and note > -1000 and note < 3000 and difference != 100 and difference != 200 and difference != 600 and difference != 1100):
				return note

def nextFrase(bar):
	lengths = {
	0 : 4,
	1 : 6,
	2 : 8,
	3 : 8,
	4 : 8,
	5 : 10,
	6 : 12,
	7 : 16,
	}	
	i = random.randrange(0, 8)
	return lengths[i]*bar

