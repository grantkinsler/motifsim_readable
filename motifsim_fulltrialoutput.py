
import csv

def motifsim_fulltrialoutput(parameterlist,masterprefix,testprefix,trial_population_data,trial_elongation_data,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias):

	with open(masterprefix + testprefix +'_FullTrial1Data_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif = motif, maxStrandLength = maxStrandLength, bias= bias, elong=elong, trials=trials, numRounds=numRounds), 'wb') as f:

		strand_writer = csv.writer(f, quotechar="'", quoting=csv.QUOTE_ALL) # making sure we put quotes around our strings so they're not read as numbers
		parameter_writer = csv.writer(f) # we don't need the quotes for the parameter list

		# write parameters into first row
		parameter_writer.writerow(parameterlist)

		# iterate through time points (only for first trial)
		for time_point in xrange(numRounds):
			# iterate through cells in the population at that time point
			for cell in xrange(numCells):
				# write a row with all strands in the cell at that time point
				strand_writer.writerow(trial_population_data[time_point][cell])
				# write a row with the elongation patterns of the strands in the cell
				strand_writer.writerow(trial_elongation_data[time_point][cell])

	f.close()
