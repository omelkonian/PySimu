import numpy as np
from collections import deque

from Constants import avg_driving_times, end_arr


# Get data from CSV files produces by Matlab scripts
gamma_shape = np.loadtxt('matlab/gamma_shape.csv').tolist()
lambdas = deque(np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist())
next_lambda = lambda: lambdas.popleft()
driving_parameters = deque([(a[0], a[1]) for a in np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist()])


# Driving time
def gen_driving_time(source):
    return np.random.gamma(shape=gamma_shape, scale=avg_driving_times[source]/gamma_shape)


# Passenger In
def gen_passenger_arrival(state, stop, total=None):
    if end_arr(stop) and total:
        return 0
    lambda_per_second = state.lambdas[stop]/(15 * 60)
    if total is None:
        distr = lambda l: np.random.exponential(1/l)
    else:
        distr = lambda l: np.random.poisson(l * total)
    if lambda_per_second > 0.01:
        return distr(lambda_per_second)
    else:
        mins = state.time.time.minute
        next_quarter = int(np.floor(mins / 15)) + 1
        return ((next_quarter * 15) - mins) * 60


# Passenger Out
def gen_passenger_exit_percentage(stop):
    a, b = driving_parameters[stop]
    if a == 0 or b == 0:
        return 0
    return np.random.beta(a, b)


# Dwell time
def gen_dwell_time(state, p_in, p_out):
    assert p_in >= 0
    assert p_out >= 0
    dwell_time = 0
    # Door blocking
    if np.random.sample() < state.db:
        dwell_time += 60
    # Passenger transfer
    dwell_time += 12.5 + 0.22 * p_in + 0.13 * p_out
    return dwell_time
