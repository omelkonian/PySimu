import numpy as np
from Constants import avg_driving_times, gamma_shape


# TODO value sanitization


def gen_passenger_arrival(state):
    return np.random.exponential(1/state.lambda_)


def gen_driving_time(source):
    return np.random.gamma(shape=gamma_shape, scale=avg_driving_times[source]/gamma_shape)


def gen_passenger_exit_percentage():
    return np.random.uniform(0, 1)  # TODO get from matlab


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
