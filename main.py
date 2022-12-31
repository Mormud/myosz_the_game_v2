import pygame, sys
from button import Button
from edit_lvl_menu import EditLvlMenu


# set pygame
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()

# core variables
screen_size = pygame.display.get_window_size()
btn_y_vector = screen_size[0] / 2
btn_x_vector = screen_size[1] / 4
gui_font = pygame.font.Font(None, 30)
running = True

# screen elements
play_btn = Button('Graj', 200, 40, (btn_y_vector - 100, btn_x_vector), 5, screen, gui_font)
edit_lvl_btn = Button('Edytor map', 200, 40, (btn_y_vector - 100, (btn_x_vector * 2)), 5, screen, gui_font)
quit_btn = Button('Wyjdź', 200, 40, (btn_y_vector - 100, (btn_x_vector * 3)), 5, screen, gui_font)

while running:
	screen.fill('#DCDDD8')

	# buttons
	play_btn.draw()
	if play_btn.check_click():
		pass
	edit_lvl_btn.draw()
	if edit_lvl_btn.check_click():
		edit_lvl_menu = EditLvlMenu(screen, gui_font, clock)
		edit_lvl_menu.run()
	quit_btn.draw()
	if quit_btn.check_click():
		running = False

	# handling game states
	#main loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()



	pygame.display.update()
	clock.tick(60)