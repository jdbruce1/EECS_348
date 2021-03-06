import copy
import os

class Chan_Bruce_2:

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
		self.depth_limit = 5

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
		return legal

	#Places piece of opponent's color at (row,col) and then returns 
	#the best move, determined by the make_move(...) function
	def evaluation(self, player, opp):
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

		return (corner_value / 3 + parity_value / 3 + mobility_value / 3)


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

	def get_square(self, row, col):
		return self.board[row][col]

	def save(self):
		saved_val = copy.deepcopy(self.board)
		# Deep copies to have something to revert to
		self.saved.append(saved_val)

	# Restores board to the saved value
	def restore(self):
		saved_val = self.saved.pop()
		self.played.pop()
		self.board = saved_val

	def result(self,action, playerColor,oppColor):
		self.place_piece(action[0],action[1],playerColor,oppColor)

	def max_value(self,playerColor,oppColor,alpha,beta,depth):
		if(self.cutoff_test(depth)):
			return self.evaluation(playerColor,oppColor)
		v = -1000000
		for a in self.actions(playerColor,oppColor):
			self.save()
			self.result(a,playerColor,oppColor)
			v = max(v,self.min_value(playerColor,oppColor,alpha, beta, depth+1))
			self.restore()
			if v >= beta:
				return v
			alpha = max(alpha,v)
		return v

	def min_value(self,playerColor,oppColor,alpha,beta,depth):
		if(self.cutoff_test(depth)):
			return self.evaluation(playerColor,oppColor)
		v = 1000000
		for a in self.actions(oppColor,playerColor):
			self.save()
			self.result(a,oppColor,playerColor)
			v = min(v,self.max_value(playerColor,oppColor,alpha,beta, depth+1))
			self.restore()
			if v <= alpha:
				return v
			beta = min(beta,v)
		return v

	def make_move(self,playerColor,oppColor):
		best_action = None
		best_value = -1000000
		list_of_actions = self.actions(playerColor,oppColor)
		if not list_of_actions:
			return (-1,-1)
		v = self.max_value(playerColor,oppColor,-1000000,1000000,0)
		
		self.PrintBoard()
		for action in list_of_actions:
			self.save()
			self.result(action,playerColor,oppColor)
			value = self.min_value(playerColor,oppColor,-1000000,1000000,1)
			self.restore()
			if value == v:
				self.place_piece(action[0],action[1],playerColor,oppColor)
				return (action[0],action[1])