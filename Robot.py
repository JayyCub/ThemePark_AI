import time
from enum import Enum


class Directions(Enum):
    Stay = 0
    Up = 1
    Right = 2
    Down = 3
    Left = 4


class Robot:
    def __init__(self, gui, park, val_gui):
        self.gui = gui
        self.park = park
        self.rode = 0
        self.ridden = 0
        self.curr_x = self.park.start_x
        self.curr_y = self.park.start_y
        # print(f"Starting at: {self.curr_x}, {self.curr_y}")
        self.gui.change_cell_color(self.curr_y, self.curr_x, "blue")
        # for i in range(0, 5):
        #     time.sleep(2)
        #     self.move(1)
        #     # self.gui.update_gui()
        self.v_s = []
        self.previous_ride = -1
        self.vals_gui = val_gui
        self.rides = []

        self.run()

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
        discount_factor = 0.95
        epsilon = 0.01

        self.v_s = [[0 for _ in range(self.park.width)] for _ in range(self.park.height)]

        while True:
            max_change = 0.0
            for x in range(self.park.width):
                for y in range(self.park.height):
                    # print(f"X: {x}, Y: {y}, val: {self.park.map[y][x]}")
                    if self.park.map[y][x] == '_':
                        continue

                    old_v = self.v_s[y][x]
                    reward = self.calculate_reward(x, y)
                    max_val = self.get_max_next_state_value(x, y)
                    # print(f"Reward: {type(reward)}, {reward}\n"
                    #       f"discount: {type(discount_factor)}, {discount_factor}\n"
                    #       f"max: {type(max)}, {max}\n")
                    new_val = reward + discount_factor * max_val
                    self.v_s[y][x] = new_val

                    change = abs(new_val - old_v)
                    if change > max_change:
                        max_change = change
            if max_change < epsilon:
                # print("CONVERGED")
                break

    def calculate_reward(self, x, y):
        # print(f"X: {x}, Y: {y}, val: {self.park.map[y][x]}")
        if self.park.map[y][x] == 'O' or self.park.map[y][x] == 'E':
            return 0.0
        elif self.park.map[y][x].isdigit():
            ride_num = int(self.park.map[y][x])
            if ride_num == self.previous_ride:
                return -1
            ride_reward = self.park.ride_list[ride_num].reward
            ride_wait = self.park.ride_list[ride_num].wait_time
            times_rode = self.park.ride_list[ride_num].times_rode

            return (ride_reward / ride_wait) * pow(3, -1 * times_rode)
            # return 10.0

    def get_max_next_state_value(self, x, y):
        max_next_value = float('-inf')

        for direction in Directions:
            new_x, new_y = self.get_new_position(x, y, direction)

            if self.square_valid(new_x, new_y) and self.park.map[new_y][new_x] != '_':
                next_value = self.v_s[new_y][new_x]
                if next_value > max_next_value:
                    max_next_value = next_value
        # print(round(maxNextValue, 3), end=" : ", flush=True)
        return max_next_value

    def get_new_position(self, x, y, direction):
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

    def square_valid(self, x, y):
        valid = True
        if y < 0 or y >= self.park.height or x < 0 or x >= self.park.width:
            valid = False
        return valid

    def automatic_action(self):
        max_expected_util = float('-inf')
        best_action = Directions.Stay
        for direction in Directions:
            expected_util = self.calc_expected_util(direction)

            if expected_util > max_expected_util:
                max_expected_util = expected_util
                best_action = direction

        return best_action

    def calc_expected_util(self, direction):
        expected_utility = 0.0

        for x in range(self.park.width):
            for y in range(self.park.height):
                if self.park.map[y][x] == '_':
                    continue

                new_x, new_y = self.get_new_position(x, y, direction)
                if self.square_valid(new_x, new_y) and x == self.curr_x and y == self.curr_y\
                        and self.park.map[new_y][new_x] != '_':
                    expected_utility += self.v_s[new_y][new_x]

        return expected_utility

    def run(self):
        while self.park.curr_time < self.park.end_of_day:
            input("Press enter to find the next ride:")
            self.value_iteration()
            self.vals_gui.val_gui_update(self.v_s)
            input("Press enter to go to the ride:")
            # for row in self.Vs:
            #     print(row)

            while True:
                if self.park.curr_time >= self.park.end_of_day:
                    break

                action = self.automatic_action()
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
                    print("Stay", end=" ", flush=True)

                time.sleep(0.1)
                self.move(action)
                self.gui.update_gui()

                if self.park.map[self.curr_y][self.curr_x].isdigit():
                    ride_num = int(self.park.map[self.curr_y][self.curr_x])
                    print(f"\n[{self.park.curr_time}]: Now boarding The ",
                          self.park.ride_list[ride_num].name,
                          "!")
                    self.rides.append(self.park.ride_list[ride_num])
                    self.park.curr_time += self.park.ride_list[ride_num].wait_time
                    self.previous_ride = ride_num
                    print(f"[{self.park.curr_time}]: ")
                    # self.park.ride_list[ride_num].reward /= 10
                    self.park.ride_list[ride_num].times_rode += 1
                    self.park.increment_waits()

                    break

        print(f"\n[{self.park.curr_time}]: The park is now closed, please exit.")
        print(f"Thanks for visiting {self.park.name}!")
        print("Your day report:")
        for ride in self.rides:
            print(ride.name)
        input("\nPress enter to end program:")
        exit(0)
