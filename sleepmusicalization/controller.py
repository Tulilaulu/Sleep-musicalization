"""
This file was written by Aurora Tulilaulu and it is a part of the sleep musicalization project at http://sleepmusicalization.net/

This work is licensed under the Creative Commons Attribution-NonCommercial 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

This is the old controller for making songs. Not used anymore.
"""
import reader
import music
import generateKunquat
import debug

#makes Kunquat songs in default directory for now (kqtc00)
#fetchsleepdata  #uncomment later

def composeSong(analysis_result_json_string, sleep_result_json_string):
	respiration_timestamps, respiration_cycle_lengths, ihr_timestamps, ihr_values, actigram_timestamps = reader.getSignalAnalysisResults(analysis_result_json_string)
	
	reader.processSleepData(sleep_result_json_string)
	
	actigram = reader.processActigram(actigram_timestamps)
	
	respiration = reader.processRespirationVariability(analysis_result_json_string) 
	IHR = reader.processIHR(ihr_timestamps, ihr_values)
	
	reader.syncStages(IHR) #take tempos and stages and make the faster stages have more beats and slower ones less. Gets stages from reader...
	
	nightLength = reader.getNightLength()
	generateKunquat.makeDirectories()
	generateKunquat.makeFiles()
	voices = 2 #not counting actigramtrack
	scaletype = 1#0 for minor, 1 for Major
	music.generate([], voices, reader.getNightLength(), reader.getStages(), respiration, scaletype, actigram) #second last parameter = rythm dencity, last parameter = volume variation
	
	#music.actigramNoise(actigram)
	
	music.setTempos(IHR) #works with both respiration and IHR
	
	voices = music.howManyVoices() #now counting actigramtrack
	for i in range(voices): #for each voice (if several)
	#	print str(i)+":"
	#	if (i==2):
	#		print music.getVoice(i)
		generateKunquat.columnWriter(i, music.getVoice(i))
	generateKunquat.patternWriter(music.getLength()+4)
	#debug.debugRythm(music)
	debug.debugprint(music)


def main():
	analysis_result_json_string = open("json_export_sample/joonas_2012-05-10 00:00:00_result.json").read()
	sleep_result_json_string = open("json_export_sample/joonas_2012-05-10 00:00:00_sleep.json").read()
	
	composeSong(analysis_result_json_string, sleep_result_json_string)

if __name__ == "__main__":
	main()
