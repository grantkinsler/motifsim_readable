from cell import Cell
from population import Population
import random as rand
from copy import deepcopy
from copy import copy

def motifsim_trial(motif,max_strand_nr,maxStrandLength,numCells,numRounds,elong,bias):

	# initialize empty population
	population = Population([],'empty','empty','empty')

	# populate the population with empty cells
	population.populate(numCells,motif,max_strand_nr)

	# counter lists
	nr_motifs = [] # contains number of motifs in the population
	nr_strands_used = [] # contains number of non-empty strands in population
	nr_cells_with_motif = [] # contains number of cells with the motif
	population_tracker = [] # contains cells and strands of entire population
	elongation_tracker = [] # contains elongation patterns of all the strands

	# iterate through numRounds amount of times
	for time in xrange(numRounds):
		# iterate through the cells in the population
		for cell_iterator in xrange(numCells):
			# grow the contents of the cell
			population.cells[cell_iterator].grow(elong,bias,maxStrandLength)

		# pick a cell at random to divice
		cell_to_divide = rand.sample(range(numCells),1)[0]

		# create new daughter cell, distributing contents between the new and existing
		new_cell = population.cells[cell_to_divide].divide()

		# add this new cell to the population
		population.cells.append(new_cell)

		# select the new population (killing one cell)
		population.cells = rand.sample(population.cells,numCells)

		# update population counters
		population.update_counters()

		# update running counter lists for this time point
		nr_motifs.append(copy(population.nr_motifs))
		nr_strands_used.append(copy(population.nr_strands))
		nr_cells_with_motif.append(copy(population.nr_cells_with_motif))
		population_tracker_temp, elongation_tracker_temp = population.returncontents()
		population_tracker.append(deepcopy(population_tracker_temp))
		elongation_tracker.append(deepcopy(elongation_tracker_temp))

	return nr_motifs, nr_strands_used, nr_cells_with_motif, population_tracker, elongation_tracker