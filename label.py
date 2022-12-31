import pygame


class Label:
    def __init__(self, text, width, height, pos, screen, gui_font, color):
        # Core attributes
        self.top_color = color
        self.screen = screen

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color

        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)