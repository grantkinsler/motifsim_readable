Motif Simulation
Grant Kinsler
Written: 15/06/2015
Last Update: 08/05/2016

motifsim_master.py is the master file of the simulation. Options used to indicate the parameters used in the run.

Example run:
python motifsim_master.py --testprefix=Test --trials=5 --maxStrands=100 --maxStrandLength=7 --numCells=100 --numRounds=100 --motif=10000 --elong=0.05 --bias=0.8 (--elongdata=False)

Use --help option for more information on parameter options.
List of other necessary files:
motifsim_trial.py; runs a trial of the simulation
motifsim_motifoutput.py; runs simulations and controls motif data csv output
motifsim_allstrandoutput.py; controls all data csv output
motifsim_fulltrialoutput.py; controls full trial 1 data dsv output
cell.py; defines Cell class
population.py; defines Population class
