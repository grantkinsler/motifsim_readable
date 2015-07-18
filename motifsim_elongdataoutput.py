
import csv
import collections
import numpy
import itertools
from copy import copy

def makeKeyorder(maxstrandlen): # create the keyorder for the order of our dictionary
	
	keyorder = []

	for n in range(maxstrandlen): # create order of keys for the ordered dictionary
		for key in itertools.product(range(2),repeat = n+1):
			mod_key = str(key).strip(" ,(),','").replace(", ", "")
			if len(keyorder) > 0:
				if len(mod_key) == len(keyorder[-1]):
					has_placed = False
					for keys_so_far in range(len(keyorder)):
						if len(mod_key) == len(keyorder[keys_so_far]):
							if mod_key.count('1') < keyorder[keys_so_far].count('1') and has_placed == False:
								keyorder.insert(keys_so_far,mod_key)
								has_placed = True
								break
					if has_placed == False:
						keyorder.append(mod_key)
				else:
					keyorder.append(mod_key)
			else:
				keyorder.append(mod_key)

	elongkeyorder = []
	for key in keyorder:
		elongkeyorder.append(copy(key.replace("0","-").replace("1","+")))

	return keyorder, elongkeyorder

def motifsim_elongdataoutput(keyorder,parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,elongation_tracker,strand_number_dict,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias):

	elongkeyorder = []
	for key in keyorder:
		elongkeyorder.append(copy(key.replace("0","-").replace("1","+")))

	dict_per_time = []

	for time_point in xrange(numRounds):
		dict_per_time.append([])
		for key in xrange(len(keyorder)):
			dict_per_time[time_point].append([])
			for elongkey in xrange(len(elongkeyorder)):
				dict_per_time[time_point][key].append([0 for trial in xrange(trials)])

		for trial in xrange(trials):
			for cell in xrange(len(pop_tracker[trial][time_point])):
				for strand in xrange(len(pop_tracker[trial][time_point][cell])):
					dict_per_time[time_point][keyorder.index(pop_tracker[trial][time_point][cell][strand])][elongkeyorder.index(elongation_tracker[trial][time_point][cell][strand])][trial] += 1
			for key in xrange(len(keyorder)):
				for elongkey in xrange(len(elongkeyorder)):
					if float(strand_number_dict[trial][time_point][keyorder[key]]) > 0:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])/float(strand_number_dict[trial][time_point][keyorder[key]])
					else:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])

	with open(masterprefix + testprefix +'_ElongData_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif = motif, maxStrandLength = maxStrandLength, bias= bias, elong=elong, trials=trials, numRounds=numRounds), 'wb') as f:
		parameter_writer = csv.writer(f)
		strand_writer = csv.writer(f, quotechar="'", quoting=csv.QUOTE_ALL)

		parameter_writer.writerow(parameterlist)
		parameter_writer.writerow(elongkeyorder)
		strand_writer.writerow(keyorder)

		for time_point in xrange(numRounds):
			for elongkey in xrange(len(elongkeyorder)):
				time_elong_list = []
				for key in xrange(len(keyorder)):
					time_elong_list.append(numpy.mean(dict_per_time[time_point][key][elongkey]))
				parameter_writer.writerow(time_elong_list)
		for time_point in xrange(numRounds):
			for elongkey in xrange(len(elongkeyorder)):
				time_elong_list = []
				for key in xrange(len(keyorder)):
					time_elong_list.append(numpy.std(dict_per_time[time_point][key][elongkey],dtype=numpy.float64))
				parameter_writer.writerow(time_elong_list)

	f.close()