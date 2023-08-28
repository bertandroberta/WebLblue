import pygame

class Button(object):
    def __init__(self, font, text, color, x, y, **kwargs):
        self.surface = font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y

    def display(self,screen):
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False


class ButtonImage(object):
    def __init__(self, image_path, x, y, ratio = 1, **kwargs):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * ratio, self.image.get_height() * ratio))

        self.WIDTH = self.image.get_width()
        self.HEIGHT = self.image.get_height()

        self.x = x
        self.y = y

    def display(self,screen):
        screen.blit(self.image, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match:
            return True
        else:
            return False