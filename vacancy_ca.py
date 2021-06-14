import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS


class VacancyCA:

    def __init__(self, initial, goal, cell_size, window_width, window_height):
        self.initial = initial
        self.goal = goal
        self.cell_size = cell_size
        self.window_width = window_width
        self.window_height = window_height
        self.state = self.initial.copy()
        self.sources = np.array([])
        self.targets = np.array([[-1, -1]])
        self.vacancies = np.array([])
        self._initialize()

    def _initialize(self):
        self._set_sources()
        self._set_vacancies()
        self._sort_vacancies('descending')
        self._map_targets()
        # self._sort_vacancies('ascending')

    def _set_sources(self):
        sources = []
        for index, cell in np.ndenumerate(self.state):
            if cell == 1 and self.goal[index] == 0:
                sources.append(index)
        self.sources = np.array(sources)

    def _set_vacancies(self):
        vacancies = [[], []]
        for index, cell in np.ndenumerate(self.state):
            if cell == 0 and self.goal[index] == 1:
                vacancies[0].append(index)
                vacancies[1].append(0)
        self.vacancies = np.array(vacancies, dtype=object).T

    def _sort_vacancies(self, order):
        for vacancy in self.vacancies:
            vacancy[1] = self._source_distance(vacancy[0])
        if order == 'ascending':
            self.vacancies = self.vacancies[(self.vacancies[:, 1]).argsort()]
        elif order == 'descending':
            self.vacancies = self.vacancies[(-self.vacancies[:, 1]).argsort()]
        print(f'Vacancies:\n{self.vacancies}')

    def _source_distance(self, index):
        distance = 0
        for source in self.sources:
            distance += np.sum(np.abs(source - index))
        return distance

    def _map_targets(self):
        targets = []
        for vacancy in self.vacancies:
            max_distance = vacancy[1]
            for source in self.sources:
                distance = np.sum(np.abs(source - vacancy[0]))
                if distance <= max_distance and not source.tolist() in targets:
                    vacancy[1] = source
                    max_distance = distance
            targets.append(vacancy[1].tolist())
        print(f'Vacancies:\n{self.vacancies}')
                    
    def _get_percept(self, index):
        neighbors = []
        for row_shift in range(-1, 2):
            for col_shift in range(-1, 2):
                row, col = index[0] + col_shift, index[1] + row_shift
                if self._in_grid(row, col) and self.state[row, col] == 1:
                    neighbors.append([row, col])
        return np.array(neighbors) if len(neighbors) > 0 else None

    def _get_options(self, index, taken):
        options = [[], []]
        for shift in zip([0, -1, 0, 1], [-1, 0, 1, 0]):
            row, col = index[0] + shift[0], index[1] + shift[1]
            if self._in_grid(row, col) and self.state[row, col] == 1 and [row, col] not in taken:
                options[0].append([row, col])
                options[1].append(np.sum(np.abs()))  # FIXME
        return np.array(options) if len(options) > 0 else None

    def _in_grid(self, row, col):
        return self._in_rows(row) and self._in_columns(col)

    def _in_rows(self, row):
        return 0 <= row and row < self.state.shape[0]

    def _in_columns(self, col):
        return 0 <= col and col < self.state.shape[1]

    def _get_best_option(self, index, options, target):
        best_option = options[0]
        best_distance = np.sum(np.abs(target - best_option))
        for option in options:
            distance = np.sum(np.abs(target - option))
            if distance < best_distance:
                best_option = option
                best_distance = distance
        return best_option if best_distance < np.sum(np.abs(target - index)) else None

    def _at_target(self, index, target):
        return np.all(index == target)

    def _draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = self.window_height - row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2 ,y2))
        graphics.draw_indexed(4, gl.GL_TRIANGLES, indicies, data)

    def update(self):
        temp = self.state.copy()
        taken = []
        for vacancy in np.flip(self.vacancies, axis=0):
            options = self._get_options(vacancy[0], taken)
            if options is not None and not self._at_target(vacancy[0], vacancy[1]):
                best_option = self._get_best_option(vacancy[0], options, vacancy[1])
                if best_option is not None:
                    temp[vacancy[0][0], vacancy[0][1]] = 1
                    temp[best_option[0], best_option[1]] = 0
                    vacancy[0] = best_option
                    taken.append([best_option[0], best_option[1]])
        self.state = temp

    def draw(self):
        for index, cell in np.ndenumerate(self.state):
            self._draw_cell(*index) if cell == 1 else None

