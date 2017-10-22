import csv
import click
from functools import reduce

from Statistics import Statistics
from State import State
from Events import *
from T import T


def initial_events(state):
    it = int(state.initial_trams/2)
    pk = state.nt - 2 * it
    pk_cs = int(floor(pk/2))
    pk_pr = int(ceil(pk/2))
    return [
        # Simulation end
        EndSim(T('23:00:00')),
    ] + [
        # Rate changes
        LChange(T('06:15:00').shift(minutes=15 * i))
        for i in range(4 * 15)
    ] + [
        # Initial trams (CS)
        Enqueue(T('05:30:00').shift(minutes=offpeak_f * tr), tram=tr, stop=PR_DEP, nonstop=CS_DEP)
        for tr in range(it)
    ] + [
        # Initial trams (PR)
        Enqueue(T('06:00:00').shift(minutes=offpeak_f * tr), tram=tr + it, stop=PR_DEP)
        for tr in range(it)
    ] + [
        # Peak trams (CS)
        Enqueue(T('07:00:00').shift(minutes=-(state.q + end_to_end_time)),
                tram=tr + 2 * it, stop=PR_DEP, nonstop=CS_DEP)
        for tr in range(pk_cs)
    ] + [
        # Peak trams (PR)
        Enqueue(T('07:00:00'), tram=tr + 2 * it + pk_cs, stop=PR_DEP)
        for tr in range(pk_pr)
    ] + [
        # Destroy trams in the evening
        TramDestroy(T('19:00:00'), state.nt - state.initial_trams)
    ] + sum([[
        # Initial passengers
        PassengerArrival(T('06:00:00').shift(minutes=st), st + offset)
        for st in range(0, 9) if not end_arr(st)
    ] for offset in [0, 9]], [])


@click.group()
def simulate():
    pass

@simulate.command()
# Parameters
@click.option('-q', default=5, help='Turnaround time (in minutes).')
@click.option('-f', default=4, help='Tram frequency (every <f> minutes).')
@click.option('-db', default=.1, help='Door block percentage.')
@click.option('-nt', default=13, help='Number of trams.')
# Display
@click.option('-edr', default=None, help='Event display rate.')
@click.option('-sdr', default=None, help='State display rate.')
@click.option('--track_tram', '-tt', default=None, help="Track specific tram's events.")
@click.option('--track_stop', '-ts', default=None, help="Track specific stop's events.")
@click.option('--only_passengers', '-p', type=bool, default=False, help="Display only passengers' events.")
@click.option('--start', '-s', default=None, help="Start simulation later.")
@click.option('--end', '-e', default=None, help="End simulation earlier.")
@click.option('--show_all', '-A', default=None, help="Show all events.")
@click.option('--etype', '-t', default='', help="Filter on event type.")
def run(edr, sdr, q, f, db, nt, track_tram, track_stop, only_passengers, start, end, show_all, etype):
    """Run simulation with given parameters (in seconds). """
    state = State(nt, q, f, db, T(start) if start else None)
    events = Events()
    events.schedule(state, *initial_events(state))

    if end:
        events.schedule(state, EndSim(T(end)))

    i = 0
    while not state.end_simulation:
        event = events.next()
        event.handle(state, events)

        constraints = []
        if track_tram:
            constraints.append((any([isinstance(event, t) for t in [TramArrival, TramDeparture, Enqueue]]))
                               and event.tram in map(int, str.split(track_tram, ',')))
        if track_stop:
            constraints.append(not any([isinstance(event, t) for t in [EndSim, LChange, TramDestroy]])
                               and event.stop in map (int, str.split(track_stop, ',')))
        if only_passengers:
            constraints.append(isinstance(event, PassengerArrival))

        if start:
            constraints.append(event.timestamp.time >= T(start + ':00').time)

        if etype != '':
            constraints.append(any(filter(lambda s: s in type(event).__name__, str.split(etype, ','))))

        if all(constraints) or show_all:
            if edr and i % int(edr) == 0:
                print(event)
            if sdr and i % int(sdr) == 0:
                print(state)
        i += 1
    print(state.statistics)


@simulate.command()
@click.option('-n', default=10, help="Number of runs.")
@click.option('-q', default=5, help="Turnaround time.")
@click.option('-f', default=4, help="Frequency.")
def output_analysis(n, q, f):
    stats_A = multi_run(n, start='07:00:00', end='11:00', q=q, f=f, nt=14, db=.1)
    stats_B = multi_run(n, start='07:00:00', end='11:00', q=q-2, f=f, nt=13, db=.01)
    with open('output_analysis_{}_{}.csv'.format(q, f), 'w+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ')
        csv_writer.writerow(['q', 'f', 'PA_A', 'PA_B', 'ST_A', 'ST_B'])
        row = list(map(lambda x: round(x, 2),
                       [q, f, stats_A.PA_avg, stats_B.PA_avg, stats_A.ST_avg, stats_B.ST_avg]))
        print()
        print(row)
        csv_writer.writerow(row)


def multi_run(n, *args, **kwargs):
    print()
    print(kwargs['nt'], end='', flush=True)
    return reduce(Statistics.combine, [single_run(*args, **kwargs) for _ in range(n)])


def single_run(q=5, f=4, db=.1, nt=13, start='06:00:00', end=None):
    """Run simulation with given parameters once."""
    state = State(nt, q, f, db, T(start) if start else None)
    events = Events()
    events.schedule(state, *initial_events(state))

    if end:
        events.schedule(state, EndSim(T(end)))

    while not state.end_simulation:
        event = events.next()
        event.handle(state, events)

    print('.', end='', flush=True)
    return state.statistics


if __name__ == '__main__':
    # run()
    output_analysis()
