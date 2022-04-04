import pygame
from typing import List
from player import Player
from settings import GAME_SCENE_WIDTH, GAME_SCENE_HEIGHT


class GameScene:
    def __init__(self, players: List[Player]):
        self.scene_surface = pygame.Surface((GAME_SCENE_WIDTH, GAME_SCENE_HEIGHT))
        self.players = players

    def update(self, dt: float):
        for player in self.players:
            player.update(dt)


class Scene1(GameScene):
    def __init__(self, players: List[Player]):
        super().__init__(players)

        self.bg = pygame.Surface(self.scene_surface.get_size())

        ar = pygame.PixelArray(self.bg)
        for x in range(self.bg.get_width()):
            c = x / self.bg.get_width() * 255
            r, g, b = c, c, c
            ar[x, :] = (r, g, b)

    def update(self, dt: float):
        super().update(dt)
        self.scene_surface.fill("green")
        self.scene_surface.blit(self.bg, (0, 0))
        for player in self.players:
            pygame.draw.rect(
                self.scene_surface, player.color, (player.pos[0], player.pos[1], 30, 30)
            )
