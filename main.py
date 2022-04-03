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
    def __init__(self, name: str, color: pygame.color.Color):
        super().__init__()
        self.name = name
        self.color = color
        self.speed = 60

        self.pos = pygame.Vector2(random.randint(20, 620), 10)
        self.direction = pygame.Vector2(0, 0)

    def player_input(self, dt: float):
        pass

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


class Player1(Player):
    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_left(dt)
        if keys[pygame.K_d]:
            self.move_right(dt)
        if keys[pygame.K_w]:
            self.move_up(dt)
        if keys[pygame.K_s]:
            self.move_down(dt)


class Player2(Player):
    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.move_left(dt)
        if keys[pygame.K_l]:
            self.move_right(dt)
        if keys[pygame.K_i]:
            self.move_up(dt)
        if keys[pygame.K_k]:
            self.move_down(dt)


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
        self.player1 = Player1("P1", "blue")
        self.player2 = Player2("P2", "orange")
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
