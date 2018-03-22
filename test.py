#Rabids Uno

# Authors: 
# John Lee - hyunmail94@csu.fullerton.edu
# Andre Victoria - andreappstuff@csu.fullerton.edu

import pygame
from pygame.locals import *
from sys import exit
from random import randint
from time import time

#setup
pygame.init()
pygame.display.set_caption("Uno Rabbids")

#game rules config
bonus_time_limit = 3500

#background/overlay image
image = pygame.image.load("background_" + str(randint(1,10)) + ".jpg")
screen = pygame.display.set_mode(image.get_rect().size)
w, h = pygame.display.get_surface().get_size()
SURF_BACKGROUND = image.convert()
overlay = pygame.image.load("BorderOverlay.png").convert_alpha()

#deck images
deckImage1 = pygame.image.load("Deck_1.png").convert_alpha()
deckImage2 = pygame.image.load("Deck_2.png").convert_alpha()
deckImage3 = pygame.image.load("Deck_3.png").convert_alpha()
deckImage4 = pygame.image.load("Deck_4.png").convert_alpha()

#music
pygame.mixer.music.load("Music/music_" + str(randint(1,3)) + ".mp3")
pygame.mixer.music.play(-1)

def MAX(left,right):
	return left if (left>right) else right

#card class
class Card:
	color = 0
	suite = 0
	name = ""
	image_back = None
	rotation = 0
	def __init__(self, color, suite, name):
		self.color = color
		self.suite = suite
		if name is None:
			self.name = "card_" + str(color) + "_" + str(suite)
		else:
			self.name = name
		self.image = pygame.image.load("Cards/" + self.name + ".png")
		self.rect = None
		self.image_back = pygame.image.load("Cards/card_back.png")
		#self.image_back = pygame.transform.rotate(self.image_back,180)
	# def is_valid(self,left = Card,right):
	# 	#if(left.card)
	# 	return True;

	def change_type(self,color,suite):
		#TODO: Add Type changing functionality for the wildcard.
		self.color = color
		self.suite = suite
		self.name = "card_" + str(color) + "_" + str(suite)
		self.image = pygame.image.load("Cards/" + self.name + ".png")

	def get_color(self):
		return self.color

	def get_suite(self):
		return self.suite


def SHUFFLEDECK():
	#shuffle deck.
	for i in range(len(deck)):
		for j in range(0,5):
			tmp = deck[i]
			rnd = randint(18,36)
			if(randint(0,50) > 50):
				rnd *= -1;
			deck[i] = deck[(i+rnd)%len(deck)]
			deck[(i+rnd)%len(deck)] = tmp

def cards_init():
	global deck, pile
	global currentCard

	deck = []
	pile = []

	#populate deck with 2 copies of each standard card.
	for i in range(1,5):
		for j in range(1,10):
			deck.append(Card(i,j,None));
			deck.append(Card(i,j,None));

	#set a standard card to the center.
	currentCard = deck[randint(0,len(deck)-1)]
	currentCard.rotation = randint(180,270)
	pile.append(currentCard)
	deck.remove(currentCard)	

	#append special cards to the deck.
	#2 of each +x card for each color.
	for i in range(1,5):
		deck.append(Card(i,-i,"special_" + str(i)))
		deck.append(Card(i,-i,"special_" + str(i)))

		#1 wildcard per color
		deck.append(Card(-1,0,"wildcard"))

	SHUFFLEDECK()
	print("DECKLIST: ")
	for i in range(len(deck)):
		print("Card" + str(i) + ": " +deck[i].name)

#restarts the game
def restart_game():
	global whose_turn, player1, player2, winner

	winner = None			#reset winner (needed if game ended)
	cards_init()			#reset deck and pile
	whose_turn = player1	#start with player1

	#reset player values (except for Player.opponent)
	player1.restart_player()
	player2.restart_player()

	#visualize changes
	reblit_all_cards()
	pygame.display.update()
	pygame.time.wait(20)

	#draw 5 cards for each
	player1.draw_card(5)
	player2.draw_card(5)

