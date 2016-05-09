import random as rand

class Cell:

	def __init__(self,strands,elongations,motif,max_strand_nr,nr_motifs,has_motif,nr_bases):
		self.strands = strands # the strands in the cell
		self.elongations = elongations # elongation patterns of the strands in the cell
		self.motif = motif # motif that is active
		self.max_strand_nr = max_strand_nr # maximum number of strands allowed in cell
		self.nr_motifs = self.motif_count() # number of motifs in the cell
		self.has_motif = self.check_for_motif() # indicator of whether cell has motif or not
		self.nr_bases = self.find_nr_bases() # total length of strands in the cell

	# check if a motif is in the cell
	def check_for_motif(self):
		if self.nr_motifs > 0:
			return True
		else:
			return False

	# count the number of motifs in the cell
	def motif_count(self):
		motif_count = 0
		for strand_iterator in xrange(self.nr_strands()):
			if str(self.motif) in self.strands[strand_iterator]:
				motif_count += 1
		return motif_count

	# update indicators of motif
	def update_motifs(self):
		self.nr_motifs = self.motif_count()
		self.has_motif = self.check_for_motif()

	# update number of bases
	def update_nr_bases(self):
		self.nr_bases = self.find_nr_bases()

	# count number of bases (total strand length)
	def find_nr_bases(self):
		nr_bases = 0
		for strand in self.strands:
			nr_bases += len(strand)
		return nr_bases

	# count number of non-empty strands in cell
	def nr_strands(self):
		strand_counter = 0
		for strand in self.strands:
			if len(strand) > 0:
				strand_counter += 1
		return strand_counter

	# grow cell contents
	def grow(self,elong,bias,maxStrandLength):
		# iterate through the non-empty strands
		for strand_iterator in xrange(self.nr_strands()): 
			# with probability "elong" and if strand is not at maximum length, then elongate
			if rand.uniform(0,1) < elong and len(self.strands[strand_iterator]) < maxStrandLength:
				if self.has_motif == True:
					# if the cell has a motif, add a 0 with probability "bias"
					if rand.uniform(0,1) < bias:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "0"
						self.elongations[strand_iterator] = self.elongations[strand_iterator] + "+" # + indicates motif present during elongation event
					else:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "1"
						self.elongations[strand_iterator] = self.elongations[strand_iterator] + "+" # + indicates motif present during elongation event
				else:
					# if no motif in cell, add monomers with equal probability
					if rand.uniform(0,1) < 0.5:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "0"
						self.elongations[strand_iterator] = self.elongations[strand_iterator] + "-" # - indicates motif not present during elongation event
					else:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "1"
						self.elongations[strand_iterator] = self.elongations[strand_iterator] + "-" # - indicates motif not present during elongation event
		# iterate through remaining empty strands
		for empty_iterator in xrange(self.max_strand_nr-self.nr_strands()):
			# elongate with probability "elong"
			if rand.uniform(0,1) < elong:
				if self.has_motif == True:
					# if the cell has a motif, add a 0 with probability "bias"
					if rand.uniform(0,1) < bias:
						self.strands.append("0")
						self.elongations.append("+")
					else:
						self.strands.append("1")
						self.elongations.append("+")
				else:
					# if no motif in cell, add monomers with equal probability
					if rand.uniform(0,1) < 0.5:
						self.strands.append("0")
						self.elongations.append("-")
					else:
						self.strands.append("1")
						self.elongations.append("-")

		# update indicators
		self.update_motifs()
		self.update_nr_bases()

	# divide a cell
	def divide(self):
		# initialize new cell
		new_cell = Cell([],[],self.motif,self.max_strand_nr,'empty','empty','empty')

		strand_counter = 0
		# iterate through all of the strands in the cell
		for strand_number in xrange(self.nr_strands()):
			# each strand has .5 probability of going to new cell or staying
			if rand.uniform(0,1) < 0.5:
				new_cell.strands.append(self.strands.pop(strand_counter)) # this strand is removed from cell and added to new cell
				new_cell.elongations.append(self.elongations.pop(strand_counter)) # transfer elongation pattern over as well
			else:
				strand_counter += 1

		# update counters for new cell and existing
		new_cell.update_motifs()
		new_cell.update_nr_bases()
		self.update_motifs()
		self.update_nr_bases()

		return new_cell




