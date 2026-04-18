import pygame

class Button:
    def __init__(self, size: float, text: str, pos, screen, bgColor, txtColor):
        self.pos = pos
        self.size = size
        self.text = text
        self.screen = screen

        self.font = pygame.font.Font(pygame.font.get_default_font(), size[1])
        self.textSurf = self.font.render(f"{text}", True, txtColor)
        self.button = pygame.Surface((size[0], size[1])).convert()
        self.button.fill(bgColor)

    def render(self):
        self.screen.blit(self.button, (self.pos[0], self.pos[1]))
        self.screen.blit(self.textSurf, (self.pos[0]+1, self.pos[1]+5))

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()#  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False