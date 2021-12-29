#
# mancala.py
#
# 2021.12.26
#

def main():
	print('Running mancala.py')

	board = init_board()
	num_rounds = 0
	current_player = 'A'

	computer = input("Should computer be A or B? ")
	
	# trigger round
	# this function will recursively call itself until the game end condition is met
	play_round(board, num_rounds, current_player, computer)






# initialize the game board
def init_board():

	board = [None]*14

	# set quantity of stones to 4 in each hole
	for idx in range(14):
		board[idx] = 4

	# set quantity in each store to 0
	board[6] = 0
	board[13] = 0

	#---- test configs
	#for idx in range(14):
	#	board[idx] = 0
	
	#board[5] = 1
	#board[6] = 21
	#board[13] = 26
	#board[12] = 1

	print('\nBoard initialized')

	return board





# prints board in following format:
#       4   4   4   4   4   4   4
#   0                               0
#       4   4   4   4   4   4   4
def print_board(board):

	def get_string(qty):
		if qty < 10:
			return ' ' + str(qty)
		else:
			return str(qty)

	print('    ', get_string(board[12]), '  ', get_string(board[11]), '  ', get_string(board[10]), '  ', get_string(board[9]), '  ', get_string(board[8]), '  ', get_string(board[7]))
	print(get_string(board[13]), '                                   ', get_string(board[6]))
	print('    ', get_string(board[0]), '  ', get_string(board[1]), '  ', get_string(board[2]), '  ', get_string(board[3]), '  ', get_string(board[4]), '  ', get_string(board[5]))
	print()




# play a round
def play_round(board, num_rounds, current_player, computer):

	player_goes_again = True
	num_rounds += 1

	print('\n\n\n==========================================================\nPlaying round ', num_rounds)

	while player_goes_again == True and end_condition_met(board) == False and player_has_valid_moves(board, current_player):
		player_goes_again = get_input_and_execute_move(board, current_player, computer)

	if (end_condition_met(board) == False):
		if current_player == 'A':
			current_player = 'B'
		else:
			current_player = 'A'
		play_round(board, num_rounds, current_player, computer)
	else:
		print('\nGame over. End state:')
		print_board(board)
	


def player_has_valid_moves(board, current_player):
	options = [0,1,2,3,4,5] if current_player == 'A' else [7,8,9,10,11,12]
	for idx in options:
		if is_legal_move(board, current_player, idx):
			print('Player ', current_player, ' has a valid move')
			return True
	print('Player ', current_player, ' has no valid moves')
	return False


def get_input_and_execute_move(board, current_player, computer):
	msg = '\n\nPlayer ' + current_player
	if (current_player == computer):
		msg += ' (computer)'
	msg += ' to move'
	print(msg)
	print('Current board:')
	print_board(board)
	if current_player == computer:
		idx = get_computer_input(board, current_player)
		print('\n--------> computer chose ', idx)
	else:
		idx = get_input(board, current_player)

	return execute_move(board, current_player, idx, False)



# gets start hole index from user
# checks to make sure idx chosen is valid, and prompts again if it's not
# (e.g. can't be 6 or 13 since those are the pots, and needs to have
# at least one stone)
# TODO - error handling for non-integer input
def get_input(board, current_player):

	idx = 0
	move_legal = False

	while move_legal == False:
		idx = input("Choose a hole: ")
		if idx == 'exit':
			exit()
		idx = int(idx)
		if (is_legal_move(board, current_player, idx)):
			move_legal = True
		else:
			print('Invalid start hole\n')

	return idx




# a legal move must be for a hole that has at least one stone
# on the current player's side of the board
# and cannot be the "store" holes (idx 6 and 13)
def is_legal_move(board, current_player, idx):
	if current_player == 'A':
		return idx < 6 and board[idx] > 0
	else:
		return 6 < idx < 13 and board[idx] > 0





def execute_move(board, current_player, idx, is_test):
	player_goes_again = False

	# player "picks up" stones at selected start idx
	qty_in_hand = board[idx]
	board[idx] = 0

	while qty_in_hand > 0:

		# get idx of next hole. This is generally just the next hole, except
		# we need to make sure each player skips the opponents hole
		if idx == 12:
			if current_player == 'A':
				#print('Skipping left store (13) cause we player A')
				idx = 0
			else:
				idx = 13
		elif idx == 13:
			idx = 0
		elif idx == 5 and current_player == 'B':
			#print('Skipping right store (6) cause we player B')
			idx += 2
		else:
			idx += 1

		#print('idx is now: ', idx)

		# player "drops" stone in next hole
		qty_in_hand -= 1
		board[idx] += 1

		if qty_in_hand == 0:
			# if player dropped last stone in their store, they go again
			if (current_player == 'A' and idx == 6) or (current_player == 'B' and idx == 13):
				if is_test == False:
					print('Dropped last stone in store, player can go again')
				player_goes_again = True
			# if player dropped last stone in a hole with other stones,
			# we pick them all up and continue
			elif board[idx] > 1:
				if is_test == False:
					print('Last stone dropped on idx ', idx, ' which has ', board[idx], ' stones, will continue')
				qty_in_hand = board[idx]
				board[idx] = 0
			else:
				print()
				if is_test == False:
					print('Dropped last stone in reglar hole, round will end')

	return player_goes_again




# when the total of stones in both stores equals 48
# (the total number of stones), the game is over
def end_condition_met(board):
	return board[6] + board[13] == 48



def get_computer_input(board, current_player):

	print('running get_computer_input')

	# todo - the below three ifs can be generalized into an algo
	if current_player == 'A' and board[5] == 1:
		return 5
	elif current_player == 'B' and board[12] == 1:
		return 12

	if current_player == 'A' and board[4] == 2:
		return 4
	elif current_player == 'B' and board[11] == 2:
		return 11

	if current_player == 'A' and board[3] == 3:
		return 3
	elif current_player == 'B' and board[10] == 3:
		return 10

	results = []

	for idx in [0,2,3,4,5,7,8,9,10,11,12]:
		if is_legal_move(board, current_player, idx):
			board_copy = board.copy()
			player_goes_again = execute_move(board_copy, current_player, idx, True)
			store_idx = 6 if current_player == 'A' else 13
			res = {
				"idx": idx,
				"store_quantity": board_copy[store_idx],
				"player_goes_again": player_goes_again
			}
			results.append(res)

	results = sorted(results, key = lambda i: (i['store_quantity'], i['player_goes_again']), reverse = True)

	print('computer move results:')
	print(results)

	#print('\nComputer chooses idx ', results[0]['idx'])

	return results[0]['idx']




# run the game
main()








