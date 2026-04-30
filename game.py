import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple
import sys

# Инициализируем шрифты
pygame.font.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 15 

class SnakeGameAI:
    def __init__(self, w=640, h=480, headless=False):
        self.w = w
        self.h = h
        self.headless = headless
        if not self.headless:
            self.display = pygame.display.set_mode((self.w, self.h))
            pygame.display.set_caption('Snake AI')
        else:
            self.display = pygame.Surface((self.w, self.h))
            
        self.clock = pygame.time.Clock()
        self.level = 1
        self.last_reward = 0 
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]
        self.score = 0
        self.gift = None
        self.exit = None
        self._place_items()
        self.frame_iteration = 0
        self.last_reward = 0

    def _place_items(self):
        # --- ВОТ ТУТ ИЗМЕНЕНИЕ: Точка теперь стоит на месте ---
        self.gift = Point(400, 300) 
        self.exit = Point(0, 0)

    def play_step(self, action):
        self.frame_iteration += 1
        if not self.headless:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        self.clock.tick(SPEED)
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = -0.1
        game_over = False
        
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            self.last_reward = reward
            self._draw_elements()
            if not self.headless: pygame.display.flip()
            pygame.time.delay(500)
            self.level = 1
            return reward, game_over, self.score

        if self.head == self.gift:
            self.score += 1
            reward = 10
            self.last_reward = reward
            self._draw_elements()
            if not self.headless: pygame.display.flip()
            pygame.time.delay(500)
            # Мы вызываем _place_items, но теперь она всегда ставит точку в то же место
            self._place_items()
        else:
            self.snake.pop()

        if self.head == self.exit:
            reward = 50
            self.last_reward = reward
            self._draw_elements()
            if not self.headless: pygame.display.flip()
            pygame.time.delay(800)
            self.level += 1
            game_over = True
            
        self.last_reward = reward
        self._draw_elements()
        if not self.headless: pygame.display.flip()
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None: pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _draw_elements(self):
        self.display.fill((0, 0, 0))
        for pt in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.gift.x, self.gift.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, (0, 0, 255), pygame.Rect(self.exit.x, self.exit.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text_info = font.render(f"LVL: {self.level} | Score: {self.score}", True, (255, 255, 255))
        self.display.blit(text_info, [20, self.h - 40])

        color = (0, 255, 0) if self.last_reward > 0 else (255, 70, 70)
        if self.last_reward == -0.1: color = (150, 150, 150)
        reward_text = font.render(f"Step Reward: {self.last_reward}", True, color)
        self.display.blit(reward_text, [self.w - 250, self.h - 40])

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]): new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]): new_dir = clock_wise[(idx + 1) % 4]
        else: new_dir = clock_wise[(idx - 1) % 4]
        self.direction = new_dir
        x, y = self.head.x, self.head.y
        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: y += BLOCK_SIZE
        elif self.direction == Direction.UP: y -= BLOCK_SIZE
        self.head = Point(x, y)

if __name__ == '__main__':
    from agent import Agent
    game = SnakeGameAI(headless=False)
    agent = Agent()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        if done: game.reset()
