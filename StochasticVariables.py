import numpy as np
from collections import deque

from Constants import avg_driving_times, door_block_time

# Get data from CSV files produces by Matlab scripts
gamma_shape = np.loadtxt('matlab/gamma_shape.csv').tolist()
lambdas = deque(np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist())
next_lambda = lambda: lambdas.popleft()
driving_parameters = deque([(a[0], a[1]) for a in np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist()])


# Driving time
def gen_driving_time(source):
    return np.random.gamma(shape=gamma_shape, scale=avg_driving_times[source]/gamma_shape)


# Passenger In
def gen_passenger_arrival(state, stop):
    lambda_per_second = state.lambdas[stop]/(15 * 60)
    if lambda_per_second > 0.02:
        return np.random.exponential(1/lambda_per_second)
    else:
        mins = state.time.time.minute
        next_quarter = int(np.floor(mins / 15)) + 1
        return 2 * (((next_quarter * 15) - mins) * 60)


# Passenger Out
def gen_passenger_exit_percentage(stop):
    a, b = driving_parameters[stop]
    return 0 if (a * b == 0) else np.random.beta(a, b)


# Dwell time
def gen_dwell_time(state, p_in, p_out):
    assert p_in >= 0 and p_out >= 0
    db_time = door_block_time if np.random.sample() < state.db else 0  # Door blocking
    dwell_time = 12.5 + 0.22 * p_in + 0.13 * p_out  # Passenger transfer
    return db_time + dwell_time


def gen_intermediate_dwell_time(number_of_passengers):
    return 0.22 * number_of_passengers
