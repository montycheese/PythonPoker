from Card import Card
from random import randint
#implement it like a stack
class Deck(object):
	
	def __init__(self):
		self.SUITS = [
					  "Hearts", "Diamonds",
					  "Spades", "Clubs"
					 ]
		self.RANKINGS = [
						"Ace", "Two", "Three", "Four", "Five", 
						"Six", "Seven", "Eight", "Nine", "Ten",
						"Jack", "Queen", "King"
						]
		self.deck = []
		
	def __str__(self):
		contents = []
		for i in range(len(self.deck)):
			contents.append(str(self.deck[i]))
		return " ".join(contents)

	def create_deck(self):
		for x in range(13):
			for y in range(4):
				card = Card(self.RANKINGS[x], self.SUITS[y])
				self.push(card)
				
	def shuffle(self): 
		for i in range(len(self.deck)*2): 
			randomnum1 = randint(0,len(self.deck)-1)
			randomnum2 = randint(0,len(self.deck)-1)
			temp = self.deck[randomnum1]
			self.deck[randomnum1] = self.deck[randomnum2]
			self.deck[randomnum2] = temp
			
	def deal(self, num_cards, hand): #work on dealing to mult hands later
		for x in range(num_cards):
			hand.push(self.draw())
	
	def reset(self):
		self.deck = []
		self.create_deck()
	
	#Stack Methods
	def is_empty(self): # Probably will go unused
		return self.deck == []
	def push(self, card):
		self.deck.append(card)
	def draw(self): 
		return self.deck.pop()
	def peek(self): # Probably will go unused
		return self.deck[len(self.deck)-1]
	def size(self):
		return len(self.deck)
	#End Stack methods
	
			