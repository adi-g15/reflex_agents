from time import sleep
import numpy as np
import random
import math

# We create the environment
environ = np.random.choice([True,False],p=[0.1,0.9],size=(15,15))

class ModelBasedTaxi:
    def __init__(self, environ, start_loc):
        self.environ = environ
        self.start_loc = start_loc
        self.position = self.start_loc
        self.model = ModelBasedReflexAgent(self)

    def move_next(self):
        # MODEL+RULES
        action = self.model.act( self.environ )

        # ACTUATOR
        self._move(direction=action)

    def _move(self, direction):
        if direction[0] == 0 and direction[1] == 0:
            print("Model Taxi Not Move")
            return

        print("Model Taxi moving", end=" ")
        if direction[0] == -1:
            print("Left", end=" ")
        elif direction[0] == 1:
            print("Right", end=" ")
        if direction[1] == -1:
            print("Up", end=" ")
        elif direction[1] == 1:
            print("Down", end=" ")
        print()

        self.environ[ self.position[0] ][ self.position[1] ] = False

        new_x = self.position[0] + direction[0]
        new_y = self.position[1] + direction[1]

        self.environ[ new_x ][ new_y ] = True
        self.position = [ new_x, new_y ]

class GoalBasedTaxi:
    def __init__(self, environ, start_loc, end_loc):
        self.environ = environ

        self.start_loc = start_loc
        self.end_loc = end_loc
        
        self.position = self.start_loc

        self.agent = GoalBasedReflexAgent(self)
        
    def move_next(self):
        # MODEL+RULES
        action = self.agent.act( self.environ )
        
        # ACTUATOR
        self._move(direction=action)

    def _move(self, direction):
        if direction[0] == 0 and direction[1] == 0:
            print("Goal Taxi Not Moving")
            return

        print("Goal Taxi moving", end=" ")
        if direction[0] == -1:
            print("Left", end=" ")
        elif direction[0] == 1:
            print("Right", end=" ")
        if direction[1] == -1:
            print("Up", end=" ")
        elif direction[1] == 1:
            print("Down", end=" ")
        print()

        self.environ[ self.position[0] ][ self.position[1] ] = False

        new_x = self.position[0] + direction[0]
        new_y = self.position[1] + direction[1]

        self.environ[ new_x ][ new_y ] = True
        self.position = [ new_x, new_y ]

# Model-based reflex agent
class ModelBasedReflexAgent:
    def __init__(self,parent_taxi):
        self.taxi = parent_taxi
        # STATE
        self.state = {
            "obstacles": []
        }

    def _state_update(self):
        curr_pos = self.taxi.position
        environ = self.taxi.environ
        obstacles = []

        dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for dir in dirs:
            x = curr_pos[0] + dir[0]
            y = curr_pos[1] + dir[1]
            if environ[x][y]:
                obstacles.append([x,y])

        self.state["obstacles"] = obstacles

    def act(self,percept):
        # UPDATE STATE
        self._state_update()

        pos = self.taxi.position

        movable_directions = []
        
        dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        
        for dir in dirs:
            x = pos[0] + dir[0]
            y = pos[1] + dir[1]

            # TODO
            if x < 0 or x >= len(self.taxi.environ) or y < 0 or y >= len(self.taxi.environ):
                continue

            if [x,y] not in self.state["obstacles"]:
                movable_directions.append(dir)

        return random.choice(movable_directions)

# Goal-based reflex agent
class GoalBasedReflexAgent:
    def __init__(self,parent_taxi):
        self.taxi = parent_taxi
        self.state = {
            "goal": self.taxi.end_loc,
            "obstacles": []
        }

    def _state_update(self):
        curr_pos = self.taxi.position
        environ = self.taxi.environ
        obstacles = []

        dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for dir in dirs:
            x = curr_pos[0] + dir[0]
            y = curr_pos[1] + dir[1]
            if environ[x][y]:
                obstacles.append([x,y])

        self.state["obstacles"] = obstacles

    def act(self,percept):
        # UPDATE STATE
        self._state_update()

        movable_directions = []

        dirs = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        pos = self.taxi.position

        if pos == self.state["goal"]:
            print("Goal based Reached Destination...")
            return [0,0]

        for dir in dirs:
            x = pos[0] + dir[0]
            y = pos[1] + dir[1]
            if [x,y] not in self.state["obstacles"]:
                movable_directions.append(dir)

        better_direction = [0,0]
        goal = self.state["goal"]
        for dir in movable_directions:
            x = pos[0] + dir[0]
            y = pos[1] + dir[1]
            nearer_x = pos[0] + better_direction[0]
            nearer_y = pos[1] + better_direction[1]
            
            nearest_dist = math.hypot( goal[1] - nearer_y, goal[0] - nearer_x )
            new_dist = math.hypot( goal[1] - y, goal[0] - x )

            if new_dist <= nearest_dist:
                better_direction = dir

        return better_direction

# A model-based reflex agent
model_taxi = ModelBasedTaxi(
        environ=environ,
        start_loc=[5,4],
    )

# A goal-based reflex agent
goal_taxi = GoalBasedTaxi(
        environ=environ,
        start_loc=[2,9],
        end_loc=[12,1]
    )

# Run whatever cars/taxis were added

while True:
    print(model_taxi.position, goal_taxi.position)
    for i in range(15):
        for j in range(15):
            if environ[i][j]:
                if [i,j] == model_taxi.position or [i,j] == goal_taxi.position:
                    print("+", end = " ")
                else:
                    print("*", end = " ")
            else:
                print(" ", end = " ")
        print()

    model_taxi.move_next()
    goal_taxi.move_next()
    sleep(1)
