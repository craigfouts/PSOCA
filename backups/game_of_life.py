import pyglet
import random as rand


class GameOfLife:

    def __init__(self, window_width, window_height, cell_size, percent_fill):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.fill = percent_fill
        self.cells = []
        self.generate_cells()

    def generate_cells(self):
        for row in range(self.grid_height):
            self.cells.append([])
            for _ in range(self.grid_width):
                self.cells[row].append(1 if rand.random() < self.fill else 0)

    def _draw_cell(self, x1, y1):
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, indicies, data)

    def draw(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 1:
                    self._draw_cell(row * self.cell_size, col * self.cell_size)

    def _in_height_range(self, row):
        return row >= 0 and row < self.grid_width

    def _in_width_range(self, col):
        return col >= 0 and col < self.grid_width

    def _in_grid(self, row, col):
        return self._in_height_range(row) and self._in_width_range(col)

    def _get_cell_value(self, row, col):
        return self.cells[row][col] if self._in_grid(row, col) else 0

    def _get_neighbor_count(self, row, col):
        return sum([self._get_cell_value(row - 1, col - 1),
                    self._get_cell_value(row - 1, col),
                    self._get_cell_value(row - 1, col + 1),
                    self._get_cell_value(row, col - 1),
                    self._get_cell_value(row, col + 1),
                    self._get_cell_value(row + 1, col - 1),
                    self._get_cell_value(row + 1, col),
                    self._get_cell_value(row + 1, col + 1)])

    def run_rules(self):
        temp = []
        for row in range(self.grid_height):
            temp.append([])
            for col in range(self.grid_width):
                neighbors = self._get_neighbor_count(row, col)
                if self.cells[row][col] == 0 and neighbors == 3:
                    temp[row].append(1)
                elif self.cells[row][col] == 1 and neighbors in (2, 3):
                    temp[row].append(1)
                else:
                    temp[row].append(0)
        self.cells = temp
