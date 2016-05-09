
import csv
import collections
import numpy
import itertools
from copy import copy

def motifsim_elongdataoutput(keyorder,parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,elongation_tracker,strand_number_dict,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias):

	elongkeyorder = []
	for key in keyorder:
		elongkeyorder.append(copy(key.replace("0","-").replace("1","+"))) # elongation pattern keyorder

	dict_per_time = []

	for time_point in xrange(numRounds):
		dict_per_time.append([])
		for key in xrange(len(keyorder)):
			dict_per_time[time_point].append([])
			for elongkey in xrange(len(elongkeyorder)):
				dict_per_time[time_point][key].append([0 for trial in xrange(trials)]) # initialize list with all zeros

		for trial in xrange(trials):
			for cell in xrange(len(pop_tracker[trial][time_point])):
				for strand in xrange(len(pop_tracker[trial][time_point][cell])):
					# count the strands and their elongation patterns
					dict_per_time[time_point][keyorder.index(pop_tracker[trial][time_point][cell][strand])][elongkeyorder.index(elongation_tracker[trial][time_point][cell][strand])][trial] += 1
			for key in xrange(len(keyorder)):
				for elongkey in xrange(len(elongkeyorder)):
					# convert into a frequency
					if float(strand_number_dict[trial][time_point][keyorder[key]]) > 0:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])/float(strand_number_dict[trial][time_point][keyorder[key]])
					else:
						dict_per_time[time_point][key][elongkey][trial] = int(dict_per_time[time_point][key][elongkey][trial])

	with open(masterprefix + testprefix +'_ElongData_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif = motif, maxStrandLength = maxStrandLength, bias= bias, elong=elong, trials=trials, numRounds=numRounds), 'wb') as f:
		parameter_writer = csv.writer(f)
		strand_writer = csv.writer(f, quotechar="'", quoting=csv.QUOTE_ALL)

		parameter_writer.writerow(parameterlist) # write parameters
		parameter_writer.writerow(elongkeyorder) # write elongation pattern key order
		strand_writer.writerow(keyorder) # write keyorder

		for time_point in xrange(numRounds):
			for elongkey in xrange(len(elongkeyorder)):
				time_elong_list = []
				for key in xrange(len(keyorder)):
					time_elong_list.append(numpy.mean(dict_per_time[time_point][key][elongkey])) # write out mean frequencies for this elongation pattern
				parameter_writer.writerow(time_elong_list)
		for time_point in xrange(numRounds):
			for elongkey in xrange(len(elongkeyorder)):
				time_elong_list = []
				for key in xrange(len(keyorder)):
					time_elong_list.append(numpy.std(dict_per_time[time_point][key][elongkey],dtype=numpy.float64)) # write out standard deviation of frequencies for this elongation pattern
				parameter_writer.writerow(time_elong_list)

	f.close()