import pygame
import sys
import math

pygame.init()

# Инициализация экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Paint')

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Глобальные переменные
brush_color = black
shape = 'Draw'
drawing = False
start_pos = None

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 5))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Функции для выбора цвета и инструментов
def set_black():
    global brush_color, shape
    brush_color = black
    shape = 'Draw'

def set_green():
    global brush_color, shape
    brush_color = green
    shape = 'Draw'

def set_red():
    global brush_color, shape
    brush_color = red
    shape = 'Draw'

def set_blue():
    global brush_color, shape
    brush_color = blue
    shape = 'Draw'

def set_eraser():
    global shape
    shape = 'Eraser'

def clear_screen():
    screen.fill(white)

def exit_app():
    pygame.quit()
    sys.exit()

def set_square():
    global shape
    shape = 'Square'

def set_circle():
    global shape
    shape = 'Circle'

def set_triangle():
    global shape
    shape = 'Triangle'

def set_diamond():
    global shape
    shape = 'Diamond'

# Создание кнопок
buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Square', gray, set_square),
    Button(360, 10, 60, 30, 'Circle', gray, set_circle),
    Button(430, 10, 60, 30, 'Triangle', gray, set_triangle),
    Button(500, 10, 60, 30, 'Eraser', gray, set_eraser),
    Button(570, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(640, 10, 60, 30, 'Exit', gray, exit_app),
    Button(710, 10, 60, 30, 'Diamond', gray, set_diamond)
]

# Очистка экрана при старте
clear_screen()

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                end_pos = pygame.mouse.get_pos()
                if shape == 'Square':
                    rect_width = abs(end_pos[0] - start_pos[0])
                    rect_height = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(screen, brush_color, (start_pos[0], start_pos[1], rect_width, rect_height))
                elif shape == 'Circle':
                    radius = int(math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2))
                    pygame.draw.circle(screen, brush_color, start_pos, radius)
                elif shape == 'Triangle':
                    pygame.draw.polygon(screen, brush_color, [start_pos, end_pos, (start_pos[0], end_pos[1])])
                elif shape == 'Diamond':
                    center_x = (start_pos[0] + end_pos[0]) // 2
                    center_y = (start_pos[1] + end_pos[1]) // 2
                    pygame.draw.polygon(screen, brush_color, [
                        (center_x, start_pos[1]),  # Верх
                        (end_pos[0], center_y),   # Право
                        (center_x, end_pos[1]),   # Низ
                        (start_pos[0], center_y)  # Лево
                    ])

        # Проверяем действия для каждой кнопки
        for button in buttons:
            button.check_action(event)

    if drawing:  # Рисование кистью или ластиком
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:  # Рисуем только ниже панели
            if shape == 'Eraser':  # Если выбран ластик
                pygame.draw.circle(screen, white, (mouse_x, mouse_y), 10)
            elif shape == 'Draw':  # Рисуем кистью
                pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)

    # Отображаем панель инструментов
    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()