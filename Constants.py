# Trams
C = 420
number_of_trams = 13
safety_time = 40
offpeak_f = 15
traverse_switch_time = 0

# Stops
stop_names = [
    # P+R -> CS
    "P+R", "WKZ", "UMC", "HeL", "PaL", "KrR", "GaW", "VaR", "CS",
    # CS -> P+R
    "CS->", "VaR->", "GaW->", "KrR->", "PaL->", "HeL->", "UMC->", "WKZ->", "P+R->",
]
number_of_stops = len(stop_names)
door_block_time = 60

# Endstations
PR_DEP, PR_ARR, CS_DEP, CS_ARR = 0, 17, 9, 8
end_dep = lambda st: st in [PR_DEP, CS_DEP]
end_arr = lambda st: st in [PR_ARR, CS_ARR]
end_stop = lambda st: end_dep(st) or end_arr(st)

# Driving times
avg_driving_times = {
    k: v for k, v in zip(filter(lambda i: i != 8, range(number_of_stops - 1)),
                         [110, 78, 82, 60, 100, 59, 243, 135, 134, 243, 59, 101, 60, 86, 78, 113])
}

end_to_end_time = 17


# Color output
def colored(color, s):
    color_code = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, }[color]
    return "\033[{0};1m{1}\033[0m".format(color_code, s)
