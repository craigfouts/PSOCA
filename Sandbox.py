import pyglet
from game_of_life import GameOfLife
from self_organizing_ca import SelfOrganizingCA


class Window(pyglet.window.Window):

    def __init__(self, width, height, CellularAutomata, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.ca = CellularAutomata(width, height, 50, 0.5)
        pyglet.clock.schedule_interval(self.update, 1.0 / 24.0)

    def update(self, dt):
        self.ca.run_rules()

    def on_draw(self):
        self.clear()
        self.ca.draw()


if __name__ == '__main__':
    window = Window(600, 600, SelfOrganizingCA)
    pyglet.app.run()
