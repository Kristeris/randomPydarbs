import pygame


from views.windows.WindowGame import WindowGame
from views.windows.WindowMenu import WindowMenu

pygame.init()

window = WindowMenu()
window.show()