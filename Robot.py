import time
from enum import Enum


class Directions(Enum):
    Stay = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4


class Robot:
    def __init__(self, gui, park):
        self.gui = gui
        self.park = park
        self.rode = 0
        self.curr_x = self.park.start_x
        self.curr_y = self.park.start_y
        print(f"Starting at: {self.curr_x}, {self.curr_y}")
        self.gui.change_cell_color(self.curr_y, self.curr_x, "blue")
        # for i in range(0, 5):
        #     time.sleep(2)
        #     self.move(1)
        #     # self.gui.update_gui()
        self.Vs = []

        self.Run()

    def move(self, direction):
        # print(f"At [{self.curr_x}, {self.curr_y}]... {Directions(direction).name}")
        old_x = self.curr_x
        old_y = self.curr_y
        match direction.value:
            case 1:
                self.curr_y -= 1
            case 2:
                self.curr_x += 1
            case 3:
                self.curr_y += 1
            case 4:
                self.curr_x -= 1

        self.gui.change_cell_color(self.curr_y, self.curr_x, "blue")
        self.gui.reset_cell(old_y, old_x)

    def value_iteration(self):
        discount_factor = 0.85
        epsilon = 0.01

        self.Vs = [[0 for _ in range(self.park.width)] for _ in range(self.park.height)]

        while True:
            maxChange = 0.0
            for x in range(self.park.width):
                for y in range(self.park.height):
                    # print(f"X: {x}, Y: {y}, val: {self.park.map[y][x]}")
                    if self.park.map[y][x] == '_':
                        continue

                    oldV = self.Vs[y][x]
                    reward = self.calculateReward(x, y)
                    max = self.getMaxNextStateValue(x, y)
                    # print(f"Reward: {type(reward)}, {reward}\n"
                    #       f"discount: {type(discount_factor)}, {discount_factor}\n"
                    #       f"max: {type(max)}, {max}\n")
                    newValue = reward + discount_factor * max
                    self.Vs[y][x] = newValue

                    change = abs(newValue - oldV)
                    if change > maxChange:
                        maxChange = change
            if maxChange < epsilon:
                print("CONVERGED")
                break

    def calculateReward(self, x, y):
        # print(f"X: {x}, Y: {y}, val: {self.park.map[y][x]}")
        if self.park.map[y][x] == 'O' or self.park.map[y][x] == 'E':
            return 0.0
        elif self.park.map[y][x].isdigit():
            return self.park.ride_list[int(self.park.map[y][x])].reward
            # return 10.0

    def getMaxNextStateValue(self, x, y):
        maxNextValue = float('-inf')

        for direction in Directions:
            newX, newY = self.getNewPosition(x, y, direction)

            if self.squareValid(newX, newY) and self.park.map[newY][newX] != '_':
                nextValue = self.Vs[newY][newX]
                if nextValue > maxNextValue:
                    maxNextValue = nextValue
        # print(round(maxNextValue, 3), end=" : ", flush=True)
        return maxNextValue

    def getNewPosition(self, x, y, direction):
        match direction.value:
            case 1:
                y -= 1
            case 2:
                x += 1
            case 3:
                y += 1
            case 4:
                x -= 1
        return x, y

    def squareValid(self, x, y):
        valid = True
        if y < 0 or y >= self.park.height or x < 0 or x >= self.park.width:
            valid = False
        return valid

    def automaticAction(self):
        maxExpectedUtil = float('-inf')
        bestAction = Directions.Stay
        for direction in Directions:
            expectedUtil = self.calcExpectedUtil(direction)

            if expectedUtil > maxExpectedUtil:
                maxExpectedUtil = expectedUtil
                bestAction = direction

        return bestAction

    def calcExpectedUtil(self, direction):
        expectedUtility = 0.0

        for x in range(self.park.width):
            for y in range(self.park.height):
                if self.park.map[y][x] == '_':
                    continue

                newX, newY = self.getNewPosition(x, y, direction)
                if self.squareValid(newX, newY) and x == self.curr_x and y == self.curr_y:
                    expectedUtility += self.Vs[newY][newX]

        return expectedUtility

    def Run(self):
        print("Starting...")
        self.value_iteration()
        print("Done with iteration.")

        # for row in self.Vs:
        #     print(row)

        while True:
            if self.park.curr_time >= self.park.end_of_day:
                print("The park is now closed, please exit.")
                break

            action = self.automaticAction()
            if action == Directions.Up:
                print("↑", end=" ", flush=True)
                self.park.curr_time += 1
            elif action == Directions.Down:
                print("↓", end=" ", flush=True)
                self.park.curr_time += 1
            elif action == Directions.Right:
                print("→", end=" ", flush=True)
                self.park.curr_time += 1
            elif action == Directions.Left:
                print("←", end=" ", flush=True)
                self.park.curr_time += 1
            elif action == Directions.Stay:
                print("x", end=" ", flush=True)

            time.sleep(0.1)
            self.move(action)
            self.gui.update_gui()

            if self.park.map[self.curr_y][self.curr_x].isdigit():
                print("Now boarding The ",
                      self.park.ride_list[int(self.park.map[self.curr_y][self.curr_x])].name,
                      "!")
                print("The time is ", self.park.curr_time)
                break
