import numpy as np
from Constants import driving_times


def gen_passenger_arrival(state):
    return np.random.randint(120, 240)
    # return np.random.exponential(1/state.lambda_)


def gen_driving_time(source):
    avg = driving_times[source]
    return np.random.uniform(avg - 20, avg + 20)


def gen_passenger_exit_percentage():
    return np.random.uniform(0, 1)


def gen_dwell_time(p_in, p_out):
    assert p_in >= 0
    assert p_out >= 0
    return 12.5 + 0.22 * p_in + 0.13 * p_out
