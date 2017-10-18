# Simulation of the Uithoflijn

Tested Python version: `3.5.2`

To setup: `pip install sortedcontainers numpy arrow click`

To execute: 
 ```bash
 Usage: Main.py [OPTIONS]

  Run simulation with given parameters.

Options:
  -edr INTEGER                   Event display rate.
  -sdr TEXT                      State display rate.
  -q INTEGER                     Turnaround time.
  -f INTEGER                     Tram frequency.
  -c INTEGER                     Tram capacity.
  -dd INTEGER                    Big departure delay.
  -db FLOAT                      Door block percentage.
  -tt, --track_tram TEXT         Track specific tram's events.
  -ts, --track_stop TEXT         Track specific stop's events.
  -p, --only_passengers BOOLEAN  Display only passengers' events.
  -s, --start TEXT               Start simulation later.
  -e, --end TEXT                 End simulation earlier.
  -A, --show_all TEXT            Show all events.
  -t, --etype TEXT               Filter on event type.
  --help                         Show this message and exit.
 ```

# TODO
- [x] Proper time representation
- [x] Handlers
- [x] Spawn algorithm
- [x] Performance measures
- [x] Command-line interface
- [x] Stochastic Generators
- [x] Data mangling
- [ ] Data plotting
- [ ] Data direction-split
- [x] EXTRA: Just in time passengers check the difference in dwell time
- Report
  * [ ] Problem description
  * [ ] Assumptions
  * [ ] Quantitative analysis
  * [ ] Model explanation
    - [ ] Events
    - [ ] Event handlers
    - [ ] Performance measures
    - [ ] State
  * [ ] Input Analysis
    - [ ] Modelling of input data
    - [ ] Choice and motivation for applied distributions
  * [ ] Output Analysis
    - [ ] Questions answered by the experiments
    - [ ] Investigated scenarios
    - [ ] #runs
    - [ ] Tables
    - [ ] Graphs
    - [ ] Observations from tables/graphs
    - [ ] Statistical analysis
      * [ ] Compare interesting scenarios (>= 10), using confidence intervals
      * [ ] EXTRA: Comparison with a standard
      * [ ] EXTRA: All pairwise combinations
      * [ ] EXTRA: Ranking and selection
  * [ ] Results from the artificial model
  * [ ] Conclusions
  * [ ] Appendix: Interview minutes
  
