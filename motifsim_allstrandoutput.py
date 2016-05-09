
import csv
import collections
import numpy
import itertools

def makeKeyorder(maxstrandlen): # create the keyorder for the order of our dictionary
	
	# keyorder sorted first by length, and then by number of 1s in the key

	keyorder = []

	for n in xrange(maxstrandlen): # create order of keys for the ordered dictionary
		for key in itertools.product(range(2),repeat = n+1): # generate all possible tuples of length n+1 with 0 and 1
			mod_key = str(key).strip(" ,(),','").replace(", ", "") # convert string into proper form (removing tuples)
			
			# insert keys in proper order
			if len(keyorder) > 0:
				# first sort by key length
				if len(mod_key) == len(keyorder[-1]):
					# for a given length
					for keys_so_far in xrange(len(keyorder)):
						if len(mod_key) == len(keyorder[keys_so_far]):
							# sort by number of 1 in the list
							if mod_key.count('1') < keyorder[keys_so_far].count('1'):
								keyorder.insert(keys_so_far,mod_key)
								break
					else:
						keyorder.append(mod_key)
				else:
					keyorder.append(mod_key)
			else:
				keyorder.append(mod_key)

	return keyorder # contains all possible strands

def motifsim_allstrandoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias):

	# make the keyorder (all possible strands)
	keyorder = makeKeyorder(maxStrandLength)

	# initialize lists 
	time_trial_dict = [] # frequency of every strand for each trial at each time
	dict_per_time = []  # for a given time, info for all trials

	# fill lists with initialized value
	for trial in xrange(trials):
		time_trial_dict.append([])
		for time_point in xrange(numRounds):
			temp_dict = {}
			if trial == 0:
				temp2_dict = {} 
			for key in keyorder:
				temp_dict[key] = 0 
				if trial == 0:
					temp2_dict[key] = []
			if trial == 0:
				dict_per_time.append(collections.OrderedDict(sorted(temp2_dict.items(), key = lambda i:keyorder.index(i[0])))) # ordered dict with keys in order of keyorder
			time_trial_dict[trial].append(collections.OrderedDict(sorted(temp_dict.items(), key = lambda i:keyorder.index(i[0]))))

	for trial in xrange(trials):
		for time_point in xrange(numRounds):
			for cell in xrange(len(pop_tracker[trial][time_point])):
				for strand in pop_tracker[trial][time_point][cell]:
					time_trial_dict[trial][time_point][strand] = time_trial_dict[trial][time_point][strand] + 1 # this strand was at this trial and time point

			for key, value in time_trial_dict[trial][time_point].iteritems():
				dict_per_time[time_point][key].append(int(value)/float(nr_strands_per_time[time_point][trial])) # strand's frequency per time point over all trials

	stdev_dict = [] 
	mean_dict = []

	for time_point in xrange(numRounds):
		temp_mean = {}
		temp_stdev = {}
		for key in keyorder:
			temp_mean[key] = numpy.mean(dict_per_time[time_point][key]) # mean strand frequency
			temp_stdev[key] = numpy.std(dict_per_time[time_point][key],dtype=numpy.float64) # standard deviation of strand frequency
		mean_dict.append(collections.OrderedDict(sorted(temp_mean.items(), key = lambda i:keyorder.index(i[0])))) # mean strand frequencies per time point
		stdev_dict.append(collections.OrderedDict(sorted(temp_stdev.items(), key = lambda i:keyorder.index(i[0])))) # standard deviation strand frequencies per time point


	with open(masterprefix + testprefix +'_AllStrandData_motif{motif}_len{maxStrandLength}_bias{bias}_elong{elong}_{trials}trials_numRound{numRounds}.csv'.format(motif = motif, maxStrandLength = maxStrandLength, bias= bias, elong=elong, trials=trials, numRounds=numRounds), 'wb') as f:
		parameter_writer = csv.writer(f) 
		dict_writer = csv.DictWriter(f,mean_dict[0].keys())
		dict_header_writer = csv.DictWriter(f,mean_dict[0].keys(),quotechar="'", quoting=csv.QUOTE_ALL)

		parameter_writer.writerow(parameterlist) # write parameters
		dict_header_writer.writeheader() # write out keyorder (the possible strands)

		for time_point in xrange(numRounds):
			dict_writer.writerow(mean_dict[time_point]) # write out mean strand frequencies per time point averaged over trials
		for time_point in xrange(numRounds):
			dict_writer.writerow(stdev_dict[time_point]) # write out standard deviation of strand frequencies per time point averaged over trials

	f.close()

	return time_trial_dict, keyorder
