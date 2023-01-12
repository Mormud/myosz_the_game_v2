import pygame
import threading
import numpy
import math
import os
import json
from plr_color import plr_color_list


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, field_size):
        super().__init__()
        self.image = pygame.image.load("assets/field_elements/tower_lowest.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (field_size, field_size))
        self.rect = self.image.get_rect(topleft=(x * field_size, y * field_size))


class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, field_size):
        super().__init__()
        self.image = pygame.image.load("assets/field_elements/house_low.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (field_size, field_size))
        self.rect = self.image.get_rect(topleft=(x * field_size, y * field_size))

class Map:
    def __init__(self, field_size):
        # map variables
        self.num_x_fields = 50
        self.num_y_fields = 30
        self.map = numpy.zeros((self.num_x_fields,self.num_y_fields), numpy.dtype(int))
        self.field_size = field_size
        self.map_surf = pygame.Surface((self.num_x_fields * self.field_size, self.num_y_fields * self.field_size))
        self.tower_map = []
        self.towers = pygame.sprite.Group()
        self.base_map = []
        self.bases = pygame.sprite.Group()

        # engine variables
        self.map_generated = False
        self.offset_x = 0
        self.offset_y = 0
        self.default_moving_speed = 8
        self.moving_speed = 5
        self.moving_speed_switched = False
        self.draw_on_map_clicked = False
        self.temp_fields_list = []
        self.towers_generated = False
        self.bases_generated = False
        self.del_index = 0
        self.smth_to_del = False
        self.base_deleted = False
        self.tower_deleted = False

        # others var
        self.plr_colors = plr_color_list
        self.single_tower_surf = pygame.image.load("assets/field_elements/tower_lowest.png").convert_alpha()
        self.single_tower_rect = self.single_tower_surf.get_rect(topleft=(0, 0))


    def generate_map(self):
        if self.map_generated == False:
            for x in range(0, self.num_x_fields - 1):
                for y in range(0, self.num_y_fields - 1):
                    single_field_surf = pygame.Surface((self.field_size, self.field_size))
                    single_field_surf.fill(self.plr_colors[self.map[x][y]])
                    self.map_surf.blit(single_field_surf, (x * self.field_size, y * self.field_size))
            self.map_generated = True

    def generate_towers(self):
        if self.towers_generated:
            pass
        else:
            self.towers.empty()
            if len(self.tower_map) > 0:
                self.tower_map = list(dict.fromkeys(self.tower_map))
                for x in self.tower_map:
                    if x[2] == len(self.plr_colors) + 1:
                        self.towers.add(Tower(x[0], x[1], self.field_size))
            self.towers_generated = True
            if self.tower_deleted:
                self.map_generated = False
                self.tower_deleted = False

    def generate_bases(self):
        if self.bases_generated:
            pass
        else:
            self.bases.empty()
            if len(self.base_map) > 0:
                self.base_map = list(dict.fromkeys(self.base_map))
                for x in self.base_map:
                    if x[2] == len(self.plr_colors) + 2:
                        self.bases.add(Base(x[0], x[1], self.field_size))
            self.bases_generated = True
        if self.base_deleted:
            self.map_generated = False
            self.base_deleted = False

    def draw_on_map(self, selected_item, width_map, height_map):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < width_map and mouse_pos[1] < height_map:
            if pygame.mouse.get_pressed()[0]:
                # drowning plrs fields
                if selected_item < len(self.plr_colors):
                    self.draw_on_map_clicked = True
                    x_axis = math.floor((mouse_pos[0] - self.offset_x) / self.field_size)
                    y_axis = math.floor((mouse_pos[1] - self.offset_y) / self.field_size)
                    if x_axis < self.num_x_fields and y_axis < self.num_y_fields:
                        self.map[x_axis][y_axis] = selected_item
                        self.temp_fields_list.append((x_axis, y_axis, selected_item))
                        self.map_generated = False

                # saving drawn fields to memory
                try:
                    self.temp_fields_list = list(dict.fromkeys(self.temp_fields_list))
                    for field in self.temp_fields_list:
                        single_field_surf = pygame.Surface((self.field_size, self.field_size))
                        single_field_surf.fill(field[2])
                        single_field_rect = single_field_surf.get_rect(topleft = (field[0], field[1]))
                        self.map_surf.blit(single_field_surf, single_field_rect)
                except:
                    pass

                # setting towers on map
                if selected_item == len(self.plr_colors) + 1:
                    x_axis = math.floor((mouse_pos[0] - self.offset_x) / self.field_size)
                    y_axis = math.floor((mouse_pos[1] - self.offset_y) / self.field_size)
                    if x_axis < self.num_x_fields and y_axis < self.num_y_fields:
                        self.tower_map.append((x_axis, y_axis, selected_item))
                        self.towers_generated = False

                # setting bases on map
                if selected_item == len(self.plr_colors) + 2:
                    x_axis = math.floor((mouse_pos[0] - self.offset_x) / self.field_size)
                    y_axis = math.floor((mouse_pos[1] - self.offset_y) / self.field_size)
                    if x_axis < self.num_x_fields and y_axis < self.num_y_fields:
                        self.base_map.append((x_axis, y_axis, selected_item))
                        self.bases_generated = False

                # deleting elements
                if selected_item == len(self.plr_colors) + 3:
                    x_axis = math.floor((mouse_pos[0] - self.offset_x) / self.field_size)
                    y_axis = math.floor((mouse_pos[1] - self.offset_y) / self.field_size)
                    if x_axis < self.num_x_fields and y_axis < self.num_y_fields:
                        for x in self.base_map:
                            if x[0] == x_axis and x[1] == y_axis:
                                self.base_map.pop(self.base_map.index(x))
                                self.bases_generated = False
                                self.base_deleted = True

                        for x in self.tower_map:
                            if x[0] == x_axis and x[1] == y_axis:
                                self.tower_map.pop(self.tower_map.index(x))
                                self.towers_generated = False
                                self.tower_deleted = True


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
        self.towers_generated = False
        self.bases_generated = False

    def zoom_out(self, field_size):
        self.field_size = field_size
        self.map_surf = pygame.Surface((self.num_x_fields * self.field_size, self.num_y_fields * self.field_size))
        self.map_generated = False
        self.towers_generated = False
        self.bases_generated = False
    def get_map(self):
        return self.map


    def clear_map(self):
        self.map = numpy.zeros((self.num_x_fields,self.num_y_fields), numpy.dtype(int))
        self.map_generated = False
        self.towers_generated = False
        self.bases_generated = False
        self.tower_map.clear()
        self.towers.empty()
        self.base_map.clear()
        self.bases.empty()


    def save_map(self):
        pass


    def create_map_func(self, surface, selected_item, width_map, height_map):
        t1 = threading.Thread(target=self.generate_map)
        t2 = threading.Thread(target=self.draw_on_map, args=(selected_item, width_map, height_map))
        t3 = threading.Thread(target=self.moving_on_map)
        t1.run()
        t2.run()
        t3.run()
        self.generate_towers()
        self.towers.draw(self.map_surf)
        self.generate_bases()
        self.bases.draw(self.map_surf)
        surface.blit(self.map_surf, (self.offset_x, self.offset_y))


