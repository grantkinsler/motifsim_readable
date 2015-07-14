from cell import Cell
from population import Population
import random as rand
from copy import deepcopy
from copy import copy

def motifsim_trial(motif,max_strand_nr,maxStrandLength,numCells,numRounds,elong,bias):

	population = Population([],'empty','empty','empty')

	population.populate(numCells,motif,max_strand_nr)

	# counter lists
	nr_motifs = []
	nr_strands_used = []
	nr_cells_with_motif = []
	population_tracker = []
	elongation_tracker = []

	for time in xrange(numRounds):
		for cell_iterator in xrange(numCells):
			population.cells[cell_iterator].grow(elong,bias,maxStrandLength)

		cell_to_divide = rand.sample(range(numCells),1)[0]

		new_cell = population.cells[cell_to_divide].divide()
		population.cells.append(new_cell)

		population.cells = rand.sample(population.cells,numCells)

		population.update_counters()

		nr_motifs.append(copy(population.nr_motifs))
		nr_strands_used.append(copy(population.nr_strands))
		nr_cells_with_motif.append(copy(population.nr_cells_with_motif))
		population_tracker_temp, elongation_tracker_temp = population.returncontents()
		population_tracker.append(deepcopy(population_tracker_temp))
		elongation_tracker.append(deepcopy(elongation_tracker_temp))

	return nr_motifs, nr_strands_used, nr_cells_with_motif, population_tracker, elongation_tracker