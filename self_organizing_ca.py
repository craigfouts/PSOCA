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
                      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def _draw_cell(self, x1, y1):
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, indicies, data)

    def draw(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] > 0:
                    self._draw_cell(row * self.cell_size, col * self.cell_size)

    def run_rules(self):
        pass
