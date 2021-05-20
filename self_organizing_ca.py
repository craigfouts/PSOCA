import numpy as np
import pyglet


class SelfOrganizingCA:

    def __init__(self, width, height, cell_size, percent_fill):
        self.grid_width = int(600 / 50)
        self.grid_height = int(600 / 50)
        self.cell_size = 50
        self.cells = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.agents = []
        self._set_agents()

    def _set_agents(self):
        self.agents = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] > 0:
                    self.agents.append([row, col])

    def _draw_cell(self, x1, y1):
        y1 = 600 - y1
        x1 += self.cell_size
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, indicies, data)

    def draw(self):
        # for row in range(self.grid_height):
        #     for col in range(self.grid_width):
        #         if self.cells[row][col] > 0:
        #             self._draw_cell(row * self.cell_size, col * self.cell_size)
        for agent in self.agents:
            col, row = agent[0], agent[1]
            self._draw_cell(row * self.cell_size, col * self.cell_size)

    def _get_cell(self, row, col):
        if row < 0 or row >= self.grid_width or col < 0 or col >= self.grid_height:
            return 0
        return self.cells[row][col]

    def _get_percept(self, row, col):
        percept = []
        for i in [-1, 0, 1]:
            percept.append([0, 0, 0])

        for idx_i, i in enumerate([-1, 0, 1]):
            for idx_j, j in enumerate([-1, 0, 1]):
                percept[idx_i][idx_j] = self._get_cell(row + i, col + j)
                
        return percept

    def _apply_rule(self, row, col, percept):

        if percept == [[0, 0, 0],
                       [0, 1, 1],
                       [0, 1, 1]] and row != 6:
            self.cells[row][col] = 0
            self.cells[row + 1][col - 1] = 1
        elif percept == [[0, 0, 0],
                         [0, 1, 1],
                         [0, 0, 1]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 1],
                         [0, 1, 1],
                         [0, 0, 1]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 1],
                         [0, 1, 1],
                         [0, 0, 2]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 0],
                         [0, 1, 1],
                         [1, 1, 1]]:
            self.cells[row][col] = 0
            self.cells[row][col - 1] = 1
        elif percept == [[0, 1, 0],
                         [0, 1, 1],
                         [0, 0, 1]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 1, 0],
                         [0, 1, 1],
                         [0, 0, 2]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 1, 1],
                         [0, 1, 1],
                         [0, 0, 1]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 1, 1],
                         [0, 1, 1],
                         [0, 0, 2]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 0],
                         [0, 1, 0],
                         [1, 1, 1]]:
            self.cells[row][col] = 0
            self.cells[row][col - 1] = 1
        elif percept == [[0, 0, 0],
                         [0, 1, 0],
                         [1, 1, 0]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col + 1] = 1
        elif percept == [[0, 0, 0],
                         [1, 1, 0],
                         [1, 0, 0]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col] = 1
        elif percept == [[0, 0, 0],
                         [1, 1, 0],
                         [1, 1, 1]]:
            self.cells[row][col] = 0
            self.cells[row][col + 1] = 1
        elif percept == [[0, 0, 0],
                         [1, 1, 0],
                         [0, 0, 0]]:
            self.cells[row][col] = 0
            self.cells[row + 1][col - 1] = 1
        # Give each agent its own ruleset?

    def run_rules(self):
        # temp = []
        # for row in range(self.grid_height):
        #     temp.append([])
        #     for col in range(self.grid_width):
        #         percept = self._get_percept(row, col)
        #         self._apply_rule(row, col, percept)
        for agent in self.agents:
            row, col = agent[0], agent[1]
            percept = self._get_percept(row, col)
            self._apply_rule(row, col, percept)
        self._set_agents()
