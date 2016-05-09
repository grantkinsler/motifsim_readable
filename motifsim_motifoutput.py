import csv
from motifsim_trial import motifsim_trial
import itertools
import numpy

def flatten(items, seqtypes=(list, tuple)): # used for flattening lists
    for i, x in enumerate(items):
        while isinstance(items[i], seqtypes):
            items[i:i+1] = items[i]
    return items

def motifsim_motifoutput(parameterlist,masterprefix,testprefix,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias):
	# initialize lists
	pop_tracker = [] 
	elongation_tracker = []

	# open csv file that will contain frequency data 
	with open(masterprefix+ testprefix +'_MotifData_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif = motif, maxStrandLength = maxStrandLength, bias=bias, elong=elong, trials=trials, numRounds=numRounds), 'wb') as f: 
		writer = csv.writer(f)
		writer.writerow(parameterlist)

		for trial in xrange(trials):
			pop_tracker.append([])
			elongation_tracker.append([])

			# run a trial and return contents
			nr_motifs, nr_strands, nr_cells_with_motif, pop_tracker[trial], elongation_tracker[trial]  = motifsim_trial(motif,max_strand_nr,maxStrandLength,numCells,numRounds,elong,bias)


			# get frequency of motifs per time point
			motif_freq = [motifs / float(total) for motifs,total in itertools.izip(nr_motifs,nr_strands)]
			# get frequency of non-empty strands per time point
			strands_freq = [strands / float(max_strand_nr*numCells) for strands in nr_strands]
			# get frequency of cells containing motif per time point
			cells_with_freq = [cells / float(numCells) for cells in nr_cells_with_motif]

			# write frequency data onto csv file
			writer.writerow(motif_freq)
			writer.writerow(strands_freq)
			writer.writerow(cells_with_freq)

			if trial == 0:
				# begin lists that aggregte the data
				motif_freq_aggregate = motif_freq
				strands_freq_aggregate = strands_freq
				cells_with_freq_aggregate = cells_with_freq
				nr_strands_per_time = nr_strands
			else:
				# aggregate the lists such that list[time] has all the data at that time amongst the trials
				motif_freq_aggregate = [list(round_data) for round_data in zip(motif_freq_aggregate,motif_freq)]
				strands_freq_aggregate = [list(round_data) for round_data in zip(strands_freq_aggregate,strands_freq)]
				cells_with_freq_aggregate = [list(round_data) for round_data in zip(cells_with_freq_aggregate,cells_with_freq)]
				nr_strands_per_time = [list(round_data) for round_data in zip(nr_strands_per_time,nr_strands)]
		
		for time_point in xrange(numRounds):
			# flatten the lists per time point
			motif_freq_aggregate[time_point] = flatten(motif_freq_aggregate[time_point])
			strands_freq_aggregate[time_point] = flatten(strands_freq_aggregate[time_point])
			cells_with_freq_aggregate[time_point] = flatten(cells_with_freq_aggregate[time_point])
			nr_strands_per_time[time_point] = flatten(nr_strands_per_time[time_point])
		
		means = []
		stdevs = [] 

		for iterator in xrange(3):
			means.append([])
			stdevs.append([])

		for time_point in xrange(numRounds):
			# take the mean and standard deviation per time point
			means[0].append(numpy.mean(motif_freq_aggregate[time_point]))
			stdevs[0].append(numpy.std(motif_freq_aggregate[time_point],dtype=numpy.float64))
			means[1].append(numpy.mean(strands_freq_aggregate[time_point]))
			stdevs[1].append(numpy.std(strands_freq_aggregate[time_point],dtype=numpy.float64))
			means[2].append(numpy.mean(cells_with_freq_aggregate[time_point]))
			stdevs[2].append(numpy.std(cells_with_freq_aggregate[time_point],dtype=numpy.float64))

		# write the mean data
		for mean_data in means:
			writer.writerow(mean_data)

		# write the standard deviation data
		for stdev_data in stdevs:
			writer.writerow(stdev_data)
	f.close()

	return pop_tracker, nr_strands_per_time, elongation_tracker
