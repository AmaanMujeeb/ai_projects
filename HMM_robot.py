#This is a code that I wrote to understand the concept of Hidden Markov Model
#There is a robot in a 1-D room with 5 tiles and in the both ends there are walls
#We can't see the robot but can see the observation robot makes like "wall-left","no-wall-ahead"
#At each time the robot move to the right with the probability 0.8 and stays there with a
#probability 0.2 and the observations are correct with the probability 0.9
#As time steps passes we can predict the probable location of the robot
#This robot is just an application of forward algorithm

import numpy as np

N = 5
belief = np.ones(N) / N

def normalize(belief):
    total = np.sum(belief)
    return belief/total if total!=0 else belief

def transition(belief):
    new_belief = np.zeros(N)
    for i in range(N):
        stay_prob = 0.2 * belief[i]
        move_prob = 0.8 * belief[i]
        new_belief[i] += stay_prob
        if i < N-1:
            new_belief[i+1] += move_prob
        else:
            new_belief[i] += move_prob
    return new_belief

def update_with_sensor(observation, prior_belief):
    updated_belief = np.zeros(N)
    for i in range(N):
        if i==0 and observation=="wall-left":
            prob = 0.9
        elif i!=0 and observation=="wall-left":
            prob = 0.1
        elif i==N-1 and observation=="wall-ahead":
            prob = 0.9
        elif i!=N-1 and observation=="no-wall-ahead":
            prob = 0.9
        elif i==0 and observation=="no-wall-left":
            prob = 0.1
        else:
            prob = 0.9
        updated_belief[i] = prob * prior_belief[i]
    return normalize(updated_belief)

observations = [
                "wall-left",
                "no-wall-ahead",
                "wall-ahead",
                "wall-left",
                "no-wall-left"
                ]

for t, obs in enumerate(observations, 1):
    belief = transition(belief)
    belief = update_with_sensor(obs, belief)
    print(f"Belief after observation {t}: {np.round(belief, 4)}")

