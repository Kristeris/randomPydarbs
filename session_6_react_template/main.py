import pygame


from views.windows.WindowGame import WindowGame
from views.windows.WindowHighScores import WindowHighScores, ReactPropsWindowHighScores
from views.windows.WindowMenu import WindowMenu, ReactPropsWindowMenu

pygame.init()
screen = pygame.display.set_mode((640, 640))


window = WindowMenu(props=ReactPropsWindowMenu(
    width=screen.get_width(),
    height=screen.get_height()
))
window.show(screen)
