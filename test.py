import pygame
from pygame.locals import *
from sys import exit

#setup
pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Uno Rabbids")

#background image
SURF_BACKGROUND = pygame.image.load("pic1.jpg").convert()
screen.blit(SURF_BACKGROUND ,(0,0))

#turn based logic
whose_turn = 1; # 1 => player 1, 2 => player 2

print ("starting game. Player 1 can press '1', Player 2 can press '2'")
print ("player " + str(whose_turn) + " turn.")

#game loop
while (True):
	for event in pygame.event.get():
		if (event.type == QUIT): #pressing 'x' on the window
			pygame.quit()
			exit()

		#if (event.type != MOUSEMOTION):
			#print (event)

		if (event.type == KEYDOWN):
			if (whose_turn == 1 and event.key == ord('1')):
				whose_turn = 2;
				print("Turn ended. Now it's player " + str(whose_turn) + "'s turn")
			elif (whose_turn == 2 and event.key == ord('2')):
				whose_turn = 1;
				print("Turn ended. Now it's player " + str(whose_turn) + "'s turn")
				
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