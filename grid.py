import pygame
from colors import Colors
from block import Block, sfx


class Grid:
    def __init__(self):
        self.rows = 20
        self.columns = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.columns)] for i in range(self.rows)]
        self.cell_colors = Colors.get_cell_colors()
        self.effects = []

    def reset(self):
        self.grid = [[0 for j in range(self.columns)] for i in range(self.rows)]

    def is_inside(self, row, column):
        if row >= 0 and row < self.rows and column >= 0 and column < self.columns:
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def row_is_full(self, row):
        for column in range(self.columns):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.columns):
            self.grid[row][column] = 0

    def push_row_down(self, row, number_rows):
        for column in range(self.columns):
            self.grid[row + number_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clearer(self):
        completed = 0

        for row in range(self.rows - 1, -1, - 1):
            if self.row_is_full(row):
                for col in range(self.columns):
                    cell_value = self.grid[row][col]
                    if cell_value != 0:
                        image = Block.images[cell_value]
                        pos = (col * self.cell_size, row * self.cell_size)
                        self.effects.append(sfx(pos, image))
                self.clear_row(row)
                completed += 1

            elif completed > 0:
                self.push_row_down(row, completed)

        return completed

    def update_effects(self, dt):
        for effect in self.effects[:]:
            effect.run(dt)
            if effect.end_time():
                self.effects.remove(effect)

    def draw_effects(self, screen):
        for effect in self.effects:
            screen.blit(effect.image, effect.pos)

    def draw(self, screen):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column * self.cell_size,
                                        row * self.cell_size,
                                        self.cell_size, self.cell_size)
                if cell_value != 0:
                    image = Block.images[cell_value]
                    screen.blit(image, cell_rect.topleft)
                else:
                    pygame.draw.rect(screen,
                    self.cell_colors[0],  
                    cell_rect)

                pygame.draw.rect(screen, (60, 60, 80), cell_rect, 1)