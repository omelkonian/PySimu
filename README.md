# Simulation of the Uithoflijn

To setup: `pip install sortedcontainers numpy arrow click`

To execute: 
 ```bash
 Usage: Main.py [OPTIONS]

   Run simulation with given parameters (in seconds).

 Options:
   --edr INTEGER  Event display rate.
   --sdr INTEGER  State display rate.
   --q INTEGER    Turnaround time.
   --f INTEGER    Tram frequency.
   --c INTEGER    Tram capacity.
   --dd INTEGER   Big departure delay.
   --help         Show this message and exit.
 ```

# TODO
- [x] Proper time representation
  * e.g. `int` -> `arrow.Arrow`
- [x] Handlers
  * [x] END_SIM
  * [x] F_TOGGLE
  * [x] L_CHANGE
  * [x] TRAM_ARRIVAL
  * [x] TRAM_DEPARTURE
  * [x] PASSENGER_ARRIVAL
  * [x] Event for verifying if a tram can leave the station (40 sec rule)
- [x] Spawn algorithm
  * [x] Initial trams
  * [x] Additional trams when F_TOGGLE
- [x] Performance measures
- [x] Command-line interface
- Stochastic Generators
  * [ ] Passenger inter-arrival times
  * [ ] Driving times, gamma distribution from data fitting
  * [ ] Dwell times
  * [ ] Passenger exit percentage
- Data mangling
  * [ ] Data understanding
    - Bus info (a + b)
    - Runtimes
    - Passenger Prognose
    - Stop correspondence
  * [ ] Transformations
    - p-out percentages
    - p-in -> some table to derive Poisson λ from fitting
    - driving times per segment
  * [ ] Data fittings
    - p-out percentage distribution
    - p-in to get Poisson process every 15min -> λ rates every 15min
    - driving times -> Gamma (a, b)
  * [ ] Plot derived histograms
- Optional
  * [ ] Just in time passengers check the difference in dwell time
