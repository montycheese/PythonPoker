from Hand import Hand

class Player(object):
	
	def __init__(self, name, is_big_blind = False, is_small_blind = False):
		self.name = name
		self.chip_amount = 100
		self.hand = None
		self.has_checked = False
		self.is_all_in = False # implement this later
		self.is_big = is_big_blind #implement later
		self.is_small = is_small_blind #implement later
		
	def is_big_blind(self):
		return self.is_big
	def is_small_blind(self):
		return self.is_small
	
	def set_blinds(self, big = False, small = False):
		self.is_big = big
		self.is_small = small
	
	def check(self): #implement this later
		self.has_checked = True
	
	def is_checked(self):
		return self.has_checked
	
	def un_check(self):
		self.has_checked = False
	
	def get_name(self):
		return self.name
	
	def set_hand(self, hand):
		self.hand = hand
	
	def get_hand(self):
		return self.hand
	
	def can_play(self):
		return self.chip_amount > 0
	
	def bet(self):
		bet = int(raw_input("Amount: "))
		while (bet > self.chip_amount or bet < 1):
			bet = raw_input("Amount must be less than %d or greater than 0: " % self.chip_amount)
		if  bet == self.chip_amount:
			print "%s going all in..." % self.name
			self.chip_amount -= bet
			self.is_all_in = True
			return bet
		else:
			self.chip_amount -= bet
			return bet
	
	def pay_blind(self, blind_size):
		if blind_size >= self.chip_amount:
			print "%s going all in..." % self.name
			chips_left = self.chip_amount
			self.chip_amount = 0
			self.is_all_in = True
			return chips_left
		else:
			self.chip_amount -= blind_size
			return blind_size
	
	def wins_money(self, amount):
		self.chip_amount += amount
	
	def get_value(self):
		return self.chip_amount