import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS
from pyglet.window.key import N


class TargetsCA:
    def __init__(self, initial, goal, cell_size, window_width, window_height):
        self.initial = initial
        self.goal = goal
        self.cell_size = cell_size
        self.window_width = window_width
        self.window_height = window_height
        self.state = initial.copy()
        self.sources = self._sources(initial)
        self.statics = self._statics(initial, goal)
        self.vacancies = self._vacancies(initial, goal)
        self.mappings = self._map_targets(initial, goal, self.sources, self.vacancies)
        self.paths = self._paths(self.mappings)

        # FIXME
        temp = {}
        for key, value in self.mappings.items():
            temp[(value[0], value[1])] = key
        self.mappings = temp
        temp = {}
        for key, value in self.paths.items():
            new_path = value[:-1].tolist()
            new_path.reverse()
            temp[(value[-1][0], value[-1][1])] = new_path + [list(key)]
        self.paths = temp

        print(f'Mappings:\n{self.mappings}')
        print(f'Paths:\n{self.paths}')

        # FIXME: TEMP
        self.update_ = True

    def _sources(self, state):
        sources = []
        for index, cell in np.ndenumerate(state):
            if cell == 1:
                sources.append(index)
        return np.array(sources)

    def _statics(self, state, goal):
        statics = []
        for index, cell in np.ndenumerate(state):
            if cell == 1 and goal[index] == 1:
                statics.append(index)
        return np.array(statics)

    def _source_distance(self, sources, index):
        distance = 0
        for _, source in sources:
            distance += np.sum(np.abs(source - index))
        return distance

    def _vacancies(self, state, goal):
        vacancies = [[], []]
        for index, cell in np.ndenumerate(state):
            if cell == 0 and goal[index] == 1:
                vacancies[0].append(index)
                vacancies[1].append(self._source_distance(self.sources, index))
        vacancies = np.array(vacancies, dtype=object).T
        return vacancies[(-vacancies[:, 1]).argsort()]

    def _nearest_source(self, sources, index):
        nearest = sources[0]
        for source in sources:
            if np.sum(np.abs(source - index)) < np.sum(np.abs(nearest - index)):
                nearest = source
        return nearest

    def _remove_source(self, sources, index):
        remaining = []
        for source in sources:
            if source[0] != index[0] or source[1] != index[1]:
                remaining.append(source)
        return np.array(remaining)

    def _map_targets(self, initial, goal, sources, vacancies):
        mappings = {}
        intersections = []
        for vacancy in vacancies:
            print(f'Sources: {len(sources)}')
            nearest = self._nearest_source(sources, vacancy[0])
            mappings[vacancy[0]] = nearest
            sources = self._remove_source(sources, nearest)
            if initial[nearest[0], nearest[1]] == 1 and goal[nearest[0], nearest[1]] == 1:
                intersections.append(nearest)
        for intersection in intersections:
            print(f'sources: {len(sources)}')
            nearest = self._nearest_source(sources, intersection)
            mappings[(intersection[0], intersection[1])] = nearest
            sources = self._remove_source(sources, nearest)
            if initial[nearest[0], nearest[1]] == 1 and goal[nearest[0], nearest[1]] == 1:
                intersections.append(nearest)
        print(mappings)
        return mappings

    def _options(self, index):
        options = []
        for shift in zip([0, -1, 0, 1], [-1, 0, 1, 0]):
            options.append([index[0] + shift[0], index[1] + shift[1]])
        return np.array(options)

    def _best_option(self, options, target):
        best = options[0]
        for option in options:
            if np.sum(np.abs(target - option)) < np.sum(np.abs(target - best)):
                best = option
        return best

    def _greedy_path(self, index, target):
        path = [self._best_option(self._options(index), target)]
        while not np.array_equal(path[-1], target):
            path.append(self._best_option(self._options(path[-1]), target))
        return np.array(path)

    def _paths(self, mappings):
        paths = {}
        for index, target in mappings.items():
            paths[index] = self._greedy_path(index, target)
        return paths

    def _draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = self.window_height - row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 - self.cell_size
        indicies = [0, 1, 2, 1, 2, 3]
        data = ('v2i', (x1, y1, x1, y2, x2, y1, x2, y2))
        graphics.draw_indexed(4, gl.GL_TRIANGLES, indicies, data)

    def update(self):
        temp = self.state.copy()
        temp_paths = {}
        for cell, path in self.paths.items():
            if len(path) > 0 and self.state[path[0][0], path[0][1]] == 0:
                self.state[path[0][0], path[0][1]] = 1
                temp[path[0][0], path[0][1]] = 1
                temp[cell[0], cell[1]] = 0
                temp_paths[(path[0][0], path[0][1])] = self.paths[cell][1:]
            else:
                temp_paths[cell] = path
        self.paths = temp_paths
        self.state = temp.copy()

    def draw(self):
        for index, cell in np.ndenumerate(self.state):
            self._draw_cell(*index) if cell == 1 else None
