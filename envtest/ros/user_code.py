#!/usr/bin/python3


import numpy as np
import cv2
from pickle import NONE
from utils import AgileCommandMode, AgileCommand
from rl_example import rl_example, rl_example_vision


def compute_command_vision_based(state, img, rl_policy=None):
    ################################################
    # !!! Begin of user code !!!
    # TODO: populate the command message
    ################################################
    # print("Computing command vision-based!")
    # print(state)
    # print("Image shape: ", img.shape)

    # Example of SRT command
    command_mode = 0
    command = AgileCommand(command_mode)
    command.t = state.t
    command.rotor_thrusts = [1.0, 1.0, 1.0, 1.0]

    # Example of CTBR command
    command_mode = 1
    command = AgileCommand(command_mode)
    command.t = state.t
    command.collective_thrust = 15.0
    command.bodyrates = [0.0, 0.0, 0.0]

    # Example of LINVEL command (velocity is expressed in world frame)
    command_mode = 2
    command = AgileCommand(command_mode)
    command.t = state.t
    command.velocity = [1.0, 0.0, 0.0]
    command.yawrate = 0.0

    # resized_img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_NEAREST)[::-1, ::-1].T
    # print("{}, {}, {}".format(np.min(resized_img), np.max(resized_img), img.shape))
    # phi = 45*7/8
    # phi_np = np.linspace(-phi*np.pi/180, phi*np.pi/180, 8)
    # phi_np = np.cos(phi_np)
    # phi_np = np.tile(phi_np,(8,1))
    # theta_np = np.copy(phi_np).T 

    # obstacles = np.minimum((resized_img/phi_np/theta_np)*10.0, 1.0)
    # # print(obstacles)
    # obstacles = obstacles.flatten()

    if rl_policy is not None:
        command = rl_example_vision(state, img, rl_policy)

    ################################################
    # !!! End of user code !!!
    ################################################
    # print(command)
    
    return command


def compute_command_state_based(state, obstacles, rl_policy=None):
    ################################################
    # !!! Begin of user code !!!
    # TODO: populate the command message
    ################################################
    # print("Computing command based on obstacle information!")
    # print(state)
    # print("Obstacles: ", obstacles)

    # Example of SRT command
    command_mode = 0
    command = AgileCommand(command_mode)
    command.t = state.t
    command.rotor_thrusts = [1.0, 1.0, 1.0, 1.0]
 
    # Example of CTBR command
    command_mode = 1
    command = AgileCommand(command_mode)
    command.t = state.t
    command.collective_thrust = 10.0
    command.bodyrates = [0.0, 0.0, 0.0]

    # Example of LINVEL command (velocity is expressed in world frame)
    command_mode = 2
    command = AgileCommand(command_mode)
    command.t = state.t
    command.velocity = [0, 0.0, -5.0]
    command.yawrate = 0.0

    # If you want to test your RL policy
    if rl_policy is not None:
        command = rl_example(state, obstacles.boxel, rl_policy)

    ################################################
    # !!! End of user code !!!
    ################################################

    return command
