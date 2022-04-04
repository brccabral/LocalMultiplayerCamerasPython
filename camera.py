import pygame
from player import Player
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from typing import Tuple


class Camera:
    def __init__(self, player: Player, screen_pos: Tuple[int, int]):
        self.offset = pygame.Vector2()
        self.center_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 // 2)
        self.player = player
        self.screen_pos = screen_pos
        self.camera_surface = pygame.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))

    def center_target_camera(self):
        self.offset = self.center_pos - self.player.pos

    def update(self, scene_surface: pygame.Surface):
        self.camera_surface.fill("red")
        self.center_target_camera()
        self.camera_surface.blit(scene_surface, self.offset)
