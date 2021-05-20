import pyglet
from game_of_life import GameOfLife
from self_organizing_ca import SelfOrganizingCA


class Window(pyglet.window.Window):

    def __init__(self, width, height, CellularAutomata, *args, **kwargs):
        super().__init__(width, height, *args, **kwargs)
        self.rule = CellularAutomata
        self.ca = self.rule(width, height, 50, 0.5)

    def update(self, dt):
        self.ca.run_rules()

    def on_draw(self):
        self.clear()
        self.ca.draw()

    def on_key_press(self, symbol, modifier):
        if symbol == pyglet.window.key.SPACE:
            pyglet.clock.schedule_interval(self.update, 1.0 / 6.0)
        elif symbol == pyglet.window.key.R:
            self.ca = self.rule(0, 0, 50, 0.5)
            pyglet.clock.unschedule(self.update)


if __name__ == '__main__':
    window = Window(600, 600, SelfOrganizingCA)
    pyglet.app.run()
