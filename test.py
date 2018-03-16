import pygame
from pygame.locals import *
from sys import exit
from random import randint

#setup
pygame.init()

pygame.display.set_caption("Uno Rabbids")

#background image
image = pygame.image.load("background_" + str(randint(1,10)) + ".jpg")

screen = pygame.display.set_mode(image.get_rect().size)
w, h = pygame.display.get_surface().get_size()

SURF_BACKGROUND = image.convert()

deckImage1 = pygame.image.load("Deck_1.png").convert_alpha()
deckImage2 = pygame.image.load("Deck_2.png").convert_alpha()
deckImage3 = pygame.image.load("Deck_3.png").convert_alpha()
deckImage4 = pygame.image.load("Deck_4.png").convert_alpha()

overlay = pygame.image.load("BorderOverlay.png").convert_alpha()

pygame.mixer.music.load("Music/music_2.mp4")
pygame.mixer.music.play(-1)

def MAX(left=0,right=0):
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


deck = []
pile = []

#populate deck with 2 copies of each standard card.
for i in range(1,5):
	for j in range(1,10):
		deck.append(Card(i,j,None));
		deck.append(Card(i,j,None));

#set a standard card to the center.
currentCard = deck[randint(0,len(deck))]
currentCard.rotation = randint(180,270)
pile.append(currentCard)
deck.remove(currentCard)


#append special cards to the deck.
#2 of each +x card for each color.
for i in range(1,5):
	for j in range(1,3):
		deck.append(Card(i,-j,"special_" + str(j)))
		deck.append(Card(i,-j,"special_" + str(j)))
	#1 wildcard per color
	deck.append(Card(-1,-3,"wildcard"))


#shuffle deck.
for i in range(len(deck)):
	for j in range(0,5):
		tmp = deck[i]
		rnd = randint(18,36)
		deck[i] = deck[(i+rnd)%len(deck)]
		deck[(i+rnd)%len(deck)] = tmp

print("DECKLIST: ")
for i in range(len(deck)):
	print("Card" + str(i) + ": " +deck[i].name)



#player class
class Player:
	hand = []
	cardCount = 0;	
	wildcard = None

	def __init__(self, name, isHidden,sound_normal,sound_special1,sound_special2,sound_wildcard,sound_draw):
		self.name = name
		self.isHidden = isHidden;
		self.sound_normal = effect = pygame.mixer.Sound(sound_normal)
		self.sound_special1 = pygame.mixer.Sound(sound_special1)
		self.sound_special2 = pygame.mixer.Sound(sound_special2)
		self.sound_wildcard = pygame.mixer.Sound(sound_wildcard)
		self.sound_draw = pygame.mixer.Sound(sound_draw)

	def check_hover(self,x,y):
		#print ("hovering");
		found = False
		for i in reversed(range(len(self.hand))):
			if x > self.hand[i].rect.x and (x<self.hand[i].rect.x+self.hand[i].image.get_width()):
			    x_inside = True
			else: x_inside = False
			if y > self.hand[i].rect.y and (y<self.hand[i].rect.y+self.hand[i].image.get_height()):
			    y_inside = True
			else: y_inside = False
			if x_inside and y_inside and found == False:
				found = True
				self.hand[i].rect.y = h * .55
			else: self.hand[i].rect.y = h * .75

	def check_click(self,x,y):
		for i in reversed(range(len(self.hand))):
			if self.hand[i].rect.collidepoint(x, y):
				global currentCard 

				if(self.hand[i].color == currentCard.color or
					self.hand[i].suite == currentCard.suite or
					self.hand[i].color == -1):
					currentCard = self.hand[i]
					currentCard.rotation = randint(90,270)
					
					print ("You played: " + currentCard.name);
					self.sound_normal.play()
					self.wildcard = None

					if currentCard.name == "wildcard":
						self.wildcard = currentCard;

						self.hand.remove(currentCard)
						pile.append(currentCard)

						currentCard = Card(self.hand[randint(0,len(self.hand)-1)].color,randint(1,9),None)
						self.sound_wildcard.play()

						pile.append(currentCard)
						
					elif currentCard.name == "special_1":
						self.draw_card(2)
						print("Special!!! Opponent Draws 2 cards!")
						self.sound_special1.play()

						self.hand.remove(currentCard)
						pile.append(currentCard)
					elif currentCard.name == "special_2":
						self.draw_card(4)
						self.sound_special2.play()
						print("Special!!! Opponent Draws 4 cards!")

						self.hand.remove(currentCard)
						pile.append(currentCard)
					else:
						
						self.hand.remove(currentCard)
						pile.append(currentCard)

					break
					

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
			screen.blit(self.hand[i].image, (w * startx,self.hand[i].rect.y))
			startx += interval
		if self.wildcard != None:
			screen.blit(self.wildcard.image, (w * 0,h * .75))

	def draw_card(self,count):
		for i in range(count):
			self.hand.append(deck[i])
			deck[i].rect = deck[i].image.get_rect()
			deck[i].rect.y = h * .75
			print ("drew " + deck[i].name)
			deck.remove(deck[i])
			self.redraw_hand()
		if count < 5:
			self.sound_draw.play()
		print (str(len(deck)) + " cards in deck, " + str(len(self.hand)) + " cards in hand.")
		#TODO: If no more cards in deck, and neither player has won, declare the game a tie.


	def get_hand(self):
		return self.hand

	def get_name(self):
		return self.name

	def make_move(self, card_num):
		print ("picked " + card_num)
		self.hand.remove(card_num)





