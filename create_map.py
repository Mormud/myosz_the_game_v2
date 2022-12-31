import pygame, sys
from button import Button
from label import Label
from plr_color import plr_color_list
from map_engine import Map


class CreateMap():
    def __init__(self, surface, gui_font, clock):
        self.screen = surface
        self.gui_font = gui_font
        self.clock = clock

        # core variables
        screen_size = pygame.display.get_window_size()
        self.btn_x_vector = screen_size[0] / 8
        self.btn_y_vector = screen_size[1] / 13
        self.running = True
        self.selected_item = 0
        self.plr_color = plr_color_list

        # map
        self.map_width = int(screen_size[0] - self.btn_x_vector * 2)
        self.map_height = screen_size[1]
        self.field_size = 30
        self.map = Map(self.field_size)
        self.zoom_value = 5

        # screen elements
        # right menu
        self.back_btn = Button('Wróć', 200, 40, ((self.btn_x_vector * 6) + 70, (self.btn_y_vector)),
                               5, self.screen, self.gui_font)
        self.zoom_in_btn = Button('+', 40, 40, ((self.btn_x_vector * 6) + 150, (self.btn_y_vector * 2)),
                                  5, self.screen, self.gui_font)
        self.zoom_out_btn = Button('-', 40, 40, ((self.btn_x_vector * 6) + 150, (self.btn_y_vector * 3)),
                                   5, self.screen, self.gui_font)
        self.choose_element = Button('Gracz', 200, 40, ((self.btn_x_vector * 6) + 70, self.btn_y_vector * 4),
                                     5, self.screen, self.gui_font)
        self.clear_btn = Button('Reset', 200, 40, ((self.btn_x_vector * 6) + 70, (self.btn_y_vector * 12)),
                               5, self.screen, self.gui_font)
        self.right_menu_bg_surf = pygame.Surface((screen_size[0] - self.map_width, screen_size[1]))
        self.right_menu_bg_surf.fill('#202124')
        self.right_menu_bg_rect = self.right_menu_bg_surf.get_rect(bottomright=(screen_size[0], screen_size[1]))

    def run(self):
        while self.running:
            self.screen.fill('#202124')
            # map
            self.map.create_map_func(self.screen, self.selected_item, self.map_width, self.map_height)

            # right menu
            self.screen.blit(self.right_menu_bg_surf, self.right_menu_bg_rect)
            # buttons
            self.back_btn.draw()
            if self.back_btn.check_click():
                self.running = False

            self.zoom_in_btn.draw()
            if self.zoom_in_btn.check_click():
                if self.field_size + self.zoom_value < 50:
                    self.field_size += self.zoom_value
                    self.map.zoom_in(self.field_size)

            self.zoom_out_btn.draw()
            if self.zoom_out_btn.check_click():
                 if self.field_size - self.zoom_value > 10:
                    self.field_size -= self.zoom_value
                    self.map.zoom_out(self.field_size)

            self.choose_element.draw()
            if self.choose_element.check_click():
                self.selected_item += 1
                if self.selected_item > len(self.plr_color) - 1:
                    self.selected_item = 0

            self.clear_btn.draw()
            if self.clear_btn.check_click():
                self.map.clear_map()

            # selected item label
            selected_lbl = Label('', 200, 45, ((self.btn_x_vector * 6) + 70, self.btn_y_vector * 5), self.screen, self.gui_font,self.plr_color[self.selected_item])
            selected_lbl.draw()

            # main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)