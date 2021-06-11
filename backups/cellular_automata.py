import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS

class CellularAutomata:

    def __init__(self, cell_map, cell_size):
        self.cell_map = cell_map
        self.temp_map = self.cell_map.copy()
        self.cell_size = cell_size
        self.grid_width = self.cell_map.shape[1]
        self.grid_height = self.cell_map.shape[0]
        self.window_width = self.cell_map.shape[1] * self.cell_size
        self.window_height = self.cell_map.shape[0] * self.cell_size
        rules = np.array([np.array([[0, 0, 0],
                                    [0, 1, 1],
                                    [0, 1, 1]], dtype='int8').tobytes(),
                          np.array([[0, 0, 0],
                                    [0, 1, 1],
                                    [0, 0, 1]], dtype='int8').tobytes(),
                          np.array([[0, 0, 1],
                                    [0, 1, 1],
                                    [0, 0, 1]], dtype='int8').tobytes(),
                          np.array([[0, 0, 1],
                                    [0, 1, 1],
                                    [0, 0, 0]], dtype='int8').tobytes(),
                          np.array([[0, 0, 0],
                                    [0, 1, 1],
                                    [1, 1, 1]], dtype='int8').tobytes(),
                          np.array([[0, 0, 0],
                                    [0, 1, 0],
                                    [1, 1, 1]], dtype='int8').tobytes(),
                          np.array([[0, 0, 0],
                                    [0, 1, 0],
                                    [0, 1, 1]], dtype='int8').tobytes()])
        self.rule_map = {
            rules[0]: lambda a: self._move_agent(a, 1, -1, 1),
            rules[1]: lambda a: self._move_agent(a, 1, 0, 1),
            rules[2]: lambda a: self._move_agent(a, 1, 0, 1),
            rules[3]: lambda a: self._move_agent(a, 0, 0, 2),
            rules[4]: lambda a: self._move_agent(a, 0, -1, 1),
            rules[5]: lambda a: self._move_agent(a, 0, -1, 1),
            rules[6]: lambda a: self._move_agent(a, 1, -1, 1)
        }
        self.agents = np.array([], dtype='int8')
        self._set_agents()

    def _move_agent(self, agent, dr, dc, val):
        self.temp_map[agent[0], agent[1]] = 0
        self.temp_map[agent[0] + dr, agent[1] + dc] = val

    def _add_agent(self, agent):
        self.agents = np.append(self.agents, agent)

    def _set_agents(self):
        self.agents = np.array([], dtype='int8')
        for index, cell in np.ndenumerate(self.cell_map):
            self._add_agent(index) if cell > 0 else None
        rows = self.agents.shape[0]
        self.agents = self.agents.reshape(int(rows / 2), 2)

    def _in_grid(self, row, col):
        return row in range(self.grid_height) and col in range(self.grid_width)

    def _get_cell(self, row, col):
        return self.cell_map[row, col] if self._in_grid(row, col) else 0

    def _get_percept(self, agent):
        percept = np.zeros((3, 3), dtype='int8')
        for row, i in enumerate([-1, 0, 1]):
            for col, j in enumerate([-1, 0, 1]):
                percept[row, col] = self._get_cell(agent[0] + i, agent[1] + j)
        return percept

    def _draw_cell(self, x1, y1):
        x1, y1 = y1, self.window_height - x1
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        graphics.draw_indexed(4, gl.GL_TRIANGLES, indicies, data)

    def update(self):
        for agent in self.agents:
            percept = self._get_percept(agent)
            try:
                self.rule_map[percept.tobytes()](agent)
            except:
                pass
        self.cell_map = self.temp_map.copy()
        self._set_agents()

    def draw(self):
        for agent in self.agents:
            [row, col] = agent
            self._draw_cell(row * self.cell_size, col * self.cell_size)