#player class
class Player:
	def __init__(self, name, isHidden,sound_normal,sound_invalid,sound_special1,sound_special2,sound_special3,sound_wildcard,sound_draw,sound_changeTurn,sound_bonus,sound_loss,sound_victory):
		self.name = name
		self.isHidden = isHidden;
		self.sound_normal = effect = pygame.mixer.Sound(sound_normal)
		self.sound_invalid = pygame.mixer.Sound(sound_invalid)
		self.sound_special1 = pygame.mixer.Sound(sound_special1)
		self.sound_special2 = pygame.mixer.Sound(sound_special2)
		self.sound_special3 = pygame.mixer.Sound(sound_special3)
		self.sound_wildcard = pygame.mixer.Sound(sound_wildcard)
		self.sound_draw = pygame.mixer.Sound(sound_draw)
		self.sound_changeTurn = pygame.mixer.Sound(sound_changeTurn)
		self.sound_bonus = pygame.mixer.Sound(sound_bonus)
		self.sound_loss = pygame.mixer.Sound(sound_loss)
		self.sound_victory = pygame.mixer.Sound(sound_victory)
		self.hand = []
		self.wildcard = None
		self.opponent = None
		self.cardCount = 0
		self.bonus = 0
		self.lastCardTime = pygame.time.get_ticks()
		self.got_wildcard = False
		if isHidden:
			self.cardY = -.13
		else:
			self.cardY = .75

	#for restarting the game
	def restart_player(self):
		self.hand = []
		self.wildcard = None
		self.cardCount = 0
		self.bonus = 0
		self.lastCardTime = pygame.time.get_ticks()
		self.got_wildcard = False


	def check_hover(self,x,y):
		#print ("hovering");
		found = False
		for i in reversed(range(len(self.hand))):
			if x >= self.hand[i].rect.x and (x<=self.hand[i].rect.x+self.hand[i].image.get_width()):
			    x_inside = True
			else: x_inside = False
			if y >= self.hand[i].rect.y and (y<=self.hand[i].rect.y+self.hand[i].image.get_height()*2):
			    y_inside = True
			else: y_inside = False
			if x_inside and y_inside and found == False:
				found = True
				self.hand[i].rect.y = h * .55
			else: self.hand[i].rect.y = h * self.cardY

	def check_click(self,x,y):
		for i in reversed(range(len(self.hand))):
			if self.hand[i].rect.collidepoint(x, y):
				global currentCard 
				global whose_turn
				if (self.hand[i].color == currentCard.color or
					self.hand[i].suite == currentCard.suite or
					self.hand[i].color == -1) and whose_turn == self:
					currentCard = self.hand[i]
					currentCard.rotation = randint(90,270)
					
					print (self.name + " Played " + currentCard.name);
					self.sound_normal.play()
					self.wildcard = None
					self.cardCount -= 1
					print ("count: " + str(self.cardCount))
					if currentCard.name == "wildcard":
						self.wildcard = currentCard;

						self.hand.remove(currentCard)
						pile.append(currentCard)

						if len(self.hand) > 0:
							currentCard = Card(MAX(1,self.hand[randint(0,len(self.hand)-1)].color),randint(1,9),None)
						else:
							currentCard = Card(randint(1,4),randint(1,9),None)
						self.sound_wildcard.play()

						print ("Wildcard created " + currentCard.name)

						
						pile.append(currentCard)
						# whose_turn = self.opponent
						# self.opponent.sound_changeTurn.play()
					elif currentCard.name == "special_1":
						print("Special!!! Opponent Draws 2 cards!")
						self.sound_special1.play()
						self.opponent.sound_loss.play()
						self.hand.remove(currentCard)
						pile.append(currentCard)

						
						self.opponent.draw_card(1)
						
						self.opponent.draw_card(1)

						whose_turn = self.opponent
						#self.opponent.sound_changeTurn.play()
					elif currentCard.name == "special_2":
						print("Special!!! Opponent Draws 4 cards!")
						self.sound_special2.play()
						self.opponent.sound_loss.play()
						self.hand.remove(currentCard)
						pile.append(currentCard)

						
						self.opponent.draw_card(1)
						
						self.opponent.draw_card(1)
						
						self.opponent.draw_card(1)
						
						self.opponent.draw_card(1)

						whose_turn = self.opponent
						#self.opponent.sound_changeTurn.play()
					elif currentCard.name == "special_3":
						#opponent 
						self.sound_special3.play()
						self.opponent.sound_loss.play()
						self.hand.remove(currentCard)
						pile.append(currentCard)

						oldcardCount = self.cardCount

						while (len(self.hand) > 0):
							deck.append(self.hand[0])
							self.hand.remove(self.hand[0])
						SHUFFLEDECK()

						for i in range(self.cardCount):
							self.draw_card(1)
							
						self.cardCount = oldcardCount

						whose_turn = self.opponent
						#self.opponent.sound_changeTurn.play()
					elif currentCard.name == "special_4":
						self.hand.remove(currentCard)
						pile.append(currentCard)
						self.sound_special1.play()
						self.opponent.sound_loss.play()
					else:
						self.hand.remove(currentCard)
						pile.append(currentCard)
						whose_turn = self.opponent
						if len(self.hand) > 0:
							self.opponent.sound_changeTurn.play()

					if pygame.time.get_ticks() - self.lastCardTime < bonus_time_limit:
						self.bonus += 1
					else:
						self.bonus = 0

					global player1
					if(self == player1):
						print ( "current time: " + str(pygame.time.get_ticks()))
						print ( "my time: " + str(self.lastCardTime))
						print ( "Time since last card played: " + str(pygame.time.get_ticks() - self.lastCardTime ) )
						print ( "Bonus: " + str(self.bonus))


					if self.bonus > 1 and len(self.hand) > 0 and self.wildcard == None:
						self.got_wildcard = True
						print ( "Drew wildcard!")
						newCard = Card(-1,0,"wildcard")
						if self.isHidden:
							newCard.image = pygame.transform.rotate(newCard.image,180)
						newCard.rect = newCard.image.get_rect()
						newCard.rect.y = h * self.cardY
						self.hand.insert(0, newCard)
						self.bonus = 0
						self.cardCount += 1
						self.sound_bonus.play()
					self.opponent.lastCardTime = pygame.time.get_ticks()
					break
					
					print ( whose_turn.name + "'s turn")
				else:
					print ("invalid card")
					self.sound_invalid.play()

	#pausing time so player can visualize whats happening
	def time_stop(self, delay_val):

		#update and display everything
		reblit_all_cards()
		pygame.display.update()

		#stop time (also 'stop' the quickplay bonus timer)
		#pygame.time.wait(delay_val)
		self.lastCardTime += delay_val


	def redraw_hand(self):
		minx = .23
		maxx = .62
		starty = .75
		startx = .4
		interval = .09;#(.5) / (MAX(len(self.hand),1))
		if(interval * (len(self.hand)-1) > (maxx-minx)):
			interval *= (maxx-minx) / (interval * (len(self.hand)-1))
		startx -= (interval/2) * (len(self.hand)-1);
		
		for i in range(len(self.hand)):
			self.hand[i].rect.x = w * startx
			screen.blit(self.hand[i].image_back if self.isHidden else self.hand[i].image, (w * startx,self.hand[i].rect.y))
			startx += interval

		if self.wildcard != None:
			screen.blit(self.wildcard.image, (w * 0,h * self.cardY))
			#old: screen.blit(self.hand[i].image_back if self.isHidden else self.wildcard.image, (w * 0,h * self.cardY))

	def draw_card(self,count):
		for i in range(count):
			if self.isHidden:
				deck[i].image_back = pygame.transform.rotate(deck[i].image_back,180)
			
			deck[i].rect = deck[i].image.get_rect()
			deck[i].rect.y = h * self.cardY
			
			print ("drew " + deck[i].name)
			self.hand.append(deck[i])
			deck.remove(deck[i])
			self.cardCount += 1
		
		self.redraw_hand()
			
		print (str(len(deck)) + " cards in deck, " + self.name + " has " + str(len(self.hand)) + " cards in hand.")
		#TODO: If no more cards in deck, and neither player has won, declare the game a tie.

	def get_hand(self):
		return self.hand

	def get_name(self):
		return self.name

	def make_move(self, card_num):
		print ("picked " + card_num)
		self.hand.remove(card_num)

