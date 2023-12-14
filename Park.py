import random


class Park:
    def __init__(self, name, park_id, lod):
        self.name = name
        self.park_id = park_id
        self.ride_list = []
        self.map = []
        self.curr_time = 0
        self.end_of_day = self.curr_time + lod
        print(f"The park closes at: [{self.end_of_day}] today!")
        self.start_x = -1
        self.start_y = -1
        self.width = 0
        self.height = 0

    def add_map(self, map_array):
        self.map = map_array
        self.height = len(self.map)
        self.width = len(self.map[1])
        # print(f"WIDTH: {self.width}, HEIGHT: {self.height}")
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] == 'E':
                    self.start_x = col
                    self.start_y = row

    def add_ride(self, ride_val):
        name, weight, reward = ride_val.split(':')
        self.ride_list.append(Ride(name, weight, reward))

    def display_info(self):
        print(f"Park Name:\t{self.name}")
        print(f"Park ID:\t{self.park_id}")
        self.display_times()
        # for row in self.map:
        #     print(row)

    def display_times(self):
        print(f"Ride List:\nTime: {self.curr_time}\n")
        for ride in self.ride_list:
            print(f"{ride.wait_time} : {ride.name}")

    def increment_waits(self):
        # self.curr_time += 5
        for ride in self.ride_list:
            ride.increment_wait()


class Ride:
    def __init__(self, name, weight, reward):
        self.name = name
        self.weight = int(weight)
        self.wait_time = 0
        self.reward = int(reward)
        self.randomize_wait()

    def randomize_wait(self):
        if self.weight == 0:
            random_number = random.randint(0, 30)
            random_five = random_number + (5 - random_number % 5)
            self.wait_time = random_five
        if self.weight == 1:
            random_number = random.randint(25, 60)
            random_five = random_number + (5 - random_number % 5)
            self.wait_time = random_five
        if self.weight == 2:
            random_number = random.randint(50, 100)
            random_five = random_number + (5 - random_number % 5)
            self.wait_time = random_five

    def increment_wait(self):
        adjustment = random.choice([-10, -5, 0, 5, 10]) * (self.weight + 1)
        adjusted_wait_time = self.wait_time + adjustment
        self.wait_time = min(max(5, adjusted_wait_time), 120)
