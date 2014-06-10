import copy
import os

class Chan_Bruce:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
		self.played = [[3,4],[3,3],[4,4],[4,3]]
		self.depth_limit = 4
		self.num_open = 60
		self.saved = []

#prints the boards
	def PrintBoard(self):

		# Print column numbers
		print("  ",end="")
		for i in range(self.size):
			print(i+1,end=" ")
		print()

		# Build horizontal separator
		linestr = " " + ("+-" * self.size) + "+"

		# Print board
		for i in range(self.size):
			print(linestr)					   # Separator
			print(i+1,end="|")				   # Row number
			for j in range(self.size):
				print(self.board[i][j],end="|")  # board[i][j] and pipe separator 
			print()							  # End line
		print(linestr)

#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.	
	def islegal(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		for Dir in self.directions:
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						return True
		return False
		
#returns true if the square was played, false if the move is not allowed
	def place_piece(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		
		self.num_open = self.num_open - 1;


		if(player == opp):
			print("player and opponent cannot be the same")
			return False
		
		legal = False
		#for each direction, check to see if the move is legal by seeing if the adjacent square
		#in that direction is occuipied by the opponent. If it isnt check the next direction.
		#if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
		#if the chain of opponents pieces is flanked on both ends by the players pieces, flip
		#the opponents pieces 
		for Dir in self.directions:
			#look across the length of the board to see if the neighboring squares are empty,
			#held by the player, or held by the opponent
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						legal = True
						self.flip_tiles(row, col, Dir, i, player)
						break
		self.played.append([row,col])
		# print(self.played)

		return legal

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
	
# Don't think we need the utility function

	# def utility(self, player):
	# 	player_count = 0
	# 	opponent_count = 0
	# 	for r in range(self.size):
	# 		for c in range(self.size):
	# 			if(player = self.board[r][c]):
	# 				player_count = player_count + 1
	# 			else:
	# 				opponent_count = opponent_count + 1
	# 	if(player_count = opponent_count):
	# 		return 0
	# 	if(player_count > opponent_count):
	# 		return 1
	# 	if(player_count < opponent_count):
	# 		return -1

	def tile_parity(self, player, opp):
		opp_count = 0
		player_count = 0

		opp_corner_count = 0
		player_corner_count = 0

		for row in range(self.size):
			for col in range(self.size):
				if self.board[row][col] == opp:
					opp_count = opp_count + 1
				elif self.board[row][col] == player:
					player_count = player_count + 1

				if((row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col ==7)):
					if self.board[row][col] == opp:
						opp_corner_count = opp_corner_count + 1
					elif self.board[row][col] == player:
						player_corner_count = player_corner_count + 1

		if player_corner_count + opp_corner_count != 0:
			corner_value = 100 * (player_corner_count - opp_corner_count) / (player_corner_count + opp_corner_count)
		else:
			corner_value = 0

		parity_value = 100 * (player_count - opp_count) / (player_count + opp_count)
		mobility_value = self.mobility(player, opp)

		return (corner_value * 2 + parity_value / 4 + mobility_value / 4)


	def mobility(self, player, opp):
		player_move_count = len(self.actions(player, opp))
		opp_move_count = len(self.actions(opp, player))

		if (player_move_count + opp_move_count) != 0:
			return 100 * (player_move_count - opp_move_count) / (player_move_count + opp_move_count)
		else:
			return 0

	def increment(self,player_count,playerColor,oppColor,r,c,amt):
		val = self.board[r][c]
		if(val == playerColor):
			player_count = player_count + amt
		else:
			if(val == oppColor):
				player_count = player_count - amt
		return player_count

	def evaluation(self,playerColor,oppColor):
		return self.tile_parity(playerColor, oppColor)
		# player_count = 0
		# for r in range(self.size):
		# 	for c in range(self.size):
		# 		if(r == 0 or r == 7 or c == 0 or c ==7):
		# 			if((r == 0 and c == 0) or (r == 0 and c == 7) or (r == 7 and c == 0) or (r == 7 and c ==7)):
		# 				player_count = self.increment(player_count,playerColor,oppColor,r,c,10)		# Corner = 10
		# 			else:
		# 				player_count = self.increment(player_count,playerColor,oppColor,r,c,2)
		# 		else:
		# 			player_count = self.increment(player_count,playerColor,oppColor,r,c,1)
		# return player_count

	def cutoff_test(self,depth):
		if depth >= self.depth_limit:
			return True
		else:
			if self.num_open == 0:
				return True
		return False


	def play_square(self, row, col, playerColor, oppColor):		
		# Place a piece of the opponent's color at (row,col)
		if (row,col) != (-1,-1):
			self.place_piece(row,col,oppColor,playerColor)
		
		# Determine best move and and return value to Matchmaker
		# print("Evaluation function for " + playerColor + " is " + str(self.evaluation(playerColor,oppColor)))
		# print("Played pieces are " + str(self.played))
		# print("Number of squares left is " + str(self.num_open))
		return self.make_move(playerColor, oppColor)

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
	def flip_tiles(self, row, col, Dir, dist, player):

		for i in range(dist):
			self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
		return True

	def actions(self, playerColor, oppColor):
		actions = []
		for row in range(self.size):
			for col in range(self.size):
				if self.islegal(row,col,playerColor,oppColor):
					actions.append([row,col])
		return actions

		# Simple actions function. Greg was working on a more complicated one:
	# def actions(self, player, opp):
	# 	start = os.times().elapsed
	# 	actions = []
	# 	checked = []
	# 	for square in self.played:
	# 		# print(square)
	# 		row = square[0]
	# 		col = square[1]

	# 		for c in range(col - 1, col + 2):
	# 			for r in range(row - 1, row + 2):
	# 				if r == row and c == col:
	# 					continue
	# 				key = str(r) + "," + str(c)
	# 				if r >= 0 and c >= 0 and r < self.size and c < self.size:
	# 					if self.board[r][c] == " " and self.islegal(r,c,player,opp) and not key in checked:
	# 						actions.append([r, c])
	# 					checked.append(key)
	# 	end = os.times().elapsed
	# 	print(str(end - start))
	# 	return actions

	def get_square(self, row, col):
		return self.board[row][col]


	# def save(self):
	# 	start = os.times().elapsed
	# 	saved_val = copy.deepcopy(self)
	# 	# Deep copies to have something to revert to
	# 	self.saved.append(saved_val)
	# 	end = os.times().elapsed
	# 	print(str(end-start))

	def save(self):
		# start = os.times().elapsed
		saved_val = copy.deepcopy(self.board)
		# Deep copies to have something to revert to
		self.saved.append(saved_val)
		# end = os.times().elapsed
		# print(str(end-start))

	def restore(self):
		saved_val = self.saved.pop()
		self.played.pop()
		# print("This is the board that will be restored")
		# saved_val.PrintBoard()
		self.board = saved_val
		# print("Right after restoration")
		# self.PrintBoard()

	# def restore(self):
	# 	saved_val = self.saved.pop()
	# 	# print("This is the board that will be restored")
	# 	# saved_val.PrintBoard()
	# 	self.board = saved_val.board
	# 	# print("Right after restoration")
	# 	# self.PrintBoard()

		# Restores board to the saved value

	def result(self,action, playerColor,oppColor):
		self.place_piece(action[0],action[1],playerColor,oppColor)



	def max_value(self,playerColor,oppColor,alpha,beta,depth):
		# print("Entering max_value")
		if(self.cutoff_test(depth)):
			# print("Evaluation value for this board is " + str(self.evaluation(playerColor,oppColor)))
			return self.evaluation(playerColor,oppColor)
		v = -1000000
		for a in self.actions(playerColor,oppColor):
			self.save()
			# print("Saved board is: ")
			# self.saved[len(self.saved) - 1].PrintBoard()
			# print("Setting the result of " + str(a) + " for player " + playerColor)
			self.result(a,playerColor,oppColor)
			# self.PrintBoard()
			# print("Recursively calling min_value")
			v = max(v,self.min_value(playerColor,oppColor,alpha, beta, depth+1))
			# self.PrintBoard()
			# print("Restoring board")
			self.restore()
			# self.PrintBoard()
			if v >= beta:
				# print("v = " + str(v) + " which is greater than or equal to beta (" + str(beta) + "). This is getting pruned.")
				return v
			alpha = max(alpha,v)
		# print("Returning from max_value to caller with v = " + str(v))
		return v

	def min_value(self,playerColor,oppColor,alpha,beta,depth):
		# print("Entering min_value")
		if(self.cutoff_test(depth)):
			# print("Evaluation value for this board is " + str(self.evaluation(playerColor,oppColor)))
			return self.evaluation(playerColor,oppColor)
		v = 1000000
		for a in self.actions(oppColor,playerColor):
			self.save()
			# print("Saved board is: ")
			# self.saved[len(self.saved) - 1].PrintBoard()
			# print("Setting the result of " + str(a) + " for player " + oppColor)
			self.result(a,oppColor,playerColor)
			# self.PrintBoard()
			# print("Recursively calling max_value")
			v = min(v,self.max_value(playerColor,oppColor,alpha,beta, depth+1))
			# self.PrintBoard()
			# print("Restoring board")
			self.restore()
			# self.PrintBoard()
			if v <= alpha:
				# print("v = " + str(v) + " which is less than or equal to beta (" + str(alpha) + "). This is getting pruned.")
				return v
			beta = min(beta,v)
		# print("Returning from min_value to caller with v = " + str(v))
		return v


	def make_move(self,playerColor,oppColor):
		best_action = None
		best_value = -1000000
		list_of_actions = self.actions(playerColor,oppColor)
		if not list_of_actions:
			return (-1,-1)
		v = self.max_value(playerColor,oppColor,-1000000,1000000,0)
		# print("Optimal value of " + str(v)+ " decided on.")
		self.PrintBoard()
		for action in list_of_actions:
			# print("Seeing if " + str(action) + " matches the value of " + str(v))
			self.save()
			self.result(action,playerColor,oppColor)
			value = self.min_value(playerColor,oppColor,-1000000,1000000,1)
			self.restore()
			if value == v:
				# print("The action " + str(action) + " matches the value of " + str(v) + " so that's what we'll play")
				self.place_piece(action[0],action[1],playerColor,oppColor)
				return (action[0],action[1])

#Search the game board for a legal move, and play the first one it finds
	# def make_move(self, playerColor, oppColor):
	# 	for row in range(self.size):
	# 		for col in range(self.size):
	# 			if(self.islegal(row,col,playerColor, oppColor)):
	# 				for Dir in self.directions:
	# 					#look across the length of the board to see if the neighboring squares are empty,
	# 					#held by the player, or held by the opponent
	# 					for i in range(self.size):
	# 						if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
	# 							#does the adjacent square in direction dir belong to the opponent?
	# 							if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= oppColor and i==1 : # no
	# 								#no pieces will be flipped in this direction, so skip it
	# 								break
	# 							#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
	# 							#of opponent pieces
	# 							if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
	# 								break

	# 							#with one of player's pieces at the other end
	# 							if self.get_square(row+ i*Dir[0], col + i*Dir[1])==playerColor and i!=0 and i!=1 :
	# 								#set a flag so we know that the move was legal
	# 								legal = True
	# 								self.flip_tiles(row, col, Dir, i, playerColor)
	# 								break
	# 				self.played.append([row,col])
	# 				self.num_open = self.num_open - 1				
	# 				return (row,col)
	# 	return (-1,-1)
			


# cb = Chan_Bruce()
# print(cb.actions('B', 'W'))
# cb.PrintBoard()






