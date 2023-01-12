import pygame


class Button:
	def __init__(self,text,width,height,pos,elevation, screen, gui_font):
		#Core attributes
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]
		self.screen = screen

		# top rectangle
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'

		#text
		self.text_surf = gui_font.render(text, True, '#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
		self.screen.blit(self.text_surf, self.text_rect)

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.pressed = False
					return True
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'
			return False


class SwButton(Button):
	def check_click(self, on):
		if on:
			self.dynamic_elecation = 0
			self.top_color = '#943434'
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'

		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.pressed = True
			else:
				if self.pressed == True:
					self.pressed = False
					return True
		else:
			return False


class ImgButton:
	def __init__(self, width, height, pos, img_scr, bg_color, screen):
		# core attributes
		self.pressed = False
		self.screen = screen

		# button attributes
		self.bg_color = bg_color
		self.btn_surf = pygame.image.load(img_scr).convert_alpha()
		self.btn_surf = pygame.transform.scale(self.btn_surf, (width, height))
		self.btn_rect = self.btn_surf.get_rect(topleft=pos)

	def draw(self, on):
		self.screen.blit(self.btn_surf, self.btn_rect)
		if on:
			pygame.draw.rect(self.screen, self.bg_color, self.btn_rect, border_radius=12)
			self.screen.blit(self.btn_surf, self.btn_rect)

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.btn_rect.collidepoint(mouse_pos):
			if pygame.mouse.get_pressed()[0]:
				self.pressed = True
			else:
				if self.pressed == True:
					self.pressed = False
					return True
		else:
			return False