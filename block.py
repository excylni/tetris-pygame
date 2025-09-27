import pygame
import os
from colors import Colors
import sys
import random


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  


SPRITE_DIR_PATH = os.path.join(base_path, "tetriminos")


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Block:
    images = None

    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.row_offset = 0
        self.column_offset = 0
        self.color = Colors.get_cell_colors()
        self.move(0, 4)

        if Block.images is None:
            Block.images = self.load_images()

    def load_images(self):
        files = sorted([i for i in os.listdir(SPRITE_DIR_PATH) if i.endswith(".png")])
        images = [pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)]  
        for file in files:
            full_path = os.path.join(SPRITE_DIR_PATH, file) 
            img = pygame.image.load(full_path).convert_alpha()
            img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
            images.append(img)
        return images

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()

        for tile in tiles:
            image = Block.images[self.id]
            screen.blit(image, (tile.column * self.cell_size + offset_x,
                                tile.row * self.cell_size + offset_y))

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def rotation(self):
        self.rotation_state = (self.rotation_state + 1) % 4

    def undo_rotation(self):
        self.rotation_state = (self.rotation_state - 1) % 4

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset,
                                position.column + self.column_offset)
            moved_tiles.append(position)

        return moved_tiles


class sfx:
    def __init__(self, initial_pos, image):
        self.original_image = image.copy()
        self.original_image.set_alpha(200)

        self.pos = pygame.Vector2(initial_pos)
        self.speed = random.uniform(3500, 4000)
        self.cycles = random.randrange(2, 3)
        self.rotation_speed = random.uniform(180, 360)
        self.angle = 0
        self.cycle_counter = 0
        self.elapsed = 0

    def run(self, dt):
        self.elapsed += dt
        self.pos.y -= self.speed * dt

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.angle += self.rotation_speed * dt

    def end_time(self):
        return self.elapsed > 0.035


class LBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }


class JBlock(Block):
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }


class IBlock(Block):
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 0)


class OBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            1: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            2: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            3: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }


class SBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }


class TBlock(Block):
    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }


class ZBlock(Block):
    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }