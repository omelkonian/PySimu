import numpy as np
from collections import deque

from Constants import avg_driving_times, number_of_stops, end_arr


# Helpers
def index_stop(index):
    return {
        x: ((int(number_of_stops / 2) - 1 - x) if x < 9 else (x - int(number_of_stops / 2))) for x in range(18)
    }[index]


# Driving times
gamma_shape = np.loadtxt('matlab/gamma_shape.csv').tolist()


def gen_driving_time(source):
    return np.random.gamma(shape=gamma_shape, scale=avg_driving_times[source]/gamma_shape)


# Passenger In
lambdas = deque(np.loadtxt('matlab/pin_lambdas.csv', delimiter=',').tolist())
next_lambda = lambda: lambdas.popleft()


def gen_passenger_arrival(state, stop, total=None):
    if end_arr(stop) and total:
        return 0
    lambda_per_second = state.lambdas[index_stop(stop)]/(15 * 60)
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
driving_parameters = deque(
    map(lambda i: [(x, y) for x in i[0] for y in i[1]],
        zip(np.loadtxt('matlab/pout_a.csv', delimiter=',').tolist(),
            np.loadtxt('matlab/pout_b.csv', delimiter=',').tolist())))
next_driving_parameter = lambda: driving_parameters.popleft()


def gen_passenger_exit_percentage(state, stop):
    a, b = state.driving_parameters[index_stop(stop)]
    if a == 0 or b == 0:
        return 0
    # return np.random.uniform(0, 1)
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
