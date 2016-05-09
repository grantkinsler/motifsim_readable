
import sys
import getopt
from motifsim_motifoutput import motifsim_motifoutput
from motifsim_fulltrialoutput import motifsim_fulltrialoutput
from motifsim_allstrandoutput import motifsim_allstrandoutput
from motifsim_elongdataoutput import motifsim_elongdataoutput

def usage():
	print "Running a Motif Simulation using the parameters designated by options\n"
	print "PARAMETERS:"
	print "--testprefix		String, specifies text to be included in prefix of files for this run"
	print "--trials		Integer, specifies number of trials to be run (must be > 1)" 
	print "--maxStrands		Integer, specifies maximum number of strands per cell"
	print "--maxStrandLength	Integer, specifies maximum strand length"
	print "--numCells		Integer, specifies number of cells in population"
	print "--numRounds		Integer, specifies number of rounds in a trial"
	print "--motif 		Binary String, specifies the motif that biases elongation"
	print "--elong 		Float (between 0 and 1), specifies elongation probability"
	print "--bias 			Float (between 0 and 1), specifies probability of adding a 0 monomer in presence of motif"
	print "--elongdata 		Boolean, specifies whether or not elongation data should be tracked and exported (False if not specified)\n"
	print "Example Run:"
	print "python motifsim_master.py --testprefix=Test --trials=5 --maxStrands=100 --maxStrandLength=7 --numCells=100 --numRounds=100 --motif=10000 --elong=0.05 --bias=0.8\n"
	print "Outputs three csv files:\n"
	print "1. 'MotifData' designates the csv file containing primarily motif data. First row is parameters."
	print "For each trial, a row of motif frequency per round, a row of freq of total nr_strands used per round, a row of freq_nr_cells_with_motif per round"
	print "Last 6 rows are mean (by round) of the three data types collected, and then standard deviation of the same.\n"
	print "2. 'FullTrial1Data' designates a csv file where each row represents the cell contents for a single cell at a particular time point (plus first row of parameters)."
	print "The first numCells rows are the cells after the first round.\n"
	print "3. 'AllStrandData' designates a csv file where the first row is a list of all possible strands in the simulation."
	print "The rows beneath correspond chronologically with time, first with all mean data and then with stdev data (mean1, mean2, ..., stdev1, stdev2, ...)\n"
	print "4. 'ElongData' designates a csv file where the first row is a list of the possible elongation patterns, the next row is the same as beginning of 'AllStrandData'"
	print "The rows beneath correspond chronologically with time and the elongationpattern, first with all mean data and then with stdev data (mean1-,mean1+,mean1--, ..., mean2-, ..., stdev1-,... stdev2-, ...) "

def main(argv):

	try:
		opts, args = getopt.getopt(argv, "h", ["help","testprefix=","trials=","maxStrands=","maxStrandLength=","numCells=","numRounds=","motif=","elong=","bias=","elongdata="])
	except getopt.GetoptError, error:
		sys.stderr.write(str(error)+"\n")
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt =="--testprefix":
			testprefix = arg
		elif opt == "--trials" :
			trials = int(arg)
		elif opt == "--maxStrands" :
			max_strand_nr = int(arg)
		elif opt == "--maxStrandLength" :
			maxStrandLength = int(arg)
		elif opt == '--numCells' :
			numCells = int(arg)
		elif opt == '--numRounds' :
			numRounds = int(arg)
		elif opt == '--motif' :
			motif = arg
		elif opt == '--elong' :
			elong = float(arg)
		elif opt == '--bias' :
			bias = float(arg)
		elif opt == '--elongdata' :
			elongdata = arg
		else:
			sys.stderr.write("Unknown option %s\n" %opt)
			usage()
			sys.exit(2)

	masterprefix = 'MotifSimulation_'

	parameterlist = [trials, max_strand_nr, maxStrandLength, numCells, numRounds, repr(motif), elong, bias]

	# run the trials and output frequency information
	pop_tracker, nr_strands_per_time, elongation_tracker = motifsim_motifoutput(parameterlist,masterprefix,testprefix,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias)

	# output full data (all of the cells and strands) for the first trial
	motifsim_fulltrialoutput(parameterlist,masterprefix,testprefix,pop_tracker[0],elongation_tracker[0],trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias)

	# output strand frequency data
	strand_number_dict, keyorder = motifsim_allstrandoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias)

	try:
		elongdata
	except:
		elongdata =  'False'

	if elongdata == 'True':
		# output elongation pattern data
		motifsim_elongdataoutput(keyorder,parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,elongation_tracker,strand_number_dict,trials,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias)


if __name__ == "__main__":
	main(sys.argv[1:])







