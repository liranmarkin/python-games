#!/usr/bin/python3
import pygame
import random
UNIT_SIZE = 30
DELAY_START = 300
DELAY_MIN = 50
DELAY_DOWN_RATE = 2

pygame.init()
width, height = 30, 20
size = width * UNIT_SIZE, height * UNIT_SIZE
window = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
WINDOW_BACKGROUND = (0x19, 0x19, 0x19)
LINK_SURFACE = pygame.Surface((UNIT_SIZE - 2, UNIT_SIZE - 2))
LINK_SURFACE.fill((0xE5, 0x8F, 0x65))
HEAD_SURFACE = pygame.Surface.copy(LINK_SURFACE)
HEAD_SURFACE.fill((0x63, 0x37, 0x2C))

FOOD_SURFACE = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
FOOD_SURFACE.fill((0xE1, 0xF4, 0xCB))

class GameOverException(BaseException):
    pass

class Snake:
    def __init__(self, x, y):
        self.links = [pygame.Rect(1 + x * UNIT_SIZE, 1 + y * UNIT_SIZE, UNIT_SIZE - 2, UNIT_SIZE - 2)]
        self.direction = [1, 0]
        self.next_direction = [1, 0]
        self.grow = False

    def collides(self, obj):
        return any(link.colliderect(obj) for link in self.links)

    def get_length(self):
        return len(self.links)

    def try_eat(self, obj):
        if self.collides(obj):
            self.grow = True
            return True
        return False

    def apply_key(self, key):
        if key == pygame.K_LEFT and self.direction[0] != 1:
            self.next_direction = [-1, 0]
        elif key == pygame.K_RIGHT and self.direction[0] != -1:
            self.next_direction = [1, 0]
        elif key == pygame.K_UP and self.direction[1] != 1:
            self.next_direction = [0, -1]
        elif key == pygame.K_DOWN and self.direction[1] != -1:
            self.next_direction = [0, 1]

    def _validate(self, new_link):
        if new_link in self.links or new_link[0] < 0 or new_link[0] >= size[0] or new_link[1] < 0 or new_link[1] >= size[1]:
            raise GameOverException()

    def move(self):
        self.direction = self.next_direction
        new_link = self.links[0].move([x * UNIT_SIZE for x in self.direction])
        if not self.grow:
            self.links.pop()
        self._validate(new_link)
        self.links.insert(0, new_link)
        self.grow = False

    def draw(self, window):
        for link in self.links[1:]:
            window.blit(LINK_SURFACE, link)
        window.blit(HEAD_SURFACE, self.links[0])

def make_random_food(snake):
    food = None
    while food is None or snake.collides(food):
        food = pygame.Rect(
            random.randint(0, width - 1) * UNIT_SIZE,
            random.randint(0, height - 1) * UNIT_SIZE,
            UNIT_SIZE,
            UNIT_SIZE
        )
    return food
    

snake = Snake(width // 2, height // 2)


def loop():
    food = make_random_food(snake)
    delay_milliseconds = DELAY_START
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return
            if event.type == pygame.KEYDOWN:
                snake.apply_key(event.key)

        snake.move()
        if snake.try_eat(food):
            delay_milliseconds = max(delay_milliseconds - DELAY_DOWN_RATE, DELAY_MIN)
            food = make_random_food(snake)

        window.fill(WINDOW_BACKGROUND)
        snake.draw(window)
        window.blit(FOOD_SURFACE, food)
        pygame.display.update()
        pygame.time.delay(delay_milliseconds)

try:
    loop()
except GameOverException:
    print('Game Over :)')
    print('Your score was: {}'.format(snake.get_length() - 1))
    pygame.time.delay(2000)
pygame.quit()