import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS


class VacancyCA:

    def __init__(self, initial, goal, cell_size=10):
        self.initial = initial
        self.goal = goal
        self.cell_size = cell_size
        self.state = self.initial.copy()
        self.vacancies = np.array([])
        self.sources = np.array([])
        self.window_width = self.state.shape[1] * self.cell_size
        self.window_height = self.state.shape[0] * self.cell_size
        self._initialize_vacancies()

    def _initialize_vacancies(self):
        vacancies = []
        for index, cell in np.ndenumerate(self.initial):
            if cell == 0 and self.goal[index] == 1:
                vacancies.append(index)
        self.vacancies = np.array(vacancies)
        print(self.vacancies)

    def _set_sources(self):
        sources = []
        for index, cell in np.ndenumerate(self.state):
            if cell == 1 and self.goal[index] == 0:
                sources.append(index)
        self.sources = np.array(sources)

    def _in_grid(self, value):
        return 0 <= value and value < self.window_width

    def _get_neighbors(self, cell):
        neighbors = []
        for shift in zip([0, 1, 0, -1], [1, 0, -1, 0]):
            row, col = cell[0] + shift[0], cell[1] + shift[1]
            if self._in_grid(row) and self._in_grid(col):
                neighbors.append([row, col])
        print(neighbors)
        return np.array(neighbors) if len(neighbors) > 0 else None

    def _get_value(self, cell):
        value = np.inf
        for source in self.sources:
            dist = np.sum(np.abs(source - cell))
            value = dist if dist < value else value
        return value

    def _get_replacement(self, neighbors):
        replacement = neighbors[0]
        for neighbor in neighbors:
            if self._get_value(neighbor) < self._get_value(replacement):
                replacement = neighbor
        return replacement

    def _swap_vacancy(self, vacancy, replacement):
        print('Vacancy:', vacancy)
        print('Replacement:', replacement)
        self.state[vacancy[0], vacancy[1]] = 1
        self.state[replacement[0], replacement[1]] = 0
        vacancies = self.vacancies.tolist()
        vacancies.remove(vacancy.tolist())
        vacancies.append(replacement.tolist())
        self.vacancies = np.array(vacancies)

    def _goal_test(self):
        for vacancy in self.vacancies:
            if self.goal[vacancy[0], vacancy[1]] == 1:
                return True
        return False

    def update(self):
        if self._goal_test():
            for vacancy in self.vacancies:
                neighbors = self._get_neighbors(vacancy)
                if neighbors is not None:
                    replacement = self._get_replacement(neighbors)
                    self._swap_vacancy(vacancy, replacement)

    def _draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = self.window_height - row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2 ,y2))
        graphics.draw_indexed(4, gl.GL_TRIANGLES, indicies, data)

    def draw(self):
        for index, cell in np.ndenumerate(self.state):
            self._draw_cell(*index) if cell == 1 else None
