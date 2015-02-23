#! /usr/bin/python
from Card import Card
from Deck import Deck
from Hand import Hand
from Pile import Table
from Player import Player
from ComputerPlayer import ComputerPlayer
from time import sleep

""" 
Python Poker, Texas Hold 'em v1.0 
created by Montana Wong
Playable on any Command line 
Requires python 2.xx

montanawong@gmail.com
www.github.com/montycheese
"""
DEBUG_MODE = True
SINGLE_BOT_MODE = False
PLAY_WITH_BLINDS = True
PLAYING_STYLES = ["Blinky", "Pinky", "Inky", "Clyde"]
num_players = 1

def main():
	global num_players, PLAY_WITH_BLINDS
	print "Welcome to Python Poker\nPress Enter to play"
	user_input = raw_input()
	if user_input == "":
		pass
	else:
		exit(0)
	if SINGLE_BOT_MODE: # debugging mode
		num_players = 1
	else:
		try:
			while(True):
				num_players = int(raw_input("How many players do you want to play with? (limit 5): "))
				if num_players < 1 or num_players > 5:
					print "Enter a valid input"
				else:
					break
		except:
			print "Your input was invalid, goodbye."
			exit(0)

	try:
		while(True):
			user_input = raw_input("Play with blinds? (y/n)")
			if (user_input.lower() == "y" or user_input.lower == "yes"):
				break
			elif (user_input.lower() == "n" or user_input.lower == "no"):
				PLAY_WITH_BLINDS = False
				break
			else:
				continue
	except:
		print "Your input was invalid, goodbye."
		exit(0)
	run()
	print "Thanks for playing!"

