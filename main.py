import random
import sys
from types import TracebackType
from typing import List
import pygame


def debug(message: str):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "white")
    screen.blit(text, [10, 10])


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
        self.pos = pygame.Vector2(random.randint(20, 620), 10)
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


class GameScene:
    def __init__(self, players: List[Player]):
        self.scene_surface = pygame.Surface((1280, 240))
        self.players = players

    def update(self, dt: float):
        for player in self.players:
            player.update(dt)


class Scene1(GameScene):
    def __init__(self, players: List[Player]):
        super().__init__(players)

        self.bg = pygame.Surface((1280, 240))

        ar = pygame.PixelArray(self.bg)
        for x in range(1280):
            c = x / 1280 * 255
            r, g, b = c, c, c
            ar[x, :] = (r, g, b)

    def update(self, dt: float):
        super().update(dt)
        self.scene_surface.blit(self.bg, (0, 0))
        for player in self.players:
            pygame.draw.rect(
                self.scene_surface, player.color, (player.pos[0], player.pos[1], 30, 30)
            )
        GameWindow().window_surface.blit(self.scene_surface, (0, 0))
        GameWindow().window_surface.blit(self.scene_surface, (0, 240))
        debug(player.pos)


class GameWindow:
    instance = None

    def __new__(cls, *args, **kwds):
        """Return an open Pygame window"""

        if GameWindow.instance is not None:
            return GameWindow.instance
        self = object.__new__(cls)
        pygame.init()
        self.window_surface = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.player1 = Player()
        self.player2 = Player(
            "P2", "orange", pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k
        )
        self.set_scene()
        GameWindow.instance = self
        return self

    def __enter__(self):
        return self

    def __exit__(
        self, exc_type: type, exc_value: Exception, exc_traceback: TracebackType
    ):
        self.close()
        return False

    def close(self):
        pygame.quit()
        GameWindow.instance = None

    def set_scene(self):
        self.scene = Scene1([self.player1, self.player2])

    def run(self):
        dt = 0.0
        while True:
            self.window_surface.fill("black")

            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene.update(dt)

            pygame.display.update()
            dt = self.clock.tick(60) / 1000


if __name__ == "__main__":
    with GameWindow() as game:
        game.run()
