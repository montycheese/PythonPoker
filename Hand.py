class Hand(object):
	
	def __init__(self):
		self.hand = []
	
	def __str__(self):
		contents = []
		for i in range(len(self.hand)):
			contents.append(str(self.hand[i]))
		return " ".join(contents)
	
	def is_empty(self):
		return self.hand == []
		
	def push(self, card):
		self.hand.append(card)
	
	def size(self):
		return len(self.hand)
	
	def calculate_value(self): 
		total = 0
		for card in range(self.size()):
			total += self.hand[card].get_value()
		return total
			
	def return_num_suits(self): # as a k-v pair
		num_suits_per_card = dict()
		for card in self.hand:
			try:
				num_suits_per_card[card.get_suit()] += 1
			except KeyError:
				num_suits_per_card[card.get_suit()] = 1
		return num_suits_per_card
		
	def contains(self, rank): #return number of cards of value "x". -1 if None
		count = 0
		for card in self.hand:
			if rank == card.get_rank():
				count+=1
		if count == 0:
			return -1
		else:
			return count
			
	def clear(self):
		self.hand = []
	def get_hand(self): # bad practice but using for sake of pile method contains_straight
		return self.hand
