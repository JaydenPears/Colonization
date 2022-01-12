import pygame
import os
import sys
from artificial_intelligence import GameBot
from backend import (PlayersColony, PeacefulColony, EnemyColony)


class MainWindow:
    def __init__(self, size):
        self.starter_position = (0, 0)
        self.size = size

        self.states = {'starter menu': self.render_starter_menu}
        self.array_buttons = []

        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.starter_image = pygame.image.load("start_image.png").convert()
        
        running = True

        clock = pygame.time.Clock()
        global_time = 0

        self.check_state = 'starter menu'

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.states[self.check_state]()
            global_time += clock.tick()
            pygame.display.flip()
        pygame.quit()

    def render_starter_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

    def render_create_account_menu(self):
        pass

    def render_enter_account(self):
        pass

    def render_game_lvl_first(self):
        pass

    def render_game_lvl_second(self):
        pass

    def render_game_lvl_third(self):
        pass


class Button:
    def __init__(self, x, y, width, height, color_for_button):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color_for_draw = color_for_button

    def draw_button(self):
        pass

    def hide_button(self):
        pass


if __name__ == '__main__':
    size = width, height = 1920, 1080
    mw = MainWindow(size)