#-----------UI-----------
myfont = pygame.font.SysFont('Comic Sans MS', 30)
mouse_posx, mouse_posy = pygame.mouse.get_pos() 	#saves the mouse position since last movement

#Draws a rectangle bar on screen that fills up before bonus time is up. accepts w and h floats (0.00 -> 1.00)
def quickplay_bar_UI(percent_w, percent_h):
	global winner
	#background bar
	pygame.draw.rect(screen, (0,0,0), (w*(percent_w - 0.020),h * (percent_h - 0.038),154,54))
	time_limit = bonus_time_limit

	#changing the bar
	bar_fill_color = (150,84,79)
	if (winner != None):
		quickplay_text = myfont.render('   WINS!', False, (255, 255, 255))
		pygame.draw.rect(screen, (25,25,25), (w*(percent_w - 0.018),h * (percent_h - 0.035), 150,50))
		screen.blit(quickplay_text,(w * percent_w,h * percent_h))
	else:
		if (whose_turn == player1):
			player1.got_wildcard = False
			if ((pygame.time.get_ticks() - player1.lastCardTime) >= time_limit):
				#player didnt make move in time
				quickplay_text = myfont.render('Too slow :(', False, (255, 255, 255))
				pygame.draw.rect(screen, (25,25,25), (w*(percent_w - 0.018),h * (percent_h - 0.035), 150,50))
				screen.blit(quickplay_text,(w * percent_w,h * percent_h))
			else:
				#fill up the bar
				time_left = round((time_limit - (pygame.time.get_ticks() - player1.lastCardTime)) / 1000, 1)
				quickplay_text = myfont.render('Time left: ' + str(time_left), False, (255, 255, 255))
				pygame.draw.rect(screen, bar_fill_color, (w*(percent_w - 0.018),h * (percent_h - 0.035),(pygame.time.get_ticks() - player1.lastCardTime) * 150 / time_limit,50))
				screen.blit(quickplay_text,((w * (percent_w - 0.008)),h * percent_h))
		elif (whose_turn == player2):
			#show how many quickplays left to get bonus
			if (player1.got_wildcard):
				quickplay_text = myfont.render('got wildcard!', False, (255, 255, 255))
				screen.blit(quickplay_text,(w * (percent_w - 0.010),h * percent_h))
			else:
				quickplay_text = myfont.render(str(2 - player1.bonus) + ' more!', False, (255, 255, 255))
				pygame.draw.rect(screen, (25,25,25), (w*(percent_w - 0.018),h * (percent_h - 0.035), 150,50))
				screen.blit(quickplay_text,(w * (percent_w + 0.012),h * percent_h))

