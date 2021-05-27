import numpy as np
from pyglet import gl, graphics
from pyglet.libs.win32.constants import DT_PATH_ELLIPSIS


class AStarCA:

    def __init__(self, cell_size=10):
        self.cell_size = cell_size

    @staticmethod
    def _set_statics(initial, goal):
        for index, cell in np.ndenumerate(initial):
            initial[index] = 2 if cell == goal[index] == 1 else cell

    @staticmethod
    def _configure_goal(goal):
        for index, cell in np.ndenumerate(goal):
            goal[index] = 2 if cell == 1 else 0

    @staticmethod
    def _get_agents(initial):
        agents = np.array([], dtype='int8')
        for index, cell in np.ndenumerate(initial):
            agents = np.append(agents, index) if cell == 1 else agents
        return agents.reshape(int(agents.shape[0] / 2), 2)

    # @staticmethod
    # def _run_a_star(self, initial, goal, agents):
    #     while initial != goal:

    def fit(self, initial, goal):
        self._set_statics(initial, goal)
        self._configure_goal(goal)
        agents = self._get_agents(initial)
        print('Initial:\n', initial)
        print('Goal:\n', goal)
        print('Agents:\n', agents)
    
    def run(self):
        pass


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
                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
a_star_ca = AStarCA(10)
a_star_ca.fit(initial, goal)
