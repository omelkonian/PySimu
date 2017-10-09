# Parameters
q = 5 * 60  # Turnaround time
f = 2  # Tram frequency
c = 420  # Tram capacity
DD = 60  # Departure delay threshold

# Lambdas
initial_l = 100  # Passenger arrival rate

# Trams
number_of_trams = 13

# Stops
stop_names = [
    # P+R -> CS
    "P+R De Uithof",
    "WKZ",
    "UMC",
    "Heidelberglaan",
    "Padualaan",
    "Kromme Rijn",
    "Galgenwaard",
    "Vaartsche Rijn",
    "Central Station",
    # CS -> P+R
    "Central Station ->",
    "Vaartsche Rijn ->",
    "Galgenwaard ->",
    "Kromme Rijn ->",
    "Padualaan ->",
    "Heidelberglaan ->",
    "UMC ->",
    "WKZ ->",
    "P+R De Uithof ->",
]
number_of_stops = len(stop_names)

# Driving times
driving_times = {
    k: v for k, v in zip(filter(lambda i: i != 8, range(number_of_stops - 1)),
                         [110, 78, 82, 60, 100, 59, 243, 135, 134, 243, 59, 101, 60, 86, 78, 113])
}
total_driving_time = 17 * 60
end_to_end_time = q + total_driving_time

# Endstations
PR_DEP, PR_ARR, CS_DEP, CS_ARR = 0, 17, 9, 8
end_dep = lambda stop: stop in [PR_DEP, CS_DEP]
end_arr = lambda stop: stop in [PR_ARR, CS_ARR]
