# Theme Park Navigation with Interactive MDP

***Important Note***: This was developed in and only works for **Python 3.11**

_Created by Jacob Thomsen, for BYU CS 470 - Intro to Artificial Intelligence, Final Project_


## Overview
Welcome to the Theme Park Navigation project! This program utilizes a Markov Decision Process (MDP) algorithm to optimize the navigation of a robot through a theme park. The goal is to efficiently choose and visit rides based on various factors, such as wait time, reward, and travel distance.

## Main Highlights/Features

1. **MDP Algorithm:** The core of the project is a Markov Decision Process algorithm that intelligently guides the robot through the theme park to optimize its ride selections.

2. **Interactive GUI:** The program features a graphical user interface (GUI) that visually represents the theme park map, the robot's position, and a heatmap of values after each iteration of the MDP algorithm.

3. **Ride Customization:** Users can customize ride attributes by modifying the input files (`ShapelandRides.txt`). Set reward values and weight for each ride, influencing the robot's decision-making process.

4. **Dynamic Environment:** The program simulates dynamic changes in ride wait times after each ride, adding realism to the optimization process.

5. **Multiple Goals:** The robot is capable of navigating to multiple ride goals in a single simulation, preventing it from repeatedly visiting the same ride.

6. **Discount Factor Adjustment:** Users can interactively change the discount factor (gamma) for each run of the algorithm, influencing the robot's decision strategy.

## How to Run

```python3 main.py ShapelandMap.txt ShapelandRides.txt```

Replace ShapelandMap.txt and ShapelandRides.txt with your own theme park map and ride data files.

## Interact with the GUI:

After running the program, a GUI window will open, displaying the theme park map, the robot's movements, and the heatmap of values after each MDP iteration.
Customize Ride Attributes:

Modify the ShapelandRides.txt file to adjust ride rewards and weights. Higher rewards attract the robot, while weights influence wait time randomness.

## Change Discount Factor:

You can enable the interactive discount value feature from within the code (robot.py, line 55). This will add prompts to change the discount value between MDP value iterations after each ride.

Note:

The program uses Tkinter for GUI components, so ensure that you have the Tkinter library installed in your Python environment.
