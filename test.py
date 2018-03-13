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

SURF_BACKGROUND = image.convert()
screen.blit(SURF_BACKGROUND ,(0,0))


#test vals
hand1 = ['1','2','3']
hand2 = ['4','5','6']

#player class
class Player:
	hand = []
	

	def __init__(self, name, hand):
		self.hand = hand
		self.name = name

	def get_hand(self):
		return self.hand

	def get_name(self):
		return self.name

	def make_move(self, card_num):
		print ("picked " + card_num)
		self.hand.remove(card_num)

#turn based logic
player1 = Player("player 1", hand1)
player2 = Player("player 2", hand2)


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