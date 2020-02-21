import requests
import math

def calc_fuel(mass):
    rem = mass%3
    return (mass - rem)/3 - 2
    
def recursive_calc_fuel_1(mass):
    _m = mass
    total = 0
    while _m > 0:
        _m = calc_fuel(_m)
        if _m > 0:
            total += _m
    return total
    
def recursive_calc_fuel(mass):
    add_fuel = calc_fuel(mass)
    if add_fuel <= 0:
        return 0
        
    return add_fuel + recursive_calc_fuel(add_fuel)

   
with open('./puzzle1input.txt', 'r') as f:
    total = 0
    for mass in f:
        total += recursive_calc_fuel(int(mass))
    print(total)