def run():
	playing = True
	won_round = True
	round = 1
	# Creating bot opponents 
	cpu_players = []
	for i in range(num_players):
		cpu = ComputerPlayer("CPU" + str(i+1), PLAYING_STYLES[0]) #Playing style
		hand = Hand()
		cpu.set_hand(hand)
		cpu_players.append(cpu)
	player = Player("User", is_big_blind = True)
	deck = Deck()
	deck.create_deck()
	hand = Hand()
	table = Table()
	
	#start game loop 
	while (player.can_play() and playing):
		print "Round: %d" % round
		deck.shuffle()
		player.set_hand(hand)
		if PLAY_WITH_BLINDS:
			table.set_player_blinds(player, cpu_players)
			for p in ([player] + cpu_players):
				if p.is_big_blind():
					blind = p.pay_blind(table.get_big_blind_size())
					table.add_bet(blind)
					print "*%s is big blind*" % str(p)
				elif p.is_small_blind():
					blind = p.pay_blind(table.get_small_blind_size())
					table.add_bet(blind)
					print "*%s is small blind*" % str(p)
			print ""
			
		deck.deal(2, player.get_hand())
		for cpu in cpu_players:
			deck.deal(2, cpu.get_hand())
			if (DEBUG_MODE):
				print "%s\'s HAND: %s" % (str(cpu), str(cpu.get_hand()))##### FOR DEBUGGING
		non_folded_cpu = cpu_players[:]
		# Hold'em rules: discard, "burn" 2 cards before the display of the flop
		for i in range(5):
			if i < 2:
				table.burn(deck.draw())
			else:
				table.push(deck.draw())
		turn = 1
		
		#condition to allow bets to continue 
		betting = True
		while turn < 4 and non_folded_cpu != []:
			print "%s:\n%s \n" % ("Flop" if turn ==1 else ("Turn" if turn ==2 else "River"), str(table))
			print "Current Hand: %s" % str(player.get_hand())
			print "Chip amount: %d" % player.get_value()
			current_bet = 0
			
			###START BETTING LOOP#####
			while(betting or not [cpu.is_checked() for cpu in non_folded_cpu]):
				ready_to_exit = True #boolean to control wheter we leave bet loop
				user_input = parse_input("Bet, Check, or Fold? (Enter B/C/F):")
				if user_input == "B":
					current_bet = player.bet()
					table.add_bet(current_bet)
				#ADD SO I CAN CHECK IF THE BET IS HIGHER THAN MY LAST
				elif user_input == "C":
					pass
				elif user_input == "F":
					betting = False
					won_round = False
				#for loop to decide cpu action
				for cpu in non_folded_cpu:
					print "%s is deciding..." % str(cpu)
					sleep(1)
					cpu_bet = cpu.bet(current_bet)
					if cpu_bet == -1:
						print "%s folds." % str(cpu)
						non_folded_cpu.remove(cpu)
					elif cpu.is_checked() and current_bet == 0:
						print "%s checks." % str(cpu)
					#there was a raise
					elif cpu_bet > current_bet:
						print "%s raises to %d." % (str(cpu), cpu_bet) 
						table.add_bet(cpu_bet)
						current_bet = cpu_bet
					elif cpu_bet == current_bet:
						print "%s matches the bet." % str(cpu)
						table.add_bet(cpu_bet)
					else:
						raise RuntimeError("Problem Occured, exiting")
						exit(0)
					print "\nCurrent Pot: %d" % table.get_value()
					#end for
					
					if non_folded_cpu == []:
						break
					#####ADD CONDITION TO EXIT OUT OF BETTING LOOP

					for cpu in non_folded_cpu:
						if cpu.get_last_bet() < current_bet:
							ready_to_exit = False

					if player.get_last_bet() < current_bet:
						ready_to_exit = False
						print "Current Bet : %d" % current_bet
					elif player.get_last_bet() > current_bet:
						raise RuntimeError("Error occured, player bet greater than current bet, should be the same or lesser in value")
						exit(0)
					if ready_to_exit:
						break
				####END BET LOOP####
			if turn != 3:
				table.burn(deck.draw())
				table.push(deck.draw())
			if non_folded_cpu != []:
				map(lambda cpu: cpu.normalize(), non_folded_cpu)
			turn += 1
			
		# Calculating who won
		player_hand_ranking = table.find_greatest_value(player.get_hand())
		print "You had a: %s" % table.get_hand_ranking(player_hand_ranking)	

		#cpu_has_highest_hand = False implement later
		#highest_hand = None
		try:
			for cpu in non_folded_cpu:
				cpu_hand_ranking = table.find_greatest_value(cpu.get_hand())
				if cpu_hand_ranking > player_hand_ranking:
					print "You lost this round, %s had a \n%s." % (str(cpu), table.get_hand_ranking(cpu_hand_ranking))
					table.distribute_winnings_to(cpu)
					won_round = False
					break # remove later
				#Now need to calculate who won based on high card of the hand
				elif cpu_hand_ranking == player_hand_ranking:
					#Even though both the player and a cpu have the same ranking hand
					#The winner can be determined based on the numerical value of the hand
					if player.get_hand().calculate_value() > cpu.get_hand().calculate_value():
						won_round = True
					#If the numerical value and rank are identical
					elif player.get_hand().calculate_value() == cpu.get_hand().calculate_value():
						print "You both had the same ranked hand. Pot is split"
						table.distribute_winnings_to(cpu, player)
						won_round = False
						break
					else:
						print "You lost this round, %s had a \n%s." % (str(cpu), table.get_hand_ranking(cpu_hand_ranking))
						table.distribute_winnings_to(cpu)
						won_round = False
						break # remove later
		#In the case that all cpu's folded 
		except IndexError:
			pass
		

		
		if won_round:
			print "Congrats, you had the strongest hand this round you won $%d worth of chips!" % table.get_value()
			table.distribute_winnings_to(player)
			
		playing = parse_input("Play again? (Y/N)")
		deck.reset()
		player.get_hand().clear()
		table.clear()
		#remove any cpu's that are out of chips and can no longer play
		for cpu in cpu_players:
			cpu.get_hand().clear()
			cpu.normalize() # reset certain instance variables to reflect new round
			if not cpu.can_play():
				print "%s is out of chips and has left the game" % str(cpu)
				cpu_players.remove(cpu)
		if cpu_players == []:
			print "You've eliminated all the other opponents"
			playing = False
			continue
		if PLAY_WITH_BLINDS: 
			table.inc_blinds(round)
		print "\n\n\n\n\n\n\n\n\n\n\n%s" % ("*"*50)
		round +=1
		############ End Round loop ##############
	#### END GAME #######

def parse_input(msg):
	print msg
	while (True):
		user_input = raw_input().upper()
		if user_input == "B":
			return "B"
		elif user_input == "C":
			return "C"
		elif user_input == "F":
			return "F"
		elif user_input == "Y":
			return True
		elif user_input == "N":
			return False
		else:
			print "Please enter a valid input\n%s" % msg

if __name__ == "__main__":
	main()
