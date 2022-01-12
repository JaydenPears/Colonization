import pygame
import os
import sys
from artificial_intelligence import GameBot
from backend import (PlayersColony, PeacefulColony, EnemyColony)


class MainWindow:
    def __init__(self, size):
        self.starter_position = (0, 0)
        self.size = size

        self.states = {'starter menu': self.starter_menu}

        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.starter_image = pygame.image.load("images/start_image.png").convert()
        cursor_image = pygame.image.load("images/cursor.png")

        pygame.mouse.set_visible(False)
        
        running = True

        clock = pygame.time.Clock()
        global_time = 0

        self.check_state = 'starter menu'

        while running:
            self.states[self.check_state]()
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(cursor_image, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            global_time += clock.tick()
            pygame.display.flip()
        pygame.quit()

    def starter_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)
        size_create_account = (200, 50)
        positions = (self.size[0] // 2 - size_create_account[0],
                     self.size[1] // 2 - size_create_account[1])
        button_create_account = Button(positions, size_create_account,
                                       (1, 1, 1), 'Trebuchet MS', 'Зарегистрироваться',
                                       self.screen)

    def render_game_lvl_first(self):
        pass

    def render_game_lvl_second(self):
        pass

    def render_game_lvl_third(self):
        pass


class Button:
    def __init__(self, pos, size, color_for_button, font, text, screen):
        self.x, self.y = pos
        self.width, self.height = size
        self.color_for_draw = color_for_button
        self.screen = screen
        self.font = font
        self.text = text

    def draw_button(self):
        pass

    def draw_active_button(self):
        pass

    def hide_button(self):
        pass


if __name__ == '__main__':
    size = width, height = 1920, 1080
    mw = MainWindow(size)