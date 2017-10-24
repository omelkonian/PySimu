# Simulation of the Uithoflijn

Tested Python version: `3.5.2`

To setup: `pip install sortedcontainers numpy arrow click`

To execute you have 3 options:

 * `python Main.py run --help`:
     ```bash
     Usage: Main.py run [OPTIONS]

      Run simulation with given parameters.

      Options:
      -q INTEGER                     Turnaround time (in minutes).
      -f INTEGER                     Tram frequency (every <f> minutes).
      -db FLOAT                      Door block percentage.
      -nt INTEGER                    Number of trams.
      -edr TEXT                      Event display rate.
      -sdr TEXT                      State display rate.
      -tt, --track_tram TEXT         Track specific tram's events.
      -ts, --track_stop TEXT         Track specific stop's events.
      -p, --only_passengers BOOLEAN  Display only passengers' events.
      -s, --start TEXT               Start simulation later.
      -e, --end TEXT                 End simulation earlier.
      -A, --show_all TEXT            Show all events.
      -t, --etype TEXT               Filter on event type.
      --help                         Show this message and exit.
     ```

 * `python Main.py output_analysis --help`:
     ```bash
     Usage: Main.py output_analysis [OPTIONS]

      Run N simulations with given parameters and combine all statistics.

      Options:
        -n INTEGER  Number of runs.
        -q INTEGER  Turnaround time.
        -f INTEGER  Frequency.
        --help      Show this message and exit.

     ```
 * `python Main.py confidence_compare --help`:
     ```bash
     Usage: Main.py confidence_compare [OPTIONS]

       Run N simulations with given parameters and compute sample means and
       variances.

     Options:
       -n INTEGER  Number of runs.
       -qs TEXT    Turnaround time.
       -fs TEXT    Frequency.
       --help      Show this message and exit.

     ```

 * `python Main.py artificial_validation --help`
    ```bash
    Usage: Main.py artificial_validation [OPTIONS]

      Run N simulations with given parameters and combine all statistics.

    Options:
      -n INTEGER  Number of runs.
      -q INTEGER  Turnaround time.
      -f INTEGER  Frequency.
      -db FLOAT   Door block.
      --help      Show this message and exit.
    ```