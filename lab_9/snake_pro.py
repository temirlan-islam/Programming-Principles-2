import pygame  
import sys  
import copy  
import random  
import time  

pygame.init()  

# Устанавливаем параметры игры
scale = 15  
score = 0  
level = 0  
SPEED = 20

food_x = 10  
food_y = 10  

# Создаем окно для отображения игры
display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")  
clock = pygame.time.Clock()  
background = pygame.image.load("fon_snake.png")  
background = pygame.transform.scale(background, (500, 500))

# Определяем цвета
background_top = (0, 0, 50)  
background_bottom = (0, 0, 0)  
snake_colour = (255, 137, 0)  
food_colour = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))  
snake_head = (255, 247, 0)  
font_colour = (255, 255, 255)  
defeat_colour = (255, 0, 0)  

# Класс Snake
class Snake:
    def __init__(self, x_start, y_start):
        self.x = x_start  
        self.y = y_start  
        self.w = 15  
        self.h = 15  
        self.x_dir = 1  
        self.y_dir = 0  
        self.history = [[self.x, self.y]]  
        self.length = 1  

    def reset(self):
        self.x = 500 / 2 - scale  
        self.y = 500 / 2 - scale  
        self.w = 15  
        self.h = 15  
        self.x_dir = 1  
        self.y_dir = 0  
        self.history = [[self.x, self.y]]  
        self.length = 1  

    def show(self):
        for i in range(self.length):
            if not i == 0:
                pygame.draw.rect(display, snake_colour, (self.history[i][0], self.history[i][1], self.w, self.h))
            else:
                pygame.draw.rect(display, snake_head, (self.history[i][0], self.history[i][1], self.w, self.h))

    def check_eaten(self, food_x, food_y, scale):
        if abs(self.history[0][0] - food_x) < scale and abs(self.history[0][1] - food_y) < scale:
            return True
        return False

    def check_level(self):
        global level
        if self.length % 5 == 0:
            return True

    def grow(self):
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < self.w and abs(self.history[0][1] - self.history[i][1]) < self.h and self.length > 2:
                return True
            i -= 1

    def update(self):
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i - 1])
            i -= 1
        self.history[0][0] += self.x_dir * scale
        self.history[0][1] += self.y_dir * scale


# Класс Food
class Food:
    def __init__(self):
        self.food_x = random.randrange(1, int(500 / scale) - 1) * scale
        self.food_y = random.randrange(1, int(500 / scale) - 1) * scale
        self.weight = random.randint(1, 5)  # Случайный вес еды (от 1 до 5)
        self.timer = time.time()  # Время появления еды

    def new_location(self):
        self.food_x = random.randrange(1, int(500 / scale) - 1) * scale
        self.food_y = random.randrange(1, int(500 / scale) - 1) * scale
        self.weight = random.randint(1, 5)  # Случайный вес
        self.timer = time.time()  # Обновляем таймер появления еды

    def show(self):
        # Отображаем еду, если она не исчезла (таймер больше 5 секунд)
        if time.time() - self.timer < 5:
            pygame.draw.rect(display, food_colour, (self.food_x, self.food_y, scale, scale))

    def is_expired(self):
        return time.time() - self.timer >= 5


# Функция для отображения счета игрока
def show_score():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: " + str(score), True, font_colour)
    display.blit(text, (scale, scale))

# Функция для отображения уровня игры
def show_level():
    font = pygame.font.SysFont(None, 20)
    text = font.render("Level: " + str(level), True, font_colour)
    display.blit(text, (90 - scale, scale))

# Основной цикл игры
def gameLoop():
    global score
    global level
    global SPEED

    snake = Snake(500 / 2, 500 / 2)  
    food = Food()  # Создаем объект еды

    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                sys.exit()  
            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_q:  
                    pygame.quit()  
                    sys.exit()  
                if snake.y_dir == 0:  
                    if event.key == pygame.K_UP:  
                        snake.x_dir = 0  
                        snake.y_dir = -1  
                    if event.key == pygame.K_DOWN:  
                        snake.x_dir = 0  
                        snake.y_dir = 1  

                if snake.x_dir == 0:  
                    if event.key == pygame.K_LEFT:  
                        snake.x_dir = -1  
                        snake.y_dir = 0  
                    if event.key == pygame.K_RIGHT:  
                        snake.x_dir = 1  
                        snake.y_dir = 0  

        display.blit(background, (0, 0))  
        snake.show()  # Отображаем змейку
        snake.update()  # Обновляем положение змейки
        food.show()  # Отображаем еду
        show_score()  # Отображаем счет
        show_level()  # Отображаем уровень

        if snake.check_eaten(food.food_x, food.food_y, scale):  # Если змейка съела еду
            score += food.weight  # Добавляем вес еды к счету
            food.new_location()  # Устанавливаем новую позицию еды
            snake.grow()  # Увеличиваем длину змейки

        if snake.check_level():  # Если достигнут новый уровень
            food.new_location()  # Устанавливаем новую позицию еды
            level += 1  # Увеличиваем уровень
            SPEED += 1  # Увеличиваем скорость змейки
            snake.grow()  # Увеличиваем длину змейки

        if snake.death():  # Если змейка столкнулась с хвостом
            score = 0  
            level = 0  
            font = pygame.font.SysFont(None, 100)  
            text = font.render("Game Over!", True, defeat_colour)  
            display.blit(text, (50, 200))  
            pygame.display.update()  
            time.sleep(3)  
            snake.reset()  # Сбрасываем змейку

        if snake.history[0][0] > 500:  
            snake.history[0][0] = 0  
        if snake.history[0][0] < 0:  
            snake.history[0][0] = 500  
        if snake.history[0][1] > 500:
            snake.history[0][1] = 0
        if snake.history[0][1] < 0:
            snake.history[0][1] = 500

        # Если еда исчезла, генерируем новую
        if food.is_expired():
            food.new_location()

        pygame.display.update()  
        clock.tick(SPEED)  

gameLoop()  # Запуск игры