#Draws text on screen, based on whose turn it is
#also rechecks hovers
def whose_turn_UI(percent_w, percent_h):
	global winner
	if(winner == None):
		if (whose_turn == player1):
			whose_turn_text = myfont.render('Your turn', False, (255, 255, 255))

			#brings the cards of user back up if it was down
			player1.check_hover(mouse_posx,mouse_posy)
		elif (whose_turn == player2):
			whose_turn_text = myfont.render('AI: hmmm...', False, (255, 255, 255))
	else:
		whose_turn_text = myfont.render(' ' + winner.name, False, (255, 255, 255))

		#brings the cards of user back down if it was up
		#player1.check_hover(0,0)

	#print it out
	screen.blit(whose_turn_text,(w * percent_w,h * percent_h))

#using this for when 'sleeping' the program a.k.a slowing the game down
def reblit_all_cards():
	for i in range(len(pile)):
		rotated = pygame.transform.rotate(pile[i].image,pile[i].rotation)
		screen.blit(rotated, (w * .4,h * .3))
	player1.redraw_hand()
	player2.redraw_hand()

#UI box for restarting the game. access this with "restart_UI_rect"
def restart_UI(percent_w, percent_h):
	global mouse_posx, mouse_posy
	global restart_UI_rect

	size = (100, 50)
	pos = (w * percent_w, h * percent_h)

	restart_UI_button = pygame.image.load("restart.png")
	restart_UI_button = pygame.transform.scale(restart_UI_button, size)

	screen.blit(restart_UI_button, pos)
	restart_UI_rect = pygame.Rect(pos, size)

#------------Set up the match------------

#initialize the deck and pile
deck = []
pile = []
cards_init()

#initialize players
player1 = Player("PLAYER 1", False,
	# Regular player sounds.
	"Sounds/normal.wav",
	"Sounds/invalid.wav",
	"Sounds/special1.flac",
	"Sounds/special2.flac",
	"Sounds/special1.flac", #special 3 same as special 1
	"Sounds/wildcard.wav",
	"Sounds/drawCard.wav",
	"Sounds/drawCard.wav",
	"Sounds/bonus.wav",
	"Sounds/special1.flac", #Loss sound.
	"Sounds/Victory.wav"
	)


player1.draw_card(5)

player2 = Player("PLAYER 2", True,
	#Sounds for AI.
	"Sounds/normal.wav",
	"Sounds/invalid.wav",
	"Sounds/AISpecial1.wav",
	"Sounds/AISpecial2.wav",
	"Sounds/AISpecial3.wav",
	"Sounds/AIWildcard.wav",
	"Sounds/AIDraw.wav",
	"Sounds/AITurn.wav",
	"Sounds/AIBonus.wav",
	"Sounds/AILoss.wav",
	"Sounds/AIVictory.wav")

