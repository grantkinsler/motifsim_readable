import sys
import argparse

class objectview(object):
	    def __init__(self, d):
		            self.__dict__ = d

def print_template():
	print """TEMPLATE FOR AN INPUT FILE, ORDER IS UNIMPORTANT, NO EMPTY LINES:
	testprefix [string]
	trials [int]
	growthIterations [int]
	maxStrands [int]
	maxStrandLength [int]
	numCells [int]
	numRounds [int]
	motif [string]
	elong [float]
	bias [float]
	basenumber [int]
	p_divide [float]"""

def parse_file(filename):
	try:
	    with open(filename) as inp:
		dict_params=dict(line.rstrip().split(None,1) for line in inp)
	    params_obj=objectview(dict_params)
	    
            testprefix=params_obj.testprefix
	    trials=int(params_obj.trials)
            growthIterations=int(params_obj.growthIterations)
	    max_strand_nr=int(params_obj.maxStrands)
	    maxStrandLength=int(params_obj.maxStrandLength)
	    numCells=int(params_obj.numCells)
	    numRounds=int(params_obj.numRounds)
	    motif=params_obj.motif
	    elong=float(params_obj.elong)
            bias=float(params_obj.bias)
	    basenumber=int(params_obj.basenumber)
	    p_divide=float(params_obj.p_divide)

	    masterprefix = 'MotifSimulation_'

	    parameterlist = [trials, growthIterations, max_strand_nr, maxStrandLength, numCells, numRounds, repr(motif), elong, elong, bias, basenumber, p_divide]

	    pop_tracker, nr_strands_per_time = motifsim_motifoutput(parameterlist,masterprefix,testprefix,trials,growthIterations,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias,basenumber,p_divide)

	    motifsim_fulltrialoutput(parameterlist,masterprefix,testprefix,pop_tracker[0],trials,growthIterations,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias,basenumber,p_divide)

	    motifsim_allstrandoutput(parameterlist,masterprefix,testprefix,pop_tracker,nr_strands_per_time,trials,growthIterations,max_strand_nr,maxStrandLength,numCells,numRounds,motif,elong,bias,basenumber,p_divide)

	
        except Exception as e:
		sys.stderr.write("Error while reading input file: \n %s \n" %e)
	    

if __name__=="__main__":
	parser=argparse.ArgumentParser()
	parser.add_argument('-f','--filename',dest='filename',help='Provide an input file that contains the required parameters\
			,\n for more info try --info')
	parser.add_argument('--info',action='store_true',help='prints a template input file')
	args=parser.parse_args()

	if args.info:
	    print_template()
	else:
	    parse_file(args.filename)

