import pygame
import threading
import numpy
import math
from plr_color import plr_color_list


class Map:
    def __init__(self, field_size):
        # map variables
        self.num_x_fields = 50
        self.num_y_fields = 30
        self.map = numpy.zeros((self.num_x_fields,self.num_y_fields), numpy.dtype(int))
        self.field_size = field_size
        self.map_surf = pygame.Surface((self.num_x_fields * self.field_size, self.num_y_fields * self.field_size))

        # engine variables
        self.map_generated = False
        self.offset_x = 0
        self.offset_y = 0
        self.default_moving_speed = 8
        self.moving_speed = 5
        self.moving_speed_switched = False
        self.draw_on_map_clicked = False
        self.temp_fields_list = []

        # others var
        self.plr_colors = plr_color_list

    def generate_map(self):
        if self.map_generated == False:
            for x in range(0, self.num_x_fields - 1):
                for y in range(0, self.num_y_fields - 1):
                    if self.map[x][y] == 8:
                        pass
                    else:
                        single_field_surf = pygame.Surface((self.field_size, self.field_size))
                        single_field_surf.fill(self.plr_colors[self.map[x][y]])
                        self.map_surf.blit(single_field_surf, (x * self.field_size, y * self.field_size))
            self.map_generated = True

    def draw_on_map(self, selected_item, width_map, height_map):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < width_map and mouse_pos[1] < height_map:
            if pygame.mouse.get_pressed()[0]:
                self.draw_on_map_clicked = True
                x_axis = math.floor((mouse_pos[0] - self.offset_x) / self.field_size)
                y_axis = math.floor((mouse_pos[1] - self.offset_y) / self.field_size)
                if x_axis < self.num_x_fields and y_axis < self.num_y_fields:
                    self.map[x_axis][y_axis] = selected_item
                    self.temp_fields_list.append((x_axis, y_axis, selected_item))
                    self.map_generated = False

            try:
                self.temp_fields_list = list(dict.fromkeys(self.temp_fields_list))
                for field in self.temp_fields_list:
                    single_field_surf = pygame.Surface((self.field_size, self.field_size))
                    single_field_surf.fill(field[2])
                    self.map_surf.blit(single_field_surf, (field[0], field[1]))
            except:
                pass

            if self.draw_on_map_clicked:
                if pygame.mouse.get_pressed()[0] == False:
                    self.temp_fields_list.clear()
                    self.map_generated = False
                    self.draw_on_map_clicked = False

    def moving_on_map(self):
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.moving_speed = self.default_moving_speed * 2
            self.moving_speed_switched = True
        elif self.moving_speed_switched:
            self.moving_speed = self.default_moving_speed
            self.moving_speed_switched = False
        if pygame.key.get_pressed()[pygame.K_s]:
            self.offset_y -= self.moving_speed
        if pygame.key.get_pressed()[pygame.K_w]:
            self.offset_y += self.moving_speed
        if pygame.key.get_pressed()[pygame.K_d]:
            self.offset_x -= self.moving_speed
        if pygame.key.get_pressed()[pygame.K_a]:
            self.offset_x += self.moving_speed

    def zoom_in(self, field_size):
        self.field_size = field_size
        self.map_surf = pygame.Surface((self.num_x_fields * self.field_size, self.num_y_fields * self.field_size))
        self.map_generated = False

    def zoom_out(self, field_size):
        self.field_size = field_size
        self.map_surf = pygame.Surface((self.num_x_fields * self.field_size, self.num_y_fields * self.field_size))
        self.map_generated = False
    def get_map(self):
        return self.map

    def clear_map(self):
        self.map = numpy.zeros((self.num_x_fields,self.num_y_fields), numpy.dtype(int))
        self.map_generated = False

    def create_map_func(self, surface, selected_item, width_map, height_map):
        t1 = threading.Thread(target=self.generate_map)
        t2 = threading.Thread(target=self.draw_on_map, args=(selected_item, width_map, height_map))
        t3 = threading.Thread(target=self.moving_on_map)
        t1.run()
        t2.run()
        t3.run()
        surface.blit(self.map_surf, (self.offset_x, self.offset_y))

