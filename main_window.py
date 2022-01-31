import pygame
from artificial_intelligence import GameBot
from backend import (PlayersColony, PeacefulColony, EnemyColony, ActionWithTable,
                     get_right_and_left_pos)
import time

COLOR_ACTIVE_BUTTON = (231, 238, 255)
PLAYERS_COLOR = (173, 214, 255)
ENEMY_COLOR = (255, 102, 102)


class MainWindow:
    def __init__(self, size):
        self.starter_position = (0, 0)
        self.size = size

        self.font = 'Trebuchet MS'
        self.color_for_text = (0, 0, 0)

        self.states = {'starter menu': self.render_starter_menu,
                       'new game': self.render_rules,
                       'download game': self.render_menu_download_game,
                       'settings': self.render_settings_menu,
                       'game lvl': self.render_game_lvl,
                       'init colonies': self.init_colonies}

        self.game_lvl = '1lvl'
        self.game_lvls = {'1lvl': r'GameLevels\Board1.txt',
                          '2lvl': r'GameLevels\Board2.txt',
                          '3lvl': r'GameLevels\Board3.txt'}

        self.sound_mouse = True

        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        self.starter_image = pygame.image.load("images/start_image.png").convert()
        cursor_image = pygame.image.load("images/cursor.png")

        pygame.mouse.set_visible(False)

        self.running = True

        self.saves = ActionWithTable('saves.csv').get_dict()

        clock = pygame.time.Clock()
        self.global_time = 0

        self.check_state = 'starter menu'  # по умолчанию изначально вызываем старт. меню

        self.initialization_buttons()

        while self.running:
            self.states[self.check_state]()
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(cursor_image, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.global_time += clock.tick()
            pygame.display.flip()
        pygame.quit()

    def check_pos_on_button(self, mouse_pos, button_xy, button_size):
        if (mouse_pos[0] >= button_xy[0] and mouse_pos[0] <= button_size[0] + button_xy[0]) \
                and (mouse_pos[1] >= button_xy[1] and mouse_pos[1] <= button_size[1] + button_xy[1]):
            return True
        return False

    def initialization_buttons(self):
        self.size_new_game = (200, 50)
        self.positions_new_game = (self.size[0] // 2 - (self.size_new_game[0] // 2),
                                   self.size[1] // 2 - (self.size_new_game[1] // 2) - 75)
        self.new_game = Button(self.positions_new_game, (915, 455),
                               self.size_new_game,
                               (179, 179, 179), self.color_for_text, self.font,
                               'Новая игра', self.screen)

        self.size_download_game = (200, 50)
        self.positions_download_game = (self.size[0] // 2 - (self.size_download_game[0] // 2),
                                        self.size[1] // 2 - (self.size_download_game[1] // 2) - 15)
        self.download_game = Button(self.positions_download_game, (895, 515),
                                    self.size_download_game,
                                    (179, 179, 179), self.color_for_text, self.font,
                                    'Загрузить игру', self.screen)

        self.size_settings = (200, 50)
        self.positions_settings = (self.size[0] // 2 - (self.size_settings[0] // 2),
                                   self.size[1] // 2 - (self.size_settings[1] // 2) + 45)
        self.settings_button = Button(self.positions_settings, (915, 575),
                                      self.size_settings,
                                      (179, 179, 179), self.color_for_text, self.font,
                                      'Настройки', self.screen)

        self.size_exit = (200, 50)
        self.positions_exit = (self.size[0] // 2 - (self.size_exit[0] // 2),
                               self.size[1] // 2 - (self.size_exit[1] // 2) + 105)
        self.exit_button = Button(self.positions_exit, (935, 635),
                                  self.size_exit,
                                  (179, 179, 179), self.color_for_text, self.font,
                                  'Выйти', self.screen)

        self.size_start_game = (200, 50)
        self.positions_start_game = (self.size[0] // 2 - (self.size_start_game[0] // 2),
                                     self.size[1] // 2 - (self.size_start_game[1] // 2) + 105)
        self.start_game_button = Button(self.positions_start_game, (910, 635),
                                        self.size_start_game,
                                        (179, 179, 179), self.color_for_text, self.font,
                                        'Начать игру', self.screen)

        self.size_off_sound = (300, 50)
        self.positions_off_sound = (self.size[0] // 2 - (self.size_off_sound[0] // 2),
                                    self.size[1] // 2 - (self.size_off_sound[1] // 2) - 200)
        self.off_sound = Button(self.positions_off_sound, (840, 330),
                                self.size_off_sound,
                                (179, 179, 179), self.color_for_text, self.font,
                                'Выключить/Включить звуки', self.screen)

        self.settings_back_size = (300, 50)
        self.positions_settings_back = (self.size[0] // 2 - (self.settings_back_size[0] // 2),
                                        self.size[1] // 2 - (self.settings_back_size[1] // 2))
        self.settings_back = Button(self.positions_settings_back, (750, 530),
                                    self.settings_back_size,
                                    (179, 179, 179), self.color_for_text, self.font,
                                    'Назад', self.screen)

    def init_colonies(self):
        self.board = DrawBoard(self.game_lvls[self.game_lvl], self.screen)
        self.fields = self.board.get_array()
        self.check_state = 'game lvl'

    def render_starter_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

        self.new_game.draw_button()
        self.download_game.draw_button()
        self.exit_button.draw_button()
        self.settings_button.draw_button()

        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        if self.check_pos_on_button(mouse_position, self.positions_new_game,
                                    self.size_new_game):
            self.new_game.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'init colonies'
                pygame.time.delay(100)

        if self.check_pos_on_button(mouse_position, self.positions_download_game,
                                    self.size_download_game):
            self.download_game.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'download game'
                pygame.time.delay(100)

        if self.check_pos_on_button(mouse_position, self.positions_settings,
                                    self.size_settings):
            self.settings_button.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'settings'
                pygame.time.delay(100)

        if self.check_pos_on_button(mouse_position, self.positions_exit,
                                    self.size_exit):
            self.exit_button.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                pygame.time.delay(275)
                self.running = False

    def render_menu_download_game(self):
        self.screen.blit(self.starter_image, self.starter_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_settings_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

        self.off_sound.draw_button()

        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        if self.check_pos_on_button(mouse_position, self.positions_off_sound,
                                    self.size_off_sound):
            self.off_sound.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    self.sound_mouse = False
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                else:
                    self.sound_mouse = True
                pygame.time.delay(125)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_rules(self):
        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        color_for_draw = (231, 238, 255)
        pos_for_rect = (50, 50)
        size = (1820, 545)
        alpha_level = 100

        rect = pygame.Surface(size)
        rect.set_alpha(alpha_level)
        rect.fill(color_for_draw)

        self.screen.blit(self.starter_image, self.starter_position)
        self.screen.blit(rect, pos_for_rect)

        self.start_game_button.draw_button()

        if self.check_pos_on_button(mouse_position, self.positions_start_game,
                                    self.size_start_game):
            self.start_game_button.draw_active_button()
            if is_clicked_mouse[0]:
                if self.sound_mouse:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'game lvl'
                pygame.time.delay(100)

        pos_for_text = [55, 50]
        size_text = 29
        text = ['Суть игры:', '', 'Уважаемый игрок, приветствуем Вас в игре "Колонизация"!',
                'В ходе игры Вам предстоит решать различного рода стратегические головоломки, ' +
                'совершая некоторые логические',
                'умозаключения, чтобы победить соперников и ' +
                'расширить свое превосходство над своими оппонентами.',
                'Вы можете сражаться за территории (колонии), уничтожать злостных врагов ' +
                'и защищать границы своих земель.',
                'Требуется захватывать колонии, которые предстают ' +
                'прямоугольниками некоторого размера на игровом поле.',
                'В дальнейшем же, чтобы победить, требуется захвать все имеющиеся ' +
                'на поле колонии.', '', 'Правила:', '',
                'С помощью использования левой кнопки мышки ("ЛКМ"/"LMB"), Вам потребуется ' +
                'совершать клики, используя войско той или', 'иной колонии, захватывая другие.',
                'Колонии показываются Вам в виде прямоугольниками в рамках игрового поля.',
                'Ваши колонии будут подсвечиваться автоматически синим цветом,' +
                ' а вражеские колонии будут подсвечиваться красным',
                'цветом.', 'Если готовы начать, жмите на кнопку снизу.',
                'Удачной игры и хорошего времяпровождения!']

        for i in range(len(text)):
            self.screen.blit(pygame.font.SysFont(self.font, size_text, bold=True).render(text[i], True,
                                                                                         self.color_for_text),
                             tuple(pos_for_text))
            pos_for_text[1] += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_game_lvl(self):
        self.screen.blit(self.starter_image, self.starter_position)

        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        self.board.draw()

        enemy_colonies = [0]
        players_colonies = [len(self.fields) - 1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

        for field in self.fields:
            if self.fields.index(field) in players_colonies:
                self.board.draw_player(field)
            if self.fields.index(field) in enemy_colonies:
                self.board.draw_enemy(field)
            if self.check_pos_on_button(mouse_position, field[0:2], field[2::]):
                if is_clicked_mouse[0]:
                    if self.sound_mouse:
                        pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                    pygame.time.delay(125)

    def render_endgame(self):
        # Реализовать бег спрайтов в титрах с учётом коллайда и анимаций в дальнейшем
        pass


class Button:
    def __init__(self, pos, text_pos, size, color_for_button, color_for_text, font, text, screen):
        self.x, self.y = pos
        self.width, self.height = size
        self.pos_for_text = text_pos

        self.color_for_draw = color_for_button
        self.color_for_text = color_for_text

        self.screen = screen

        self.font = font
        self.text = text
        self.size_text = 18

    def print_text_on_button(self):
        self.screen.blit(pygame.font.SysFont(self.font, self.size_text, bold=True).render(self.text, True,
                                                                                          self.color_for_text),
                         self.pos_for_text)

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color_for_draw,
                         (self.x, self.y, self.width, self.height))
        self.print_text_on_button()

    def draw_active_button(self):
        pygame.draw.rect(self.screen, COLOR_ACTIVE_BUTTON,
                         (self.x, self.y, self.width, self.height))
        self.print_text_on_button()


class DrawBoard:
    def __init__(self, filename, screen):
        self.filename = filename
        self.screen = screen

        self.nums_from_matrix = ActionWithTable(self.filename).get_nums_from_matrix()
        self.matrix = ActionWithTable(self.filename).get_matrix()

        self.color_rect = (230, 230, 230)
        self.color_outline = (0, 0, 0)

        self.array = []

    def draw(self):
        for i in self.nums_from_matrix:
            pos = get_right_and_left_pos(self.matrix, i)

            x = 785 + pos[0][0] * 50
            y = 90 + pos[0][1] * 75

            width = (pos[1][0] - pos[0][0] + 1) * 50
            height = (pos[1][1] - pos[0][1] + 1) * 75

            self.array.append([x, y, width, height])

            pygame.draw.rect(self.screen, self.color_rect,
                            (x, y, width, height))
            pygame.draw.rect(self.screen, self.color_outline,
                            (x, y, width, height), 1)

    def get_array(self):
        return self.array

    def draw_enemy(self, field):
        pygame.draw.rect(self.screen, ENEMY_COLOR,
                         (field[0], field[1], field[2], field[3]))
        pygame.draw.rect(self.screen, self.color_outline,
                         (field[0], field[1], field[2], field[3]), 1)

    def draw_player(self, field):
        pygame.draw.rect(self.screen, PLAYERS_COLOR,
                         (field[0], field[1], field[2], field[3]))
        pygame.draw.rect(self.screen, self.color_outline,
                         (field[0], field[1], field[2], field[3]), 1)


# Для печати кол-ва населения
def print_text_on_rect(screen, pos_for_text, size, font, text, color_for_text):
        screen.blit(pygame.font.SysFont(font, size, bold=True).render(text, True,
                                        color_for_text), pos_for_text)


if __name__ == '__main__':
    SIZE = width, height = 1920, 1080
    mw = MainWindow(SIZE)