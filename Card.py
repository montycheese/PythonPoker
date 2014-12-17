class Card(object):

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		self.rankings = [
						"Ace", "Two", "Three", "Four", "Five", 
						"Six", "Seven", "Eight", "Nine", "Ten",
						"Jack", "Queen", "King"
						]
	
	def __str__(self):
		return "%s of %s'" % (self.rank, self.suit)
	def __eq__(self, other): # == on two Card objects
		if self.rank == other.get_rank() and self.suit == other.get_suit():
			return True
		else:
			return False
	def __gt__(self, other): # > operator on two Card objects
		if self.get_value() > other.get_value():
			return True
		else:
			return False
	
	def get_value(self):
		for index, rank in enumerate(self.rankings):
			if self.rank == "Ace": # for poker Ace is highest card
				return 14
			if self.rank == self.rankings[index]:
				#if index >= 9: #All face cards have value of 10
				#	return 10 would use this for black jack but not poker
				return index+1
	def get_suit(self):
		return self.suit
	def get_rank(self):
		return self.rank
		
	
		
