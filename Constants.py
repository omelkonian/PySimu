from collections import deque

#
# General configuration
#

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

# Endstations
PR_DEP, PR_ARR, CS_DEP, CS_ARR = 0, 17, 9, 8
end_dep = lambda stop: stop in [PR_DEP, CS_DEP]
end_arr = lambda stop: stop in [PR_ARR, CS_ARR]


#
# Probability configuration TODO Get from CSV
#

# Passenger inter-arrival times
lambdas = deque(
    ([.05] * 8) +
    ([.2] * 48) +
    ([.05] * 8) +
    ([.2] * 48)
)
next_lambda = lambda: lambdas.popleft()

# Driving times
gamma_shape = 2.1
avg_driving_times = {
    k: v for k, v in zip(filter(lambda i: i != 8, range(number_of_stops - 1)),
                         [110, 78, 82, 60, 100, 59, 243, 135, 134, 243, 59, 101, 60, 86, 78, 113])
}
