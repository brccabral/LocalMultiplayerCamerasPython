import pygame
import random
from settings import GAME_SCENE_WIDTH, GAME_SCENE_HEIGHT


class Player:
    def __init__(
        self,
        name: str = "P1",
        color: pygame.color.Color = "blue",
        left_key: int = pygame.K_a,
        right_key: int = pygame.K_d,
        up_key: int = pygame.K_w,
        down_key: int = pygame.K_s,
    ):
        # setup
        self.name = name
        self.color = color
        self.speed = 60

        # position
        self.pos = pygame.Vector2(
            random.randint(20, GAME_SCENE_WIDTH - 20),
            random.randint(20, GAME_SCENE_HEIGHT - 20),
        )
        self.direction = pygame.Vector2(0, 0)

        # control
        self.left_key = left_key
        self.right_key = right_key
        self.up_key = up_key
        self.down_key = down_key

    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.move_left(dt)
        if keys[self.right_key]:
            self.move_right(dt)
        if keys[self.up_key]:
            self.move_up(dt)
        if keys[self.down_key]:
            self.move_down(dt)

    def move_left(self, dt: float):
        self.direction -= pygame.Vector2(self.speed * dt, 0)

    def move_right(self, dt: float):
        self.direction += pygame.Vector2(self.speed * dt, 0)

    def move_up(self, dt: float):
        self.direction -= pygame.Vector2(0, self.speed * dt)

    def move_down(self, dt: float):
        self.direction += pygame.Vector2(0, self.speed * dt)

    def update(self, dt: float):
        self.player_input(dt)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction
        self.direction = pygame.Vector2(0, 0)
