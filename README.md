# 386RabidsUno

Title: Rabids Uno

Contact Info:
John Lee - hyunmail94@csu.fullerton.edu
Andre Victoria - andreappstuff@csu.fullerton.edu

Files List:

RabidsUno.py - the game itself (must have pygame module before running)

background_x.jpg - background images for the game (not overlay), this is randomly picked

BorderOverlay.png - static overlay (seen on the corners)

Overlay1.png - to indicate it's player 1's turn

Overlay2.png - to indicate it's player 2's turn

GameInstructions.png - game instructions!

Deck_x.png - for the deck. The higher x is the more empty the deck is

restart.png - simple restart button for the game


Folders:

Cards - contains the images for different cards (normals, specials, and faced down state)
	- for normals: Card_1_2.png means it has a color value = 1 and number value = 2

Music - background music for the game (randomizes between 3 songs music_x.mp4)

Sounds - sounds / voice acting for the game.
	   - AI has their own voice lines (ex. used special card, if it's their turn, if they won/lost)
	   - player will also have it's own sounds based on what has happened

How to run:

Please make sure pygame and all its dependencies are installed before running. 

On the terminal: 
```
python3 RabidsUno.py
```
(game info is displayed on the terminal as you play for testing purposes)

How to close:
simply close the window or CTRL + C on the terminal

Features: 
1. background image and music is randomized to add some uniqueness to every match
2. added a bonus timer to reward quick decision making
3. Bunnies

Known Bugs: None
