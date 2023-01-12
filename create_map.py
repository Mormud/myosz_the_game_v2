import pygame, sys
from button import Button, ImgButton ,SwButton
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
        self.tower_btn = ImgButton(100, 100, (self.btn_x_vector * 6 + 120, self.btn_y_vector * 6),
                                   'assets/field_elements/tower.png', '#DCDDD8', self.screen)
        self.base_btn = ImgButton(100, 100, (self.btn_x_vector * 6 + 120, self.btn_y_vector * 8),
                                   'assets/field_elements/house.png', '#DCDDD8', self.screen)
        self.remove_btn = SwButton('Usuń', 200, 40, ((self.btn_x_vector * 6) + 70, (self.btn_y_vector * 10)),
                                5, self.screen, self.gui_font)
        self.save_btn = Button('Zapisz', 200, 40, ((self.btn_x_vector * 6) + 70, (self.btn_y_vector * 11)),
                                5, self.screen, self.gui_font)
        self.clear_btn = Button('Reset', 200, 40, ((self.btn_x_vector * 6) + 70, (self.btn_y_vector * 12)),
                               5, self.screen, self.gui_font)
        self.right_menu_bg_surf = pygame.Surface((screen_size[0] - self.map_width, screen_size[1]))
        self.right_menu_bg_surf.fill('#202124')
        self.right_menu_bg_rect = self.right_menu_bg_surf.get_rect(bottomright=(screen_size[0], screen_size[1]))

        # buttons variables
        self.tower_chosen = False
        self.base_chosen = False
        self.remove_chosen = False
        self.selected_item = 0
        self.last_selected_field = 0

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
                if self.tower_chosen or self.base_chosen or self.remove_chosen:
                    self.selected_item = self.last_selected_field
                self.selected_item += 1
                if self.selected_item > len(self.plr_color) - 1:
                    self.selected_item = 0
                self.tower_chosen = False
                self.base_chosen = False
                self.remove_chosen = False
                self.last_selected_field = self.selected_item

            self.tower_btn.draw(self.tower_chosen)
            if self.tower_btn.check_click():
                if self.tower_chosen:
                    self.tower_chosen = False
                    self.selected_item = self.last_selected_field
                else:
                    self.tower_chosen = True
                    self.base_chosen = False
                    self.remove_chosen = False
                    self.selected_item = len(self.plr_color) + 1

            self.base_btn.draw(self.base_chosen)
            if self.base_btn.check_click():
                if self.base_chosen:
                    self.base_chosen = False
                    self.selected_item = self.last_selected_field
                else:
                    self.base_chosen = True
                    self.tower_chosen = False
                    self.remove_chosen = False
                    self.selected_item = len(self.plr_color) + 2

            self.remove_btn.draw()
            if self.remove_btn.check_click(self.remove_chosen):
                if self.remove_chosen:
                    self.remove_chosen = False
                    self.selected_item = self.last_selected_field
                else:
                    self.remove_chosen = True
                    self.base_chosen = False
                    self.tower_chosen = False
                    self.selected_item = len(self.plr_color) + 3

            self.save_btn.draw()
            if self.save_btn.check_click():
                self.map.save_map()

            self.clear_btn.draw()
            if self.clear_btn.check_click():
                self.map.clear_map()

            # selected item label
            if self.selected_item < len(self.plr_color):
                selected_lbl = Label('', 200, 45, ((self.btn_x_vector * 6) + 70, self.btn_y_vector * 5), self.screen, self.gui_font,self.plr_color[self.selected_item])
                selected_lbl.draw()
            else:
                selected_lbl = Label('', 200, 45, ((self.btn_x_vector * 6) + 70, self.btn_y_vector * 5), self.screen,
                                     self.gui_font, self.plr_color[self.last_selected_field])
                selected_lbl.draw()

            # main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)