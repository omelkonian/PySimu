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
  * [ ] Transformations
    - p-out percentages
    - driving times per segment
  * [ ] Plot derived histograms
- Passengers
  * [ ] Retrieve λ-rate from data
  * [ ] Fing P-out distribution from data fitting (for each stop)
  * [ ] Just in time passengers check the difference in dwell time
