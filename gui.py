import curses
from math import *
def sign(_x):
	if _x < 0: return -1
	return 1
class univ:
	def __init__(self,n,stdscr):
		#transforming coords for ncurse which starts at top left
		self.transcoords=[-1,7,8,9,4,5,6,1,2,3]
		self.__margin=25+50
		self.__width=8
		self.__height=5
		self.__space=2
		univ_per_line=16
		x= self.__margin + ((n%univ_per_line)*(self.__width+self.__space))
		y= 0 +  ((n/univ_per_line)*(self.__height+self.__space))
		self.__win = curses.newwin(self.__height,  self.__width, y, x)
		self.stdscr=stdscr
		self.marks={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
	def draw(self,marks):
		for x in range(0,self.__height):
		    if (marks["color"]==1):
		    	self.__win.addch(x,2,curses.ACS_VLINE,curses.A_DIM)
		    	self.__win.addch(x,5,curses.ACS_VLINE,curses.A_DIM)
		    else:
		    	self.__win.addch(x,2,curses.ACS_VLINE,curses.color_pair(1))
		    	self.__win.addch(x,5,curses.ACS_VLINE,curses.color_pair(1))
		for x in range(0,self.__width):
		    if (marks["color"]==1):
		    	self.__win.addch(1,x,curses.ACS_HLINE,curses.A_DIM)
		    	self.__win.addch(3,x,curses.ACS_HLINE,curses.A_DIM)
		    else:
		    	self.__win.addch(1,x,curses.ACS_HLINE,curses.color_pair(1))
		    	self.__win.addch(3,x,curses.ACS_HLINE,curses.color_pair(1))
		for i in range(1,10,1):
		    p=self.transcoords[i]-1
		    #p=i-1
		    if(marks["color"]!=1):
		    	if(marks[i]==1):
		    		self.__win.addch(2*(p/3),3*(p %3),'X',curses.color_pair(1))
		    	elif(marks[i]==2):
		    		self.__win.addch(2*(p/3),3*(p %3),'0',curses.color_pair(1))
		    	elif(marks[i]==3):
		    		self.__win.addch(2*(p/3),3*(p %3),'@',curses.color_pair(1))
		    else:
		    	if(marks[i]==1):
		    		self.__win.addch(2*(p/3),3*(p %3),'X',curses.color_pair(0))
		    	elif(marks[i]==2):
		    		self.__win.addch(2*(p/3),3*(p %3),'0',curses.color_pair(0))
		    	elif(marks[i]==3):
		    		self.__win.addch(2*(p/3),3*(p %3),'@',curses.color_pair(0))

		self.stdscr.refresh()
		self.__win.refresh()
	def clear(self):
		self.__win.clear()
		self.stdscr.refresh()
		self.__win.refresh()
		
	#def update():


class gui:
	def __init__(self,stdscr):
		self.stdscr=stdscr
		#initialized color pair  https://docs.python.org/3.4/howto/curses.html
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
		self.width=17+2+17+2+17
		self.height=8+2+8+2+8
		self.coords={7:[3,8],8:[3,8+19],9:[3,8+2*19], \
				4:[3+10,8],5:[3+10,8+19],6:[3+10,8+2*19], \
				1:[3+2*10,8],2:[3+2*10,8+19],3:[3+2*10,8+2*19]}
		self.f=open('debug','w')
		self.f.write("%d\n" % (self.coords[4][0]))
		self.mainwin= curses.newwin(self.height,self.width,10,10);
		self.movesX={i:[0,0] for i in range(9)}
		self.movesO={i:[0,0] for i in range(9)}
		self.count=0
		self.univs = [univ(n,self.stdscr) for n in range(2**10)]
	#def copyuniv(self,index1,index2):
	#	for i in range(1,10):
	#		self.marks[index2][i]=self.marks[index1][i]
	def multiverse(self):
		#-1 denotes the boldness/color
		marks=[{"color":0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0} for n in range(2**10)]
		for i in range(self.count):
			for k in range(2**(i)):
				for j in range(1,10):
					if(marks[k][j]==3):
						marks[k]["color"]=1;
						marks[2**(i)+k]["color"]=1;
					marks[2**(i)+k][j]=marks[k][j]
				if (i % 2 ==0):
					if(marks[k][self.movesX[i][0]]!=0):
						marks[k][self.movesX[i][0]]=3
						marks[k]["color"]=1;
					else:
						marks[k][self.movesX[i][0]]=1
					if(marks[2**(i)+k][self.movesX[i][1]]!=0):
						marks[2**(i)+k][self.movesX[i][1]]=3
						marks[2**(i)+k]["color"]=1;
					else:
						marks[2**(i)+k][self.movesX[i][1]]=1
				elif(i % 2 ==1):
					if(marks[k][self.movesO[i][0]]!=0):
						marks[k][self.movesO[i][0]]=3
						marks[k]["color"]=1;
					else:
						marks[k][self.movesO[i][0]]=2
					if(marks[2**(i)+k][self.movesO[i][1]]!=0):
						marks[2**(i)+k][self.movesO[i][1]]=3
						marks[2**(i)+k]["color"]=1;
					else:
						marks[2**(i)+k][self.movesO[i][1]]=2
			#for k in range(2^i):
			#	marks[2^i+k]=marks[k]
			#	marks[k][self.movesO[i+1][0]]=2
			#	marks[2^i+k][self.movesO[i+1][1]]=2
			for j in range(2**self.count):
				#if (marks[j]["color"]!=1):
				self.univs[j].draw(marks[j])
				#else:
					#pass
					#self.univs[j].clear()
		self.drawgrid()
	def update_moves(self,playerLetter,pos1,pos2):
		if (playerLetter=='X'):
			self.movesX[self.count]=[pos1,pos2]
		elif (playerLetter=='O'):
			self.movesO[self.count]=[pos1,pos2]
		self.count=self.count+1
	def drawgrid(self):
		for y in  range(0,self.height):
			self.mainwin.addch(y,17,curses.ACS_VLINE)
			self.mainwin.addch(y,18,curses.ACS_VLINE)
			self.mainwin.addch(y,36,curses.ACS_VLINE)
			self.mainwin.addch(y,37,curses.ACS_VLINE)
		for x in  range(0,self.width):
			self.mainwin.addch(8,x,curses.ACS_HLINE)
			self.mainwin.addch(9,x,curses.ACS_HLINE)
			self.mainwin.addch(18,x,curses.ACS_HLINE)
			self.mainwin.addch(19,x,curses.ACS_HLINE)
		#self.drawX(9)
		#self.drawX(1)
		#self.drawO(5)
		self.mainwin.move(0,0)
	def update(self):
		self.stdscr.refresh()
		self.mainwin.refresh()
#http://svn.python.org/projects/python/trunk/Demo/curses/tclock.py
# draw a diagonal line using Bresenham's algorithm
	def dline(self,from_x, from_y, x2, y2):
		if curses.has_colors():
			self.stdscr.attrset(curses.color_pair(curses.COLOR_RED))
		
		dx = x2 - from_x
		dy = y2 - from_y
		
		ax = abs(dx * 2)
		ay = abs(dy * 2)
		
		sx = sign(dx)
		sy = sign(dy)
		
		x = from_x
		y = from_y
		
		if ax > ay:
			d = ay - ax // 2
		
		while True:
			self.mainwin.addch(y, x, '-')
			if x == x2:
			    return
			
			if d >= 0:
			    y += sy
			    d -= ax
			x += sx
			d += ay
		else:
			d = ax - ay // 2
			
			while True:
				self.mainwin.addch(y, x, '*')
				if y == y2:
				    return
				
				if d >= 0:
				    x += sx
				    d -= ay
				y += sy
				d += ax
	def circle(self,x,y,r):
		for theta in  range(0,360,1):
			px= int(x)+int(1.75*r*cos(radians(theta)))
			py= int(y)+int(r*sin(radians(theta)))
			self.f.write("%d,%d\n" % (px,py))
			self.mainwin.addch(py, px, '.')
	def drawX(self,n):
		centery=self.coords[n][0]
		centerx=self.coords[n][1]
		self.f.write("%d,%d\n" % (centerx,centery))
		self.dline(centerx-7,centery-3,centerx+7,centery+3)
		self.dline(centerx-7,centery+3,centerx+7,centery-3)
		
	def drawO(self,n):
		centery=self.coords[n][0]
		centerx=self.coords[n][1]
		self.circle(centerx,centery,3.5)

	def printstr(self,s):
		self.mainwin.move(27,10)
		self.mainwin.addstr(s)
		self.mainwin.move(0,0)
		self.update()
	def printmarks(self,n,s):
		if(s=='X'):
			self.drawX(n)
		elif(s=='O'):
			self.drawO(n)
		else:
			self.movebox(n)
			self.mainwin.addstr(s)
			self.update()
	def movebox(self,n):
		self.mainwin.move(self.coords[n][0]-2,self.coords[n][1]-7)
	def cls(self):
		self.mainwin.clear()
		self.drawgrid()
		

		
			
