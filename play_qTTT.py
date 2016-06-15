from qTTT import *
import curses,gui
import cProfile
def mainloop(stdscr):
	while(True): # loop for games
		screen=gui.gui(stdscr)
		screen.update()
	        #c = stdscr.getch()
		theBoard = Board()
		mode = 'pvc' #getGameMode()
		playerLetter, player2letter = "X", "O" #inputPlayerLetter()
		#turn = whoGoesFirst()
		turn = 'player 1'
		screen.printstr('The ' + turn + ' will go first.')
		lastMark = None # needed for keeping track of the last mark in order to facilitate collapse
		rec = 2
		
		while (True): # loop for turns
	       		#if c == ord('q'):
	       		#	exit()  # Exit the while()
	       		#elif c == ord('r'):
	       		#	stdscr.refresh()
			if turn == 'player 1':
				screen.printstr("It's player 1's turn")
				# Player 1's turn.
				theBoard.printBoard(screen)
				# Check whether there is entanglement after player 2's move
				if lastMark:
					if theBoard.findCycle(lastMark.pos):
						col = getPlayerCollapse(theBoard, lastMark,screen) # let player 1 decide where to put the last mark
						theBoard.collapse(lastMark.letter, lastMark.num, col[0], col[1]) 
						theBoard.printBoard(screen)
						
		  
				# look at winning conditions:
				p1won, p1lms = theBoard.hasWon(playerLetter)
				p2won, p2lms = theBoard.hasWon(player2letter)
				if p1won:
					if p2won:
						if p1lms < p2lms:
							#screen.printstr("\n")
							theBoard.printBoard(screen)
							screen.printstr("Player 1 has won the game!")
							break
						else:
							#screen.printstr("\n")
							theBoard.printBoard(screen)
							screen.printstr("Player 2 has won the game!")
							break	   			
					else:
						#screen.printstr("\n")
						theBoard.printBoard(screen)
						screen.printstr("Player 1 has won the game!")
						break
				elif p2won:
					#screen.printstr("\n")
					theBoard.printBoard(screen)
					screen.printstr("Player 2 has won the game!")
					break
				else:
					if isBoardFull(theBoard):
					  #print("\n")
					  theBoard.printBoard(screen)
					  print("The game is a tie!")
					  break
			
				turn = "player2"
			   # if the game hasn't ended, make a move
				pos1, pos2 = getPlayerMove(theBoard,screen)
				screen.update_moves(playerLetter,pos1, pos2)
				if lastMark:
					lastMark = theBoard.addPreMark(playerLetter, lastMark.num+1, pos1, pos2)
				else:
					lastMark = theBoard.addPreMark(playerLetter, 1, pos1, pos2)
				if mode != 'pvp':
					rec = getNumRecursions(screen)
			else:      
				screen.printstr("It's player 2's turn")
				# Player 2's turn or computer.
				theBoard.printBoard(screen)
				val = None
				move = None
				if mode != 'pvp':
					if lastMark:
						[val, moves] = minimax(theBoard, rec, rec, True, player2letter, lastMark.num+1, playerLetter, lastMove = lastMark, savedMoves = [])
					else:
						[val, moves] = minimax(theBoard, rec, rec, True, player2letter, 1, playerLetter, lastMove = None, savedMoves = [])
					move = random.choice(moves)
			   # Check whether there is entanglement after player 1's move
				if lastMark:
					if theBoard.findCycle(lastMark.pos):
						if mode == 'pvp': # if player vs player
							col = getPlayerCollapse(theBoard, lastMark,screen) # let player 2 decide where to put the last mark
							theBoard.collapse(lastMark.letter, lastMark.num, col[0], col[1])
							theBoard.printBoard(screen)
						else:
							
							#col = getComputerCollapse_Random(theBoard, lastMark)
							#theBoard.collapse(lastMark.letter, lastMark.num, col[0], col[1])
							theBoard.collapse(move[0][0], move[0][1], move[0][2], move[0][3])
							theBoard.printBoard(screen)
				p1won, p1lms = theBoard.hasWon(playerLetter)
				p2won, p2lms = theBoard.hasWon(player2letter)
				if p1won:
					if p2won:
						if p1lms < p2lms:
							#screen.printstr("\n")
							theBoard.printBoard(screen)
							screen.printstr("Player 1 has won the game!")
							break
						else:
							#screen.printstr("\n")
							theBoard.printBoard(screen)
							if mode == 'pvp':
								screen.printstr("Player 2 has won the game!")
							else:
								screen.printstr("The computer has won the game!")
							break	   			
					else:
						#screen.printstr("\n")
						theBoard.printBoard(screen)
						screen.printstr("Player 1 has won the game!")
						break
				elif p2won:
					#screen.printstr("\n")
					theBoard.printBoard(screen)
					if mode == 'pvp':
						screen.printstr("Player 2 has won the game!")
					else:
						screen.printstr("The computer has won the game!")
					break	
				else:
					if isBoardFull(theBoard):
					  #print("\n")
					  theBoard.printBoard(screen)
					  print("The game is a tie!")
					  break
				turn = "player 1"
			  
			   # if the game hasn't ended, make a move
				if mode == 'pvp':
					pos1, pos2 = getPlayerMove(theBoard,screen)
					if lastMark:
						lastMark = theBoard.addPreMark(player2letter, lastMark.num+1, pos1, pos2)
						screen.update_moves(player2letter,pos1, pos2)
					else:
						lastMark = theBoard.addPreMark(player2letter, 1, pos1, pos2)
						screen.update_moves(player2letter,pos1, pos2)
				else:
					#pos1, pos2 = getComputerMove_Random(theBoard)
					lastMark = theBoard.addPreMark(move[1][0], move[1][1], move[1][2], move[1][3])
					screen.update_moves(move[1][0],move[1][2], move[1][3])
	
		if not playAgain(screen):
			break

