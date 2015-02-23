from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player

# the community cards that all players can access

class Table(object):
	
	def __init__(self, big_blind = 10):
		self.pot = 0 # amount of money currently bet during a round
		self.big_blind_size = big_blind
		self.small_blind_size = big_blind/2
		self.pile = []
		self.burned_pile = []
		self.hand_rankings = [
							  "High Card", "Pair",
							  "Two Pair", "Three of a Kind",
							  "Straight", "Flush",
							  "Full House", "Four of a Kind",
							  "Straight Flush", "Royal Flush"
							  ]

	def __str__(self):
		contents = []
		for i in range(len(self.pile)):
			contents.append(str(self.pile[i]))
		return "\n".join(contents)
	
	def get_big_blind_size(self):
		return self.big_blind_size
		
	def get_small_blind_size(self):
		return self.small_blind_size
		
	def push(self, card):
		self.pile.append(card)
		
	def burn(self, card):
		self.burned_pile.append(card)
	
	def add_bet(self, bet):
		self.pot += bet
	
	def get_value(self):
		return self.pot
		
	def distribute_winnings_to(self, player, other_player = None): # add feature to distribute to multiple players later using *args
		if other_player != None:
			other_player.wins_money(self.pot/2)
			player.wins_money(self.pot/2) # check to see if any rounding errors 
		else:
			player.wins_money(self.pot)
		#fix later make it so I give person proportional money
	
	#increases blinds every 10 rounds
	def inc_blinds(self,round):
		if round % 10 == 0:
			self.small_blind_size = self.big_blind_size
			self.big_blind_size *= 2	
			
	def set_player_blinds(self, player1, cpu_players):
		players = [player1] + cpu_players
	    # use this to track blinds
		for index, player in enumerate(players):
			if player.is_big_blind():
				players[index].set_blinds(big = False, small = True)
				try:
					players[index+1].set_blinds(big = True, small = False)
				except IndexError: #hit the end of the list
					players[0].set_blinds(big = True, small = False)
				if len(players) > 2:
					try:
						players[index-1].set_blinds()
					except IndexError: #at the first index of list
						player[len(players)-1].set_blinds()

					
		
	def clear(self):
		self.pile = []
		self.burned_pile = []
		self.pot = 0
		
	def find_greatest_value(self, hand):
		#Gonna be ugly
		if self.contains_royal_flush(hand) != -1:
			return 9
		if self.contains_straight_flush(hand) != -1:
			return 8
		if self.contains_four_of_a_kind(hand) != -1:
			return 7
		if self.contains_full_house(hand) != -1:
			return 6
		if self.contains_flush(hand) != -1:
			return 5
		if self.contains_straight(hand) != -1:
			return 4
		if self.contains_three_of_a_kind(hand) != -1:
			return 3
		if self.contains_two_pair(hand) != -1:
			return 2
		if self.contains_pair(hand) != -1:
			return 1
		return 0 # highcard is all they have
	
	def get_hand_ranking(self, val):
		return self.hand_rankings[val]
	
	def get_high_card(self):
		high_card = self.pile[0]
		for card in self.pile:
			if card.get_value() > high_card.get_value():
				high_card = card
		return high_card.get_rank() # might just change it to returning the card's pointer
	
	def contains_pair(self, hand):
		num_of_card = dict()
		cards = self.pile + hand.get_hand()
		for card in cards:
			try:
				num_of_card[card.get_rank()] += 1
			except KeyError:
				num_of_card[card.get_rank()] = 1
		for rank in num_of_card.keys(): 
			if num_of_card[rank] == 2:
				return rank
		return -1
	
	def contains_two_pair(self, hand): 
		num_of_card = dict()
		contains_pair = False
		cards = self.pile + hand.get_hand()
		for card in cards:
			try:
				num_of_card[card.get_rank()] += 1
			except KeyError:
				num_of_card[card.get_rank()] = 1
		for rank in num_of_card.keys(): 
			if num_of_card[rank] == 2 and contains_pair:
				return rank
			if num_of_card[rank] == 2:
				contains_pair = True
		return -1
	
	def contains_three_of_a_kind(self, hand): 
		num_of_card = dict()
		cards = self.pile + hand.get_hand()
		for card in cards:
			try:
				num_of_card[card.get_rank()] += 1
			except KeyError:
				num_of_card[card.get_rank()] = 1
		for rank in num_of_card.keys():
			if num_of_card[rank] == 3:
				return rank
		return -1
		
	def contains_straight(self, hand): 
		cards = self.pile + hand.get_hand()
		values = []
		for card in cards:
			values.append(card.get_value())
		values.sort()
		# check for 5 consecutive ranks
		tally = 0
		highest_value = 0
		for i in range(len(values)-1):
			if (values[i+1] == values[i]):
				continue
			if (values[i+1] - values[i]) == 1:
				tally+=1
				highest_value = values[i]
			else:
				tally = 0
				highest_value = 0
		if tally >= 5:
			return highest_value # i.e. 2- "Two" 3-"Three", etc
		return -1
			
			
	def contains_flush(self, hand): 
		num_of_card = dict()
		cards = self.pile + hand.get_hand()
		for card in cards:
			try:
				num_of_card[card.get_suit()] += 1
			except KeyError:
				num_of_card[card.get_suit()] = 1
		for suit in num_of_card.keys(): # searching through k-v pairs to see if there are any of val 5. if so return it 
			try:
				if num_of_card[suit] >= 5:
					return suit
			except KeyError:
				continue
		return -1
	
	def contains_full_house(self, hand): #clean this up a little
		if self.contains_pair(hand) != -1 and self.contains_three_of_a_kind(hand) != -1 and self.contains_pair(hand) != self.contains_three_of_a_kind(hand):
			return 1 # Yes
		return -1

	def contains_four_of_a_kind(self, hand): 
		num_of_card = dict()
		cards = self.pile + hand.get_hand()
		for card in cards:
			try:
				num_of_card[card.get_rank()] += 1
			except KeyError:
				num_of_card[card.get_rank()] = 1
		for rank in num_of_card.keys(): # searching through k-v pairs to see if there are any of val 3. if so return it very confusing right now 
			if num_of_card[rank] == 4:
				return rank
			return -1
		
	def contains_straight_flush(self, hand):
		highest_card_in_straight = self.contains_straight(hand)
		flush_suit = self.contains_flush(hand)
		if highest_card_in_straight != -1 and flush_suit != -1:
			return highest_card_in_straight
		else:
			return -1
			
	def contains_royal_flush(self, hand):
		highest_card_in_straight = self.contains_straight(hand)
		flush_suit = self.contains_flush(hand)
		if highest_card_in_straight == 14 and flush_suit != -1:
			return highest_card_in_straight
		else:
			return -1
			
		