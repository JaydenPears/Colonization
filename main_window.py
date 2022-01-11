import pygame
import os
from artificial_intelligence import EnemyBot
from backend import (load_image, Colony)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def draw_button(self, color_for_button):
        pass


class ColonyAction:
    def __init__(self):
        pass


class MainWindow:
    def __init__(self, size, screen):
        self.fps = 60
        self.screen = screen
        self.size = size
        self.InitUI()

    def InitUI(self):
        running = True

        clock = pygame.time.Clock()
        check_draw_buttons = True
        array_buttons = []

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if check_draw_buttons:
                pass
            clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Колонизация')
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    mw = MainWindow(size, screen)