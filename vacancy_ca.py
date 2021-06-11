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
        self.vacancies = np.array([])
        self._initialize()

    def _initialize(self):
        self._set_sources()
        self._set_vacancies()
        self._sort_vacancies()
        self._map_targets()

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

    def _sort_vacancies(self):
        for vacancy in self.vacancies:
            vacancy[1] = self._source_distance(vacancy[0])
        self.vacancies = self.vacancies[(-self.vacancies[:, 1]).argsort()]
        print(f'Vacancies:\n{self.vacancies}')

    def _source_distance(self, index):
        distance = 0
        for source in self.sources:
            distance += np.sum(np.abs(source - index))
        return distance

    def _map_targets(self):
        for vacancy_index, vacancy in enumerate(self.vacancies):
            closest = self.sources[-1]
            for source in self.sources:
                print('Source:', source)
                print('Closest:', closest)
                distance = np.sum(np.abs(source - vacancy[0]))
                if distance < self.vacancies[vacancy_index][1]:
                    closest = source
            self.vacancies[vacancy_index][1] = closest
            self.sources = self.sources[self.sources != closest]
            print('Sources:', self.sources)
        print(f'Vacancies:\n{self.vacancies}')

    def update(self):
        pass

    def draw(self):
        pass

