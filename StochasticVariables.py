import numpy as np


def gen_passenger_arrival(state):
    return np.random.exponential(1/state.lambda_)


def gen_driving_time(state, source, target):
    return np.random.uniform(50, 150)


def gen_passenger_exit_percentage(state):
    return np.random.uniform(0, 100)


def gen_dwell_time(p_in, p_out):
    return 12.5 + 0.22 * p_in + 0.13 * p_out
