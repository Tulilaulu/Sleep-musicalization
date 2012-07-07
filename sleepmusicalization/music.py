"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Here is the main logic for generation of the music in the function named "generate". It calls all the other function used. Lots of stuff are in global variables so that they can be easily debug printed, sorry 'bout that.
"""
from kunquat.editor.timestamp import Timestamp
import math
import random
import melody
import accompaniment
import chords
import probabilities

music = [] #store music data, should be in format: [[notes for voice 1], [notes for voice 2], [notes for voice 3]...]
	#notes are in this format: [timestamp(two numbers)], [event(type and parameter)]
scale = [] 
major = [200, 200, 100, 200, 200, 200, 100]
harmonicminor = [200, 100, 200, 200, 100, 300, 100]
dissonances = [100, 200, 600, 1000, 1100]
#perfectconsonances = [0, 700, 1200]
#imperfectconsonances = [300, 400, 500, 800, 900]
#step = [0, 100, -100, 200, -200]
#skip = [300, -300, 400, -400, 500, -500, 600, -600, 700, -700, 800, -800, 900, -900, 1000, -1000, 1100, -1100, 1200, -1200]
bar = 0
chorddata = []
scaletype = None
IHR = []

def howManyVoices():
	voices = len(music)
	return voices

def getLength():
	return music[1][-1][0]

def getScale():
	return scale

def getVoice(number): 
	return music[number]

#returns True half of the time and False otherwise
def coinflip():
	if (random.randrange(0, 2) == 1):
		return True
	else:
		return False
def IHRatTheMoment(beat):
	for a in range(len(IHR)):
		if (IHR[a][0] > beat):
			return IHR[a-1][1]
		if (a-1 == len(IHR)):
			return IHR[a][1]
	return 60 #error :P

#getForce actigram version
def getForce(force, beat):
	beat = int(math.floor(beat))
	try :
		value = actigram[beat]
		value = value[1]
	except Exception:
		value = 5 #default, does not change anything
	if (value > 6):
		force = force + 5
	if (value > 10):
		force = force + 5
	if (value > 15):
		force = force + 5
	if (value < 5):
		force = force - 2
	if (value < 3):
		force = force - 2
	if (value < 2):
		force = force - 1
	return force

#getForce IHR version!
#def getForce(force, beat):
#	ihr = IHRatTheMoment(beat)
#	if (ihr > 70):
#		force = force + 4
#	if (ihr > 80):
#		force = force + 4
#	if (ihr > 90):
#		force = force + 4
#	if (ihr < 50):
#		force = force - 4
#	if (ihr < 40):
#		force = force - 4
#	if (ihr < 30):
#		force = force - 4
#	return force

#generates according to chrods (for melody and one accompaning voice) 
def generate(tempos, voices, length, stages, IHRdata, scaletypenumber, actigramdata):
	global music 
	global bar
	global chorddata
	global IHR 
	global actigram
	actigram = actigramdata
	IHR = IHRdata
	randomScale(scaletypenumber)
	bar = probabilities.getBar()

	stages[-1][1] = stages[-1][1]-(length%bar)

	asdf = 0
	for item in stages:
		asdf = asdf + item[1]
	length = length - (length%bar) #make sure no beats that don't fit in bars are left at the end of the song
	chorddata = chords.getChords(bar, length) #SOINTUASTEET

#generate different melodies for different sleepstages (each 2 bars long)
	lighttheme = melody.generateTheme(bar, 2*bar, scale, chorddata)
	deeptheme = melody.generateTheme(bar, 2*bar, scale, chorddata)
	remtheme = melody.generateTheme(bar, 2*bar, scale, chorddata)
	waketheme = melody.generateTheme(bar, 2*bar, scale, chorddata)

#melody in parts
	music.append([])
	for stage in stages:
		if (music[0] == []):
			starttime = 0
		else:
			starttime = lasttime + starttime
#		if (stage[0] == 'A'): DO NOTHING
#		print "length: "+str(stage[1])
#		print "starttime: "+str(starttime)
		if (stage[0] == 'W'):
			music[0].extend(melody.generateMelody(bar, stage[1], scale, chorddata, starttime, waketheme))
		if (stage[0] == 'R'):
			music[0].extend(melody.generateMelody(bar, stage[1], scale, chorddata, starttime, remtheme))
		if (stage[0] == 'L'):
			music[0].extend(melody.generateMelody(bar, stage[1], scale, chorddata, starttime, lighttheme))
		if (stage[0] == 'D'):
			music[0].extend(melody.generateMelody(bar, stage[1], scale, chorddata, starttime, deeptheme))
		lasttime = stage[1]
#accompaniment in parts:
	music.append([])
	for stage in stages:
		if (music[1] == []):
			starttime = 0
		else:
			starttime = lasttime + starttime#last bracket is the last part of the timestamp
#		if (stage[0] == 'A'): DO NOTHING
		if (stage[0] == 'R'):
			music[1].extend(accompaniment.generateAccompaniment3(bar, stage[1], scale, chorddata, starttime))
		if (stage[0] == 'W'):
			music[1].extend(accompaniment.generateAccompaniment0(bar, stage[1], scale, chorddata, starttime))
		if (stage[0] == 'L'):
			music[1].extend(accompaniment.generateAccompaniment1(bar, stage[1], scale, chorddata, starttime))
		if (stage[0] == 'D'):
			music[1].extend(accompaniment.generateAccompaniment2(bar, stage[1], scale, chorddata, starttime))
		lasttime = stage[1]#next needs to start after the length of the last
	#alternative for forloop: music.append(accompaniment.generateAccompaniment1(bar, length, scale, chorddata, 0))
	#music.append(melody.generateMelody(bar, length, scale, chorddata, 0))
	for a in range (0, len(music)):
		for i in range (0, len(music[a])):
			if (music[a][i][1][1] != None):
				music[a][i][1][1] = str(music[a][i][1][1])
	return music	

#generates random shit without bad dissonances
#not used
def generator1(tempos, voices, lenght):
	scaleLength = len(scale)
	for a in range (0, voices):
		for i in range (0, lenght):
			note = None
			#choosing
			if a != 0:
				previousnote = music[a-1][i][1][1]#previous of other voice?
				while(note == None or ((previousnote - note) % 1200 in dissonances or previousnote - note > 1600)):
					note = scale[random.randrange(0, scaleLength)]
			else: #other voices
				note  =  scale[random.randrange(0, scaleLength)]
			music[a].append([Timestamp(i+1), ["n+", note]])#save
	return music

def randomScale(scaletypenumber):
	global scaletype
	if scaletypenumber != 0:
		scaleType = major
		scaletype = "Major"
	else:
		scaleType = harmonicminor 
		scaletype = "Harmonic minor"
	note = random.randrange(-1800, -800, 100)
	scale.append(note)
	scaleIndex = 0
	for i in range (0, 20):
		note = note + scaleType[scaleIndex]
		scale.append(note)
		scaleIndex = scaleIndex + 1
		if (scaleIndex == 7):
			scaleIndex = 0

#not used anymore, but can be used if other functions related to it are uncommented again
def actigramNoise(actigram):
	i = len(music)
	music.append([])
	music[i].append([Timestamp(0), [".i", "3.0"]]) #change the instrument for this track (3.0 drum, 1.0 tick)
	a = 0
	for item in actigram:
		if (actigram[a]-actigram[a-1]>0.1):	
			music[i].append([Timestamp(actigram[a]), ["n+", "1700"]])
			music[i].append([Timestamp(actigram[a]), [".f", "-20"]]) #20 for drum, 8 for tick
		a = a + 1
	return

def thInScale(note):
	for i in range(0, 8):
		if scale[i]%1200 == note%1200:
			return i
	return -1 #error!

def setTempos(tempos):
	music[0].append([Timestamp(0), ["m.t", "60"]]) #initial tempo
	for item in tempos:
		music[0].append([Timestamp(item[0]), ["m.t", str(item[1])]])

#Random notes conserning the format kunquat uses...

# teemat = yksi teema per univaihe?

# middle A = 4400 Hz = 0
# puolisavelaskel (semitone?) = +/-100

#EVENTS (m=master .=set)
# note on = ["n+", "number"] 
# note off = ["n-", null]
# tempo switch = ["m.t", "bpm"]
# globaali aanenvoimakkuus = ["m.v", "desibeleja"] oletus 0
# nuottikohtainen aanenvoimakkuus = [".f", "desibeleja"] aseta ensin nuotti, samalla ajalla sitten voima

# Timestampille voi antaa arvoksi montako iskua biisin alusta: Timestamp(iskut)
# jsoniksi: import json json.dumps(Timestamp(5.5))
# myohemmin: handle['pat_000/p_pattern.json'] = { 'Length' : Timestamp(16) }
# voi laskea yhteen: Timestamp(4) + Timestamp(1.1)

#actigram, heartrate, hengitys:
#hairio, korkeus (hengitys?), tiheys, tempo (sydan?)

