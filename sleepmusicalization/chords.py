"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Generates the chords-array for the song.
"""
from kunquat.editor.timestamp import Timestamp
import random
import probabilities

def getChords(bar, length):
	chords = []
	for i in range (0, length/bar):
		if (i==0 or i == length/bar): #add "i == 1 or" when checking two back
			chords.append(0)
		elif (i==1):
			chords.append(probabilities.getChord(chords[-1]))
		else:
			chords.append(probabilities.getChord(chords[-1], chords[-2]))
			#chords.append(random.randrange(0, 7)) #this sucks
	return chords
