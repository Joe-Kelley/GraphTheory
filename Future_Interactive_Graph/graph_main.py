import pygame

from Dijkstras import find_shortest_path
from constants import *
from components import *
from graph_helper import *


pygame.init()
pygame.display.set_caption("Path Finder")
screen = pygame.display.set_mode([ WIDTH, WIDTH ])
screen.fill(BLACK)

def main():
	running = True
	dragging = False
	disabled = False

	board = Board(screen)
	grid = board.grid

	while running:
		board.draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if disabled and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
				disabled = False
				board = Board(screen)
				grid = board.grid

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					dragging = True
					handle_mouse_event(board)

			elif event.type == pygame.MOUSEMOTION and dragging:
				handle_mouse_event(board)

			elif event.type == pygame.MOUSEBUTTONUP:
				dragging = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					find_shortest_path(board)
					board.start.set_start()
					board.end.set_end()
					disabled = True

				# elif event.key == pygame.K_RETURN:
				# 	find_path(board)
				# 	board.start.set_start()
				# 	board.end.set_end()
				# 	disabled = True

	pygame.quit()

if __name__ == '__main__':
	main()