def getPlayerMove(board,screen):
	# Let the player type in their move.
	move = ' '
	move2 = ' '
	while ((move not in '1 2 3 4 5 6 7 8 9'.split() or move2 not in '1 2 3 4 5 6 7 8 9'.split()) and move == move2) or not board.isSpaceFree(int(move)) or not board.isSpaceFree(int(move2)):
		screen.printstr('What is your next move? (1-9)')
		#move = raw_input()

		c = screen.stdscr.getch()
		if c == ord('q'):
                	exit()  # Exit the while()
                elif c == ord('r'):
               	       screen.stdscr.refresh()
		else:
			move = chr(c)
		screen.printstr('Second field? (1-9)'+str(move))
		c = screen.stdscr.getch()
		if c == ord('q'):
                	exit()  # Exit the while()
                elif c == ord('r'):
               	       stdscr.refresh()
		else:
			move2 = chr(c)
		#move2 = raw_input()
	return int(move), int(move2)
def getNumRecursions(screen):
	val = ""
	while val not in "1 2 3 4 5 6 7 8 9 10".split(" "):
		screen.printstr("How many recursions? (1-10)")
		val = chr(screen.stdscr.getch())
	return int(val)
def getPlayerCollapse(board, lastMark,screen):
    # Let the player type in their preferred collapse target
    screen.printstr("You may collapse letter {0}{1} on field {2} or {3}".format(lastMark.letter, lastMark.num, lastMark.pos, lastMark.otherpos))
    choice = None
    while (not choice or choice not in [lastMark.pos, lastMark.otherpos]):
      screen.printstr('What choice do you want to make? ({0}, {1})'.format(lastMark.pos, lastMark.otherpos))
      #choice = int(raw_input())
      choice = int(chr(screen.stdscr.getch()))
    if choice == lastMark.pos:
      return choice, lastMark.otherpos
    else:
      return choice, lastMark.pos
def playAgain(screen):
	# This function returns True if the player wants to play again, otherwise it returns False.
	screen.printstr('Do you want to play again? (y or n)')
	#return raw_input().lower().startswith('y')
	return chr(screen.stdscr.getch())


curses.wrapper(mainloop)
