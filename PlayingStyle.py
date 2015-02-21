import random
class PlayingStyle():
	"""
	Blinky, Pinky, Inky, Clyde 
	
	Blinky is Bad-Tempered and Bossy (most aggressive)
	Pinky is Mischievous, Persistent and Tricky (quick to make rash decisions)
	Inky is Goofy, Shy, and Unpredictable (unpredictable)
	Clyde is Ignorant and Goofy (try to make "normal" behavior)
	
	"""
	def __init__(self, type):
		self.type = type

	def __str__(self):
		return type
	
	#Determines how likely a bot is going to bet
	def get_willingness_to_bet(self):
		if self.type == "Blinky":
			return 0.75
		#pinky will have a smarter strategy that will be propagated in the betting method
		elif self.type == "Pinky":
			rand = Random()
			return 0.3
		elif self.type == "Inky":
			rand = Random()
			#will be a floating point number between 0 and 1
			return rand.random()
		elif self.type == "Clyde":
			return 0.5
		else:
			print "Undefined Style"
	
	