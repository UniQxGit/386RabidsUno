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
screen.blit(SURF_BACKGROUND ,(0,0))

image = pygame.image.load("BorderOverlay.png")
screen.blit(image ,(0,0))

image = pygame.image.load("Deck_1.png")
screen.blit(image ,(w * .05,h * .3))

#card class
class Card:
	color = 0
	suite = 0
	name = ""

	def __init__(self, color, suite):
		self.color = color
		self.suite = suite
		self.name = "card_" + str(color) + "_" + str(suite)
		self.image = None
		self.rect = None

	def get_color(self):
		return self.color

	def get_suite(self):
		return self.suite

	def get_name(self):
		return self.suite

	def is_inside(self):
		#check if recieving rect is inside
		return false


deck = []
for i in range(1,5):
	for j in range(1,10):
		print("Created Card: " + Card(i,j).name)
		deck.append(Card(i,j));
		deck.append(Card(i,j));

#player class
class Player:
	hand = []
	cardCount = 0;	

	def __init__(self, name, isMain):
		self.name = name
		self.isMain = isMain;

	def redraw_hand(self):
		startx = .2
		starty = .75
		interval = (.5) / (len(self.hand))
		for i in range(len(self.hand)):
			self.hand[i].rect.center = (w * startx,h * starty)
			screen.blit(self.hand[i].image, (w * startx,h * starty))
			startx += interval

	def draw_card(self,count):
		for i in range(count):
			self.hand.append(deck[i])
			deck[i].image = pygame.image.load("Cards/" + deck[i].name + ".png")
			deck[i].rect = deck[i].image.get_rect()
			deck.remove(deck[i])
		self.redraw_hand()
		# image = pygame.image.load("Cards/card_3_4.png")
		# screen.blit(image ,(w*.35,h*.75))
		# image = pygame.image.load("Cards/card_2_6.png")
		# screen.blit(image ,(w*.45,h*.75))
		# image = pygame.image.load("Cards/card_1_8.png")
		# screen.blit(image ,(w*.55,h*.75))
		# image = pygame.image.load("Cards/card_1_8.png")
		# screen.blit(image ,(w*.65,h*.75))


	def get_hand(self):
		return self.hand

	def get_name(self):
		return self.name

	def make_move(self, card_num):
		print ("picked " + card_num)
		self.hand.remove(card_num)




#test vals

#turn based logic
player1 = Player("player 1", True)
player1.draw_card(5)
player1.draw_card(1)
player2 = Player("player 2", False)


whose_turn = player1; # 1 => player 1, 2 => player 2

print ("player " + whose_turn.get_name() + "'s turn.")
print ("player " + whose_turn.get_name() + "'s cards: ")
print (whose_turn.get_hand())

#game loop
while (True):
	for event in pygame.event.get():
		if (event.type == QUIT): #pressing 'x' on the window
			pygame.quit()
			exit()

		#if (event.type != MOUSEMOTION):
			#print (event)

		if (event.type == KEYDOWN):
			char_pressed = chr(event.key)

			#check if move is legal according to whose turn it is
			if (char_pressed in whose_turn.get_hand()):
				#make the move
				whose_turn.make_move(char_pressed)
				print (whose_turn.get_hand())

				#change turn
				if (whose_turn == player1):
					whose_turn = player2
				else:
					whose_turn = player1

				#prompt opposing player
				print("Turn ended. Now it's player " + str(whose_turn.get_name()) + "'s turn")
				print (whose_turn.get_hand())
			else:
				print("You don't have that card!")
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