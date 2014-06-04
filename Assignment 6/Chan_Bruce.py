
class Chan_Bruce:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.occuipied = []
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		self.occuipied.extend(([4, 4], [3, 4], [3, 3], [4, 3]))
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
		self.played = [[3,4],[3,3],[4,4],[4,3]]
		self.depth_limit = 10
		self.num_open = 60

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
		self.played.append([row,col])


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


	def evaluation(self,playerColor,oppColor):
		player_count = 0
		opponent_count = 0
		for r in range(self.size):
			for c in range(self.size):
				val = self.board[r][c]
				if(val == playerColor):
					player_count = player_count + 1
				else:
					if(val == oppColor):
						opponent_count = opponent_count + 1
		return player_count - opponent_count

	def cutoff_test(self,depth):
		if depth >= self.depth_limit:
			return True
		else:
			if num_open == 0:
				return True
		return False


	def play_square(self, row, col, playerColor, oppColor):		
		# Place a piece of the opponent's color at (row,col)
		if (row,col) != (-1,-1):
			self.place_piece(row,col,oppColor,playerColor)
		
		# Determine best move and and return value to Matchmaker
		print ("Evaluation function for " + playerColor + " is " + str(self.evaluation(playerColor,oppColor)))
		print ("Played pieces are " + str(self.played))
		print ("Number of squares left is " + str(self.num_open))
		return self.make_move(playerColor, oppColor)

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
	def flip_tiles(self, row, col, Dir, dist, player):

		for i in range(dist):
			self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
		return True
	
#returns the value of a square on the board
	def get_square(self, row, col):
		return self.board[row][col]


	def save(self):
		saved_val = self.deepcopy()
		# Deep copies to have something to revert to
		return saved_val

	def restore(self,saved):
		self = saved

		# Restores board to the saved value

	def result(self,action, playerColor,oppColor):
		self.place_piece(action[1],action[2],playerColor,oppColor)



	def max_value(this,playerColor,oppColor):
		if(self.cutoff_test(depth)):
			return self.evaluation(playerColor,oppColor)
		v = -100
		saved = self.save()
		for a in self.actions(playerColor,oppColor):		# Watch syntax here
			result(a,playerColor,oppColor)
			v = max(v,this.min_value(playerColor,oppColor))
			self.restore(saved)
		return v

	def min_value(this,playerColor,oppColor):
		if(self.cutoff_test(depth)):
			return self.evaluation(playerColor,oppColor)
		v = 100
		saved = self.save()
		for a in self.actions(oppColor,playerColor):
			result(a,oppColor,playerColor)
			v = min(v,max_value(oppColor,playerColor))
			self.restore(saved)
		return v


	def minimax_decision(this,playerColor,oppColor):
		# I think this will be different



#Search the game board for a legal move, and play the first one it finds
	def make_move(self, playerColor, oppColor):
		for row in range(self.size):
			for col in range(self.size):
				if(self.islegal(row,col,playerColor, oppColor)):
					for Dir in self.directions:
						#look across the length of the board to see if the neighboring squares are empty,
						#held by the player, or held by the opponent
						for i in range(self.size):
							if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
								#does the adjacent square in direction dir belong to the opponent?
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= oppColor and i==1 : # no
									#no pieces will be flipped in this direction, so skip it
									break
								#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
								#of opponent pieces
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
									break

								#with one of player's pieces at the other end
								if self.get_square(row+ i*Dir[0], col + i*Dir[1])==playerColor and i!=0 and i!=1 :
									#set a flag so we know that the move was legal
									legal = True
									self.flip_tiles(row, col, Dir, i, playerColor)
									break
					self.played.append([row,col])
					self.num_open = self.num_open - 1				
					return (row,col)
		return (-1,-1)
			
	def actions(self, player, opp):
		actions = []
		for square in self.occuipied:
			print(square)
			row = square[0]
			col = square[1]

			for c in range(col - 1, col + 2):
				for r in range(row - 1, row + 2):
					if r >= 0 and c >= 0 and r < self.size and c < self.size:
						if self.board[r][c] == " " and self.islegal(row,col,player, opp):
							adjacentSquares.append([r, c])

		return actions

cb = Chan_Bruce()
print(str(cb.actions('B', 'W')))