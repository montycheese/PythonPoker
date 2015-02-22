from Hand import Hand
from PlayingStyle import PlayingStyle
from Player import Player
from math import ceil
import random

class ComputerPlayer(Player):

	def __init__(self, name, playing_style, is_big_blind = False, is_small_blind = False):
		super(ComputerPlayer, self).__init__(name, is_big_blind = False, is_small_blind = False)
		self.playing_style = PlayingStyle(playing_style)
	
	def normalize():
		self.last_bet = -1
	
	#later implement a restriction on minimum bet based on blind size
	def bet(self, bet_size):
		if str(self.playing_style) == "Blinky":
			return self.decide_blinkys_bet(bet_size)
		elif str(self.playing_style) == "Pinky":
			return self.decide_pinkys_bet(bet_size)
		elif str(self.playing_style) == "Inky":
			return self.decide_inkys_bet(bet_size)
		elif str(self.playing_style) == "Clyde":
			return self.decide_clyde_bet(bet_size)

	
	#Blinky match bets until he is forced to go all in, then there is a % chance he will go all in
	def decide_blinkys_bet(self, bet_size):
		rand = random
		if bet_size == 0:
			if rand.random() >= 0.5 or self.chip_amount < 2:
				return 0
			else:
				bet = int(ceil((self.chip_amount * 0.1)))
				self.chip_amount -= bet
				self.last_bet = bet
				return bet
		if self.chip_amount > bet_size:
			if rand.random() >= 0.5:
				self.chip_amount -=bet_size
				self.last_bet = bet_size
				return bet_size
			else:
				bet =  bet_size + int(((self.chip_amount + bet_size)/2))
				self.chip_amount -= bet
				self.last_bet = bet
				return bet
		elif self.chip_amount <= bet_size:
			if self.playing_style.get_willingness_to_bet() >= rand.random():
				bet = self.chip_amount
				self.chip_amount = 0
				is_all_in = True
				self.last_bet = bet
				return bet
			#Fold
			else:
				return -1 
		else:
			raise RuntimeError("Shouldnt happen!")
			return 0
	
	
			
			
		