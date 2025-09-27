import random
from grid import Grid
from block import *
import os
import pygame


class Game():
    def __init__(self, base_path):
        self.grid = Grid()
        self.blocks = []
        self.generated_block = self.return_block()
        self.next_block = self.return_block()
        self.game_over = False
        self.score = 0
        self.clear_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "cleared.mp3"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(base_path, "sounds", "gameover.mp3"))
        self.clear_sound.set_volume(0.5)

        pygame.mixer.music.load(os.path.join(base_path, "sounds", "music.mp3"))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def refill_bag(self):
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        random.shuffle(self.blocks)

    def return_block(self):
        if not self.blocks:
            self.refill_bag()

        return self.blocks.pop()

    def reset(self):
        self.grid.reset()
        self.score = 0

    def draw(self, screen):
        self.grid.draw(screen)
        self.grid.draw_effects(screen)
        self.generated_block.draw(screen, 0, 0)
        self.next_block.draw(screen, 240, 270)

    def block_inside(self):
        tiles = self.generated_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def lock_block(self):
        tiles = self.generated_block.get_cell_positions()
        for tile in tiles:
            self.grid.grid[tile.row][tile.column] = self.generated_block.id
        self.generated_block = self.next_block
        self.next_block = self.return_block()
        rows_cleared = self.grid.clearer()
        if rows_cleared > 0:
            self.update_score(rows_cleared, 0)
            self.clear_sound.play()
        if not self.block_fits():
            self.game_over = True
            self.game_over_sound.play()

    def block_fits(self):
        tiles = self.generated_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate_block(self):
        self.generated_block.rotation()

        if not self.block_inside() or not self.block_fits():
            self.generated_block.undo_rotation()

    def move_down(self):
        self.generated_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.generated_block.move(-1, 0)
            self.lock_block()

    def move_left(self):
        self.generated_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.generated_block.move(0, 1)

    def move_right(self):
        self.generated_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.generated_block.move(0, -1)
