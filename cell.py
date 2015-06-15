import random as rand

class Cell:

	def __init__(self,strands,motif,max_strand_nr,nr_motifs,has_motif,nr_bases):
		self.strands = strands
		self.motif = motif
		self.max_strand_nr = max_strand_nr
		self.nr_motifs = self.motif_count()
		self.has_motif = self.check_for_motif()
		self.nr_bases = self.find_nr_bases()


	def check_for_motif(self):
		if self.nr_motifs > 0:
			return True
		else:
			return False

	def motif_count(self):
		motif_count = 0
		for strand_iterator in range(self.nr_strands()):
			if str(self.motif) in self.strands[strand_iterator]:
				motif_count += 1
		return motif_count

	def update_motifs(self):
		self.nr_motifs = self.motif_count()
		self.has_motif = self.check_for_motif()

	def update_nr_bases(self):
		self.nr_bases = self.find_nr_bases()

	def find_nr_bases(self):
		nr_bases = 0
		for strand in self.strands:
			nr_bases += len(strand)
		return nr_bases

	def nr_strands(self):
		strand_counter = 0
		for strand in self.strands:
			if len(strand) > 0:
				strand_counter += 1
		return strand_counter

	def grow(self,elong,bias,maxStrandLength):
		for strand_iterator in range(self.nr_strands()): 
			if rand.uniform(0,1) < elong and len(self.strands[strand_iterator]) < maxStrandLength:
				if self.has_motif == True:
					if rand.uniform(0,1) < bias:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "0"
					else:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "1"
				else:
					if rand.uniform(0,1) < 0.5:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "0"
					else:
						self.strands[strand_iterator] = self.strands[strand_iterator] + "1"

		for empty_iterator in range(self.max_strand_nr-self.nr_strands()):
			if rand.uniform(0,1) < elong:
				if self.has_motif == True:
					if rand.uniform(0,1) < bias:
						self.strands.append("0")
					else:
						self.strands.append("1")
				else:
					if rand.uniform(0,1) < 0.5:
						self.strands.append("0")
					else:
						self.strands.append("1")

		self.update_motifs()
		self.update_nr_bases()

	def divide(self):
		new_cell = Cell([],self.motif,self.max_strand_nr,'empty','empty','empty')
		strand_counter = 0
		for strand_number in range(self.nr_strands()):
			if rand.uniform(0,1) < 0.5:
				new_cell.strands.append(self.strands.pop(strand_counter)) # this strand is removed from cell and added to new cell
			else:
				strand_counter += 1

		new_cell.update_motifs()
		new_cell.update_nr_bases()
		self.update_motifs()
		self.update_nr_bases()

		return new_cell







