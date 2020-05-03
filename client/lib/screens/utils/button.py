import pygame

class Button:

    def __init__(self, x, y, width, height, color, text='', fill=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.fill = fill

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 2)    # border
        if self.fill:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            text = font.render(self.text, 1, (0, 0, 0))
            x = self.x + (self.width // 2 - text.get_width() // 2)
            y = self.y + (self.height // 2 - text.get_height() // 2)
            screen.blit(text, (x, y))

    def isMouseOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def action(self):    # overwrite functionality after instantiating
        pass

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.isMouseOver(pygame.mouse.get_pos()):
                    self.action()