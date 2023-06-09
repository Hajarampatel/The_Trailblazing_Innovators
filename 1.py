
import numpy as np

# Global variables 

reward = -0.04
terminate_states = ((1,3),(2,3))

reward_matrix = [[reward for _ in range(4)] for _ in range(3)]

reward_matrix[2][3] = 1
reward_matrix[1][3] = -1

wall = [(1,1)]

possible_actions = ['L','R','U','D']

prob_actions = {'L':0.25,'R':0.25,'U':0.25,'D':0.25}

# environment action corresponding to Agent

environment_left = {'L':'D','R':'U','U':'L','D':'R'}
environment_right = {'L':'U','R':'D','U':'R','D':'L'}

def is_possible(i,j):
    return (i,j) not in wall and i >= 0 and i < 3 and j >= 0 and j < 4

def print_values(V):
  for i in range(2,-1,-1):
    print("---------------------------")
    for j in range(4):
      v = V[i][j]
      if v >= 0:
        print(" %.2f|" % v, end="")
      else:
        print("%.2f|" % v, end="") # -ve sign takes up an extra space
    print("")

def func(action,i,j):
    if action == 'L':
        new_state = (i,j-1)
    elif action == 'R':
        new_state = (i,j+1)
    elif action == 'U':
        new_state = (i+1,j)
    else:
        new_state = (i-1,j)   

    return new_state

def find_value_function(i,j,gamma=1):
    value = 0
    for action in possible_actions:
        # 0.8 probability to go with given direction 
        state_x,state_y = func(action,i,j)
        if is_possible(state_x,state_y):
            value_to_action_given = (reward_matrix[state_x][state_y] + gamma*V_pie[state_x][state_y])
        else:
            value_to_action_given = (reward_matrix[i][j] + gamma*V_pie[i][j])
        
        # 0.1 probability to go with Left direction 
        state_x,state_y = func(environment_left[action],i,j)
        if is_possible(state_x,state_y):
            value_to_action_left = (reward_matrix[state_x][state_y] + gamma*V_pie[state_x][state_y])
        else:
            value_to_action_left = (reward_matrix[i][j] + gamma*V_pie[i][j])
        
        # 0.1 probability to go with Right direction 
        state_x,state_y = func(environment_right[action],i,j)
        if is_possible(state_x,state_y):
            value_to_action_right = (reward_matrix[state_x][state_y] + gamma*V_pie[state_x][state_y])
        else:
            value_to_action_right = (reward_matrix[i][j] + gamma*V_pie[i][j])
        
        value_to_action = value_to_action_given*0.8+value_to_action_left*0.1+value_to_action_right*0.1        

        value += value_to_action*prob_actions[action]

    return value

# Iterative Value function 
# Initialization of V_pie

cnt = 0

V_pie = [[0 for _ in range(4)]for _ in range(3)]

# V_pie[1][3] = -1
# V_pie[2][3] = 1


theta = 1e-6
iter = 0
while True:
    delta = 0
    for i in range(3):
        for j in range(4):
            state = (i,j)
            if state in terminate_states or state in wall:
                continue
            v = V_pie[i][j]
            V_pie[i][j] = find_value_function(i,j)
            delta = max(delta,abs(v-V_pie[i][j]))
    iter += 1
    if delta < theta:
        print(f"Iteration ends at :{iter}")
        break 

print_values(V_pie)