player2.draw_card(5)

#turn based logic
player1.opponent = player2
player2.opponent = player1
whose_turn = player1;
print ("player " + whose_turn.get_name() + "'s turn.")
print ("player " + whose_turn.get_name() + "'s cards: ")
print (whose_turn.get_hand())

#game state
winner = None

#AI "thinking" delay
yieldTime = randint(800,1500)
AIStartTime = -1

#game loop
while (True):

	#blit the arena
	screen.blit(SURF_BACKGROUND ,(0,0))
	screen.blit(overlay ,(0,0))

	#to visualize the deck decreasing
	if len(deck) > 60:
		screen.blit(deckImage1 ,(w * .05,h * .3))
	elif len(deck) > 50:
		screen.blit(deckImage2 ,(w * .05,h * .3))
	elif len(deck) > 40:
		screen.blit(deckImage3 ,(w * .05,h * .3))
	elif len(deck) > 0:
		screen.blit(deckImage4 ,(w * .05,h * .3))

	for event in pygame.event.get():
		#pressing 'x' on the window
		if (event.type == QUIT):
			pygame.quit()
			exit()

		#moving the mouse
		if event.type == pygame.MOUSEMOTION:
			mouse_posx, mouse_posy = pygame.mouse.get_pos()
			player1.check_hover(mouse_posx,mouse_posy)

		#pressing right click on the mouse
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3:
				#for cards
				x, y = event.pos
				player1.check_click(x,y)
			elif event.button == 1 and winner != None:
				#for restart button
				if (restart_UI_rect.collidepoint(mouse_posx, mouse_posy)):
					winner = None
					print ("restart the game")
					restart_game()

		if (event.type == KEYDOWN) and whose_turn == player1:
			char_pressed = chr(event.key)
			
			key = pygame.key.get_pressed()
			#if space is pressed, then draw a card. Temporary.
			if (key[pygame.K_SPACE]):
				player1.draw_card(1)
				player1.bonus = 0
				player1.opponent.lastCardTime = pygame.time.get_ticks()
				whose_turn = player1.opponent

	if winner == None:
		if len(player1.hand) == 0:
			print (player1.name + "wins!")
			winner = player1
			winner.sound_victory.play()
			winner.opponent.sound_loss.play()
		elif len(player2.hand) == 0:
			print (player2.name + "wins!")
			winner = player2
			winner.sound_victory.play()
			winner.opponent.sound_loss.play()
		
	#AI(player2) logic. We want to delay the AI making a move "AIStartTime"
	if whose_turn == player2 and AIStartTime == -1:
		AIStartTime = pygame.time.get_ticks()

	if whose_turn == player2 and winner == None and (pygame.time.get_ticks() - AIStartTime ) > yieldTime:

		hasCard = False
		for i in range(len(pile)):
			rotated = pygame.transform.rotate(pile[i].image,pile[i].rotation)
			screen.blit(rotated, (w * .4,h * .3))

		#player1.check_hover(-100,-100)
		player1.redraw_hand()
		player2.redraw_hand()
		pygame.display.update()

		yieldTime = randint(2000,bonus_time_limit + 1000)
		AIStartTime = -1
		for i in range(len(player2.hand)):
			print ("i: " + str(i))
			print ( "Card " + str(i) + ": " + player2.hand[i].name)
			if(player2.hand[i].color == currentCard.color or
					player2.hand[i].suite == currentCard.suite or
					player2.hand[i].color == -1):
				player2.check_click(player2.hand[i].rect.x,player2.hand[i].rect.y)
				hasCard = True
				break
		if hasCard == False:
			player2.draw_card(1)
			player2.opponent.lastCardTime = pygame.time.get_ticks()
			whose_turn = player2.opponent
			player2.sound_draw.play()
			player2.bonus = 0

	for i in range(len(pile)):
		rotated = pygame.transform.rotate(pile[i].image,pile[i].rotation)
		screen.blit(rotated, (w * .45,h * .3))
	
	#UI
	quickplay_bar_UI(0.29,0.5)	#quickplay bonus
	whose_turn_UI(0.29, 0.47)	#whose turn it is
	if winner != None:
		restart_UI(.29,.54)				#restart the game

	#update the screen
	player1.redraw_hand()
	player2.redraw_hand()
	pygame.display.update()


