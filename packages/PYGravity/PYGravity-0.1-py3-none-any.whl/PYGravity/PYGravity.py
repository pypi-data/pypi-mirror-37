"""
Author : Harishankar.G
Date : 16 - 10 - 2018
Version : 0.1
"""
# import needed libraries
from math import sqrt


# Functions meant for calculations


def calcgravity():
    """
    Calculates magnitude of gravitational force if all parameters are given,
    else calculates the missing parameter, if magnitude of force is given.
    """
    G = 6.67408 * 10e-11

    try:
        distance = float((eval(input("Enter distance between two bodies(in meters) :-"))))
    except SyntaxError:
        distance = False
    try:
        mass1 = float(eval((input("Enter mass of the first body :-"))))
    except SyntaxError:
        mass1 = False
    try:
        mass2 = float(eval((input("Enter mass of the second body :-"))))
    except SyntaxError:
        mass2 = False
    if distance != False and mass1 != False and mass2 != False:
        force = float((G * mass1 * mass2) / (distance ** 2))
        return force
    elif distance == False:
        try:
            force = float(eval(input("Enter magnitude of gravitational force :-")))
        except SyntaxError:
            force = False
        if force == False:
            print("Information is not provided")
        else:
            result = float(sqrt((G * mass1 * mass2) / force))
            return result
    elif mass1 == False:
        try:
            force = float(eval(input("Enter magnitude of gravitational force :-")))
        except SyntaxError:
            force = False
        if force == False:
            print("Information is not provided")
        else:
            result = float((G * mass1) / (distance ** 2) * (1 / force))
            return result
    elif mass2 == False:
        try:
            force = float(eval(input("Enter magnitude of gravitational force :-")))
        except SyntaxError:
            force = False
        if force == False:
            print("Information is not provided")
        else:
            result = float((G * mass2) / (distance ** 2) * (1 / force))
            return result
