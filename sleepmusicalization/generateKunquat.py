"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

Creates all the files needed for making a kunquat song and copies the data stored in variables into the files. 
"""	
import os
import simplejson
import json
import shutil

installation_dir = os.path.dirname(__file__)


def makeDirectories(songdir="kqtc00"):
#remove previous
	shutil.rmtree(songdir, True)
#Make main dir for song
	os.mkdir(songdir)
#Make instrument directory manually
#	os.mkdir(songdir+"/ins_00/")
#	os.mkdir(songdir+"/ins_00/kqti00")
#	os.mkdir(songdir+"/ins_00/kqti00/gen_00")
#	os.mkdir(songdir+"/ins_00/kqti00/gen_00/kqtg00")
#don't do if copying!

#Make subsong directory
	os.mkdir(songdir+"/subs_00/")
#Make pattern directory
	os.mkdir(songdir+"/pat_000/")

def makeColumnDir(columnNumber, songdir="kqtc00"):
	os.mkdir(songdir+"/pat_000/col_"+columnNumber)

#at the moment this only makes the minimun files for playing some sound with minimum settings done...
def makeFiles(songdir="kqtc00"):
#rootfile
	f = open(songdir+"/p_connections.json", "w")
	f.write('[["ins_00/kqtiXX/out_00", "out_00"], ["ins_01/kqtiXX/out_00", "out_00"], ["ins_03/kqtiXX/out_00", "out_00"]]')
	f.close()
	f = open(songdir+"/p_composition.json", "w")
	f.write('{"mix_vol" : -8}') #desibels
	f.close()
#instrument set up
#by copying
	shutil.copytree(os.path.join(installation_dir, "ins_00"), songdir+"/ins_00")
#	shutil.copytree(os.path.join(installation_dir, "ins_01"), songdir+"/ins_01") 
#	shutil.copytree(os.path.join(installation_dir, "ins_03"), songdir+"/ins_03")
#Sine-wave
#	f = open(songdir+"/ins_00/kqti00/p_connections.json", "w")
#	f.write('[["gen_00/kqtgXX/C/out_00", "out_00"]]')
#	f.close()
#	f = open(songdir+"/ins_00/kqti00/gen_00/kqtg00/p_gen_type.json", "w")
#	f.write('\"add\"')
#	f.close()
#subsong set up
	f = open(songdir+"/subs_00/p_subsong.json", "w")
	f.write('{"patterns": [0]}')
	f.close()

#write pattern 
def patternWriter (lenght, songdir="kqtc00"):
	f = open(songdir+"/pat_000/p_pattern.json", "w")
	f.write('{"length": '+json.dumps(lenght)+'}')
	f.close()

#must be called seperately for each column. Column = 1 voice
def columnWriter (columnNumber, columndata, songdir="kqtc00"):
	if (columnNumber < 10 ):
		columnNumber = "0"+str(columnNumber)
	else:
		columnNumber = str(columnNumber)		
	makeColumnDir(columnNumber, songdir)
	f = open(songdir+"/pat_000/col_"+columnNumber+"/p_events.json", "w")
	f.write(simplejson.dumps(columndata))
	f.close()
	
