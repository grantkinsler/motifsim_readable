from cell import Cell

class Population:

	def __init__(self,cells,nr_motifs,nr_strands,nr_cells_with_motif):
		self.cells = cells # list of cell objects in the population
		self.nr_motifs = self.count_motifs()
		self.nr_strands = self.count_strands()
		self.nr_cells_with_motif = self.count_cells_with_motif()

	# populate the population with empty cells
	def populate(self,numCells,motif,max_strand_nr):
		for cell_iterator in xrange(numCells):
			self.cells.append(Cell([],[],motif,max_strand_nr,'empty','empty','empty'))

	# update counters of the population
	def update_counters(self):
		self.nr_motifs = self.count_motifs() # number of motifs in the population
		self.nr_strands = self.count_strands() # number of non-empty strands in the population
		self.nr_cells_with_motif = self.count_cells_with_motif() # number of cells with motif in the population

	# count the number of motifs in population
	def count_motifs(self):
		motif_count = 0
		for cell in self.cells:
			motif_count = motif_count + cell.motif_count()

		return motif_count

	# count number of non-empty strands in population
	def count_strands(self):
		strand_count = 0
		for cell in self.cells:
			strand_count = strand_count + cell.nr_strands()
		return strand_count

	# count number of cells with motif in population
	def count_cells_with_motif(self):
		cell_count = 0
		for cell in self.cells:
			if cell.has_motif == True:
				cell_count += 1

		return cell_count

	# return lists with the contents of the population
	def returncontents(self):
		contents = [] 
		elong_contents = []

		# each entry in contents lists correponds with a cell
		for cell in self.cells:
			contents.append(cell.strands) # strands in the cell
			elong_contents.append(cell.elongations) # elongation patterns of those strands

		return contents, elong_contents
