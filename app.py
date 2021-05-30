import numpy as np
# from vacancy_ca import VacancyCA
from vacancy_ca_temp import VacancyCA
from pyglet import app, clock
from pyglet.window import Window


class MainWindow(Window):

    def __init__(self, rule, initial, goal, cell_size=10):
        self.window_width = initial.shape[0] * cell_size
        self.window_height = initial.shape[1] * cell_size
        super().__init__(self.window_width, self.window_height)

        self.rule = rule
        self.initial = initial
        self.goal = goal
        self.cell_size = cell_size
        self.ca = self.rule(self.initial, self.goal, self.cell_size)
        self.key_map = {
            32: lambda d: self._handle_space_key(d),
            114: lambda d: self._handle_r_key(d)
        } 

    def _handle_space_key(self, dt):
        clock.schedule_interval(self.update, dt)

    def _handle_r_key(self, _):
        self.ca = self.rule(self.initial, self.goal, self.cell_size)
        clock.unschedule(self.update)

    def update(self, _):
        self.ca.update()

    def on_draw(self):
        self.clear()
        self.ca.draw()

    def on_key_press(self, symbol, modifiers):
        try:
            self.key_map[symbol](1.0 / 4.0)
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
                     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    window = MainWindow(VacancyCA, initial.copy(), goal.copy(), 50)
    app.run()
