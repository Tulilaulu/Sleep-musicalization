"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

This is the abstraction for a voice in the music. 
"""
from kunquat.editor.timestamp import Timestamp

class Voice:
	def __init__(self, starttime):
	   self.noteOn = []
	   self.noteOff = []
	   self.starttime = starttime
	   self.notes = []
	   self.themes = []
	   self.others = []
	   self.lastrythm = 1
	def nextRythm(self, num):
		self.lastrythm = num
		if not self.noteOn:
			self.noteOff.append(num+self.starttime)
			self.noteOn.append(self.starttime)
		else:	
			self.noteOn.append(self.noteOff[-1])
			self.noteOff.append(num+self.noteOn[-1])
	def nextNote(self, note):
		self.notes.append(note)
	def getThemes():
		return self.themes
	def getMusic (self):
		music = []
		for i in range(0, len(self.noteOff)):
			music.append([Timestamp(self.noteOn[i]), ["n+", str(self.notes[i])]])
			music.append([Timestamp(self.noteOff[i]),["n-", None]])
		for i in range(0, len(self.others)):
			music.append(self.others[i])
		return music

	def forceEvent(self, force):
		self.others.append([Timestamp(self.noteOn[-1]), [".f", str(force)]])

	def getLastNote(self):
		if not self.notes:
			return 0 #so we start the chain from somewhere
		else:	
			return self.notes[-1]
	def getLastRythm(self):
		return self.lastrythm

