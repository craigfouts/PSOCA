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
