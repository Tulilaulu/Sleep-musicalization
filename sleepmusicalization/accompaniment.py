"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

This file generates accompaniment for the melody in parts acording to the chords it is given. 
"""

from kunquat.editor.timestamp import Timestamp
import random
import voice
import music

#For Wake
def generateAccompaniment0(bar, length, scale, chords, starttime):
	accompaniment = voice.Voice(starttime)
	note = None
	beat = starttime
	starttime = int(starttime/bar) #because the chords are ordered by bar
	for i in range (starttime, starttime+int(length/bar)):#process one chord and bar at a time
		for j in range (0, bar*4):
			note = scale[chords[i]]
			accompaniment.nextNote(note)
			accompaniment.nextRythm(0.25)
			if (j == 0 or j == 7 or j==3 or j == 10):			
				force = -4	
			else:
				force = -11
			force = music.getForce(force, beat)
			beat = beat + 0.25	
			accompaniment.forceEvent(force)
	return accompaniment.getMusic()

#For Light
def generateAccompaniment1(bar, length, scale, chords, starttime):
	accompaniment = voice.Voice(starttime)
	acc = 0
	beat = starttime
	note = None
	starttime = int(starttime/bar) #because the chords are ordered by bar
	for i in range (starttime, starttime+int(length/bar)):#process one chord and bar at a time
		for j in range (0, bar*2):
			note = scale[chords[i]+acc]
			accompaniment.nextNote(note)
			acc = acc + 2
			if (acc == 6):	
				acc = 0
			accompaniment.nextRythm(0.5)
			if (beat%bar == 0):
				force = 2
			else:
				force = -8	
			force = music.getForce(force, beat)
			beat = beat + 0.5
			accompaniment.forceEvent(force)
	return accompaniment.getMusic()

#For REM
def generateAccompaniment3(bar, length, scale, chords, starttime):
	accompaniment = voice.Voice(starttime)
	acc = 0
	note = None
	beat = starttime
	starttime = int(starttime/bar) #because the chords are ordered by bar
	for i in range (starttime, starttime+int(length/bar)):#process one chord and bar at a time
		for j in range (0, bar*4):
			note = scale[chords[i]+acc]
			accompaniment.nextNote(note)
			if (acc == 0):
				acc = 4 if music.coinflip() else (2)
			else:
				acc = 0
			accompaniment.nextRythm(0.25)
			if (beat%bar == 0):
				force = 2
			else:
				force = -8
			force = music.getForce(force, beat)
			accompaniment.forceEvent(force)
			beat = beat + 0.25	
	return accompaniment.getMusic()

#For Deep
def generateAccompaniment2(bar, length, scale, chords, starttime):
	accompaniment = voice.Voice(starttime)
	acc = 0
	note = None
	beat = starttime
	starttime = int(starttime/bar) #because the chords are ordered by bar
	for i in range (starttime, starttime+int(length/bar)):#process one chord and bar at a time
		for j in range (0, bar):
			note = scale[chords[i]+acc]
			accompaniment.nextNote(note)
			acc = acc + 4
			if (acc >= 4):	
				acc = 0
			accompaniment.nextRythm(1)
			beat = beat + 1	
			force = -6
			force = music.getForce(force, beat)
			accompaniment.forceEvent(force)
	return accompaniment.getMusic()

