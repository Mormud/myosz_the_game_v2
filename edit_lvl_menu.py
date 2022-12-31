import pygame, sys
from button import Button
from create_map import CreateMap


class EditLvlMenu():
    def __init__(self, surface, gui_font, clock):
        self.screen = surface
        self.gui_font = gui_font
        self.clock = clock

        # core variables
        screen_size = pygame.display.get_window_size()
        btn_y_vector = screen_size[0] / 2
        btn_x_vector = screen_size[1] / 4
        self.running = True

        # screen elements
        self.create_map_btn = Button('Stwórz mapę', 200, 40, (btn_y_vector - 100, btn_x_vector), 5, self.screen, self.gui_font)
        self.load_map_btn = Button('Wczytaj mapę', 200, 40, (btn_y_vector - 100, (btn_x_vector * 2)), 5, self.screen, self.gui_font)
        self.back_btn = Button('Wróć', 200, 40, (btn_y_vector - 100, (btn_x_vector * 3)), 5, self.screen, self.gui_font)

    def run(self):
        while self.running:
            self.screen.fill('#DCDDD8')

            # buttons
            self.create_map_btn.draw()
            if self.create_map_btn.check_click():
                create_map = CreateMap(self.screen, self.gui_font, self.clock)
                create_map.run()
            self.load_map_btn.draw()
            if self.load_map_btn.check_click():
                pass
            self.back_btn.draw()
            if self.back_btn.check_click():
                self.running = False

            # handling game states
            # main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)
