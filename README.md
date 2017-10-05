## TODO
- [x] Proper time representation
  * e.g. `int` -> `arrow.Arrow`
- [ ] Handlers
  * [x] END_SIM
  * [x] F_TOGGLE
  * [x] L_CHANGE
  * [ ] TRAM_ARRIVAL
  * [ ] TRAM_DEPARTURE
  * [x] PASSENGER_ARRIVAL
  * [ ] Event for verifying if a tram can leave the station (40 sec rule)
- [ ] Spawn algorithm
  * [ ] Initial trams
  * [ ] Additional trams when F_TOGGLE
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