player1 = Player("player 1", False,
	#Sounds for AI. There are different sounds for regular player. This is just to test.
	"Sounds/normal.wav",
	"Sounds/AISpecial1.wav",
	"Sounds/AISpecial2.wav",
	"Sounds/AIWildcard.wav",
	"Sounds/AIDraw.wav"
	)
# Regular player sounds.
# "Sounds/normal.wav",
# 	"Sounds/special1.flac",
# 	"Sounds/special2.flac",
# 	"Sounds/wildcard.wav",
# 	"Sounds/drawCard.wav"

player1.draw_card(5)
player2 = Player("player 2", True,
	#Sounds for AI.
	"Sounds/normal.wav",
	"Sounds/AISpecial1.wav",
	"Sounds/AISpecial2.wav",
	"Sounds/AIWildcard.wav",
	"Sounds/AIDraw.wav")

#turn based logic
whose_turn = player1; # 1 => player 1, 2 => player 2

print ("player " + whose_turn.get_name() + "'s turn.")
print ("player " + whose_turn.get_name() + "'s cards: ")
print (whose_turn.get_hand())

#game loop
while (True):
	screen.blit(SURF_BACKGROUND ,(0,0))
	screen.blit(overlay ,(0,0))

	if len(deck) > 60:
		screen.blit(deckImage1 ,(w * .05,h * .3))
	elif len(deck) > 50:
		screen.blit(deckImage2 ,(w * .05,h * .3))
	elif len(deck) > 40:
		screen.blit(deckImage3 ,(w * .05,h * .3))
	elif len(deck) > 0:
		screen.blit(deckImage4 ,(w * .05,h * .3))


	for event in pygame.event.get():
		if (event.type == QUIT): #pressing 'x' on the window
			pygame.quit()
			exit()

		#if (event.type != MOUSEMOTION):
			#print (event)


		if event.type == pygame.MOUSEMOTION:
			mouse_posx, mouse_posy = pygame.mouse.get_pos()
			player1.check_hover(mouse_posx,mouse_posy)

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			x, y = event.pos
			player1.check_click(x,y)

		if (event.type == KEYDOWN):
			char_pressed = chr(event.key)
			
			key = pygame.key.get_pressed()
			#if space is pressed, then draw a card. Temporary.
			if (key[pygame.K_SPACE]):
				player1.draw_card(1);

			#check if move is legal according to whose turn it is
			# if (char_pressed in whose_turn.get_hand()):
			# 	#make the move
			# 	whose_turn.make_move(char_pressed)
			# 	print (whose_turn.get_hand())

			# 	#change turn
			# 	if (whose_turn == player1):
			# 		whose_turn = player2
			# 	else:
			# 		whose_turn = player1

			# 	#prompt opposing player
			# 	print("Turn ended. Now it's player " + str(whose_turn.get_name()) + "'s turn")
			# 	print (whose_turn.get_hand())
			# else:
			# 	print("You don't have that card!")

	for i in range(len(pile)):
		rotated = pygame.transform.rotate(pile[i].image,pile[i].rotation)
		screen.blit(rotated, (w * .4,h * .3))

	player1.redraw_hand()
	pygame.display.update()



#unused stuff (might be useful later)

#increase FPS
'''
clock = pygame.time.Clock()
clock.tick(60)
'''

#change cursor image
'''
MOUSE_IMAGE = "cursor1.png"
#surf_cursor = pygame.image.load(MOUSE_IMAGE).convert_alpha()
inside game loop:
x,y = pygame.mouse.get_pos()
x -= surf_cursor.get_width() / 2
y -= surf_cursor.get_height() / 2
screen.blit(surf_cursor, (x,y))
'''