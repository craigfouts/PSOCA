import numpy as np
from pyglet import app, clock
from pyglet.window import key, Window
from vacancy_ca import VacancyCA


class MainWindow(Window):

    def __init__(self, model, initial, goal, cell_size=10):
        self.window_width = initial.shape[0] * cell_size
        self.window_height = initial.shape[1] * cell_size
        super().__init__(self.window_width, self.window_height)

        self.initial = initial
        self.goal = goal
        self.model = model
        self.cell_size = cell_size
        self.ca = model(initial, goal, cell_size,
                        self.window_width, self.window_height)
        self.key_map = {
            key.SPACE: lambda x: self._handle_space_key(x),
            key.R: lambda x: self._handle_r_key(x)
        }

    def _handle_space_key(self, dt):
        clock.schedule_interval(self.update, dt)

    def _handle_r_key(self, _):
        self.ca = self.model(self.initial, self.goal, self.cell_size)
        clock.unschedule(self.update)

    def update(self, _):
        self.ca.update()

    def on_draw(self):
        self.clear()
        self.ca.draw()

    def on_key_press(self, symbol, _):
        try:
            self.key_map[symbol](1.0 / 2.0)
        except:
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
                     [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                     [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    window = MainWindow(VacancyCA, initial, goal, 50)
    app.run()
