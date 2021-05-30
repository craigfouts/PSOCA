import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS
from random import randrange

class VacancyCA:

    def __init__(self, initial, goal, cell_size=10):
        self.initial = initial
        self.goal = goal
        self.cell_size = cell_size
        self.state = self.initial.copy()
        self.window_width = self.state.shape[1] * self.cell_size
        self.window_height = self.state.shape[0] * self.cell_size

    def _draw_cell(self, x1, y1):
        x1, y1 = y1, self.window_height - x1
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        graphics.draw_indexed(4, gl.GL_TRIANGLES, indicies, data)

    def _get_vacancies(self, initial, goal):
        vacancies = []
        for index, cell in np.ndenumerate(goal):
            if cell == 1 and initial[index] == 0:
                vacancies.append(index)
        return np.array(vacancies)

    def _get_sources(self, initial, goal):
        sources = []
        for index, cell in np.ndenumerate(goal):
            if cell == 0 and initial[index] == 1:
                sources.append(index)
        return np.array(sources)

    def _get_neighbors(self, cell, collection):
        neighbors = []
        for shift in zip([0, 1, 0, -1], [1, 0, -1, 0]):
            if collection[cell[0] + shift[0], cell[1] + shift[1]] == 1:
                neighbors.append([cell[0] + shift[0], cell[1] + shift[1]])
        return np.array(neighbors)

    def _swap_cell_values(self, cell1, cell2, collection):
        temp = collection[cell1[0], cell1[1]]
        collection[cell1[0], cell1[1]] = collection[cell2[0], cell2[1]]
        collection[cell2[0], cell2[1]] = temp
        return collection

    def _source_sum(self, cell, sources):
        sum = 0
        for source in sources:
            sum += abs(source[0] - cell[0]) + abs(source[1] - cell[1])
        return sum

    def _select_neighbor(self, neighbors, state, goal):
        neighbor = neighbors[0]
        sources = self._get_sources(state, goal)
        for neighbor_ in neighbors:
            if self._source_sum(neighbor_, sources) < self._source_sum(neighbor, sources):
                neighbor = neighbor_
        return neighbor

    def fit(self, initial, goal):
        state = initial.copy()
        while (state != goal).any():
            targets = self._get_targets(state, goal)
            print('Targets:\n', targets)
            for target in targets:
                # print(f'{target}:\n', self._get_neighbors(target, initial))
                neighbors = self._get_neighbors(target, state)
                if len(neighbors) > 0:
                    neighbor = neighbors[randrange(len(neighbors))]
                    self._swap_cell_values(target, neighbor, state)
                print('State:\n', state)
        return None

    def update(self):
        targets = self._get_vacancies(self.state, self.goal)
        for target in targets:
            neighbors = self._get_neighbors(target, self.state)
            if len(neighbors) > 0:
                neighbor = self._select_neighbor(neighbors, self.state, self.goal)
                self._swap_cell_values(target, neighbor, self.state)

    def draw(self):
        for cell, i in np.ndenumerate(self.state):
            [row, col] = cell
            if i == 1:
                self._draw_cell(row * self.cell_size, col * self.cell_size)

    def run(self):
        pass


if __name__ == '__main__':
    initial = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    goal = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    a_star_ca = VacancyCA()
    a_star_ca.fit(initial, goal)
