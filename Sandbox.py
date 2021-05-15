import pyglet
from game_of_life import GameOfLife


class Window(pyglet.window.Window):

    def __init__(self, window_width, window_height, *args, **kwargs):
        super().__init__(window_width, window_height, *args, **kwargs)
        self.game_of_life = GameOfLife(window_width, window_height, 10, 0.5)
        pyglet.clock.schedule_interval(self.update, 1.0 / 8.0)

    def update(self, dt):
        self.game_of_life.run_rules()

    def on_draw(self):
        self.clear()
        self.game_of_life.draw()


if __name__ == '__main__':
    window = Window(600, 600)
    pyglet.app.run()
