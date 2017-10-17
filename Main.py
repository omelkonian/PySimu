import click

from State import State
from Events import Events
from Constants import PR_DEP, number_of_trams, number_of_stops
from Events import EndSim, Enqueue, PassengerArrival, LChange
from StochasticVariables import gen_passenger_arrival
from T import T


def initial_events(state):
    return [
        # Simulation end
        EndSim(T('00:00').shift(days=1)),
    ] + [
        # Rate changes
        LChange(T('06:15:00').shift(minutes=15 * i))
        for i in range(int((T('21:30:00').time - T('06:15:00').time).total_seconds() / 60 * 15))
    ] + [
        # Initial CS trams
        Enqueue(T('05:40:00').shift(minutes=2 * tr), tram=tr, stop=PR_DEP)
        for tr in range(4)
    ] + [
        # Initial PR trams
        Enqueue(T('06:00:00').shift(minutes=2 * tr), tram=tr + 4, stop=PR_DEP)
        for tr in range(4)
    ] + [
        # Peak trams
        Enqueue(T('07:00:00').shift(minutes=2 * tr), tram=tr + 8, stop=PR_DEP)
        for tr in range(number_of_trams - 8)
    ] + [
        # Initial passengers
        PassengerArrival(T('06:00:00').shift(seconds=gen_passenger_arrival(state)), st)
        for st in range(number_of_stops)
    ]


@click.command()
@click.option('--edr', default=25, help='Event display rate.')
@click.option('--sdr', default=50, help='State display rate.')
@click.option('--q', default=5 * 60, help='Turnaround time.')
@click.option('--f', default=4, help='Tram frequency.')
@click.option('--c', default=420, help='Tram capacity.')
@click.option('--dd', default=60, help='Big departure delay.')
@click.option('--db', default=.05, help='Door block percentage.')
def run(edr, sdr, q, f, c, dd, db):
    """Run simulation with given parameters (in seconds). """
    state = State(q, f, c, dd, db)  # load_matlab_data('parameters')
    events = Events()
    events.schedule(*initial_events(state))

    i, j = 0, 0
    while not state.end_simulation:
        event = events.next()
        event.handle(state, events)
        if i % edr == 0:
            print(event)
        if j % sdr == 0:
            print(state)
        i += 1
        j += 1
    print(state.statistics)


if __name__ == '__main__':
    run()
