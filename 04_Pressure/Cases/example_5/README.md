# Example 5 — eight meshes, a fire in a sloped tunnel

128 m of tunnel, 4 m square in section, at 20 cm resolution: eight meshes of
80x20x20 cells laid end to end through a `&MULT`, 256k cells in all, 30 s of
simulated time. Air enters at 5 m/s at `x = 0` and the far end is `OPEN`. An
8 MW fire sits 40 m in — a 2 m x 2 m vent at 2000 kW/m².

The slope is put in through gravity rather than through the mesh. `GVEC` is
rotated 10° about `y`, so the tunnel stays aligned with the grid and the domain
stays a box, which is what lets the eight meshes be a single row of identical
blocks.

That row is the whole point of the case. A tunnel is the worst shape there is
for a domain-decomposed pressure solve: pressure information has to travel the
full 128 m, and with FFT it can only cross one mesh boundary per pressure
iteration. The default solver never gets there — it spends every time step on
its iteration cap without reaching the velocity tolerance.

## The three runs

Three inputs, one per variant, each with its `CHID` and its `&PRES` line already
set. Nothing to comment in and out.

| variant        | `&PRES` line                                                                  | what to look for                                                  |
| -------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `FFT`          | `VELOCITY_TOLERANCE=0.001, MAX_PRESSURE_ITERATIONS=2000`                      | pinned at 2000 iterations, tolerance never reached                |
| `FFT_TP`       | the same, plus `TUNNEL_PRECONDITIONER=T`                                      | the same solver, a few dozen iterations, tolerance reached        |
| `UGLMAT`       | `SOLVER='UGLMAT'`                                                             | velocity error at machine zero — and still several iterations     |

The tunnel preconditioner solves a one-dimensional problem along the tunnel
axis first and hands the result to FFT as a starting point, so the long-range
part of the pressure field is already there and the iteration only has to fix
what is local to the fire. The first two rows are the same solver with the same
tolerance and differ only in that.

The last row is the one to look at twice. UGLMAT assembles one unstructured
matrix over all eight meshes and solves it directly, so it leaves no velocity
error at the mesh boundaries to iterate away — its `error` device reads about
1e-15 m/s. It nonetheless runs six or seven pressure iterations per half time
step, because the velocity tolerance is not the only exit test: FDS also checks
the inseparable part of the pressure residual against `PRESSURE_TOLERANCE`, and
in a tunnel this long that is what keeps the loop going. One loop walks it down
through the 500 1/s² tolerance like this:

    2.05e+04 -> 1.77e+04 -> 8.82e+03 -> 3.66e+03 -> 1.46e+03 -> 5.52e+02 -> 1.95e+02

Those iterations are not optional here. Forcing `MAX_PRESSURE_ITERATIONS=1` here
leaves the residual three orders of magnitude above tolerance and the run goes
eventually numerically unstable. The same cap is harmless on Example 4, an open 
domain; the difference between the two cases is the point.

## Running

Eight meshes, so eight MPI processes, one per mesh:

```bash
./run.sh FFT_TP
```

`run.sh` copies the input into `results/` and runs it there, so everything FDS
writes stays with the copy of the input that produced it. The variant name is
already the `CHID`, so the three runs sit side by side instead of overwriting
each other.

Without the script the same thing by hand is:

```bash
cp Example_5_FFT_TP.fds results/
cd results
mpirun -n 8 fds Example_5_FFT_TP.fds
```

### All four

```bash
./run_all.sh          # one after another, on this machine
./submit.sh           # one job each, through Slurm
```

`run_all.sh` runs them one at a time on purpose: two of the three figures are
cost comparisons between solvers, and a second job on the same cores would show
up in them as solver cost. Budget a few hours — wall clock on the reference
machine, eight ranks, for the 30 s these cover:

| variant  | M4     | spark   |
| -------- | ------ | ------- |
| `FFT_TP` | 23 min | 17 min  |
| `UGLMAT` | 52 min | 60 min  |
| `FFT`    | 397 min| 169 min |

`submit.sh` is a Slurm example; adapt the directives to your own system. The
three runs are independent, so they can all sit in the queue at once.

What has to travel to a cluster is only the three `.fds` files, `submit.sh` and
`slice_pressit.sh` -- about 40 kB. What has to come back is each run's `.out`,
its `_devc.csv` and its sliced `_pressit_step2500.csv`; see below for the
slicing, which has to happen before the copy.

## Viewing

```bash
cd results
smokeview Example_5_FFT_TP
```

Smokeview has to be started from `results/`: the `.smv` file names its slice
files without a path, so it only finds them in the working directory.

Load the temperature slice at `y = 0` to see the plume tilt down the slope and
back-layer against the 5 m/s inflow, and the `H` slice at the same plane for
the pressure field the solver produced. Each variant writes its own `.smv`, so
once you have run several you can open them one after another and compare — the
plain FFT run, the one that never reaches its tolerance, is the interesting one
to look at.

## Plotting

```bash
python eval.py                       # pressure iterations against time
python eval.py cost                  # wall clock time against simulated time
python eval.py error                 # velocity error within one time step
python eval.py all                   # all three, plus a summary line per run
python eval.py all --dir reference   # use the reference runs
```

Every figure overlays whichever of the three runs it finds and names the rest as
missing, so the figures are worth looking at after the first run rather than
only after all three. `eval.py` reads `results/` once you have run anything
there and falls back to the shipped `reference/` runs when you have not.

Two files per run carry everything the figures need:

- `<run>_devc.csv` — `iter`, `error` and `cputime`, one row per output
  interval, from the three `&DEVC` lines at the end of each input. This is the
  whole of the iterations and cost figures.
- `<run>_pressit.csv` — one row per pressure iteration rather than per time
  step, written because each input asks `&DUMP` for `VELOCITY_ERROR_FILE`. It
  carries the velocity error and the pressure error and where in the domain
  each is worst. This is the whole of the error figure. FDS 6.10 and earlier
  called the file `_vel_err.csv`.

Nothing else is needed to redraw the slides, which matters because the plain
FFT run is a couple of hours: bring those two files back per variant and the
figures can be made anywhere.

The second of them needs cutting down first. The error figure draws one time
step, but the file holds every pressure iteration of the whole run — for the
plain FFT variant that is 2000 a half step for 2500-odd steps, around a
gigabyte. So before copying anything back:

```bash
python eval.py slice --dir results --step 2462   # needs pandas
./slice_pressit.sh 2462                          # needs only awk
```

Either writes `<run>_pressit_step2462.csv` beside each full file, a few hundred
kilobytes at most, and `eval.py` reads those when the full file is absent.
`reference/` here ships the slices, not the originals. The shell version is
there for clusters, where pandas often is not.

### Reading the error figure

`eval.py error` takes one time step apart and plots the velocity error against
the pressure iteration count inside it, predictor then corrector, with the
velocity tolerance drawn across. That is the figure on the last slide of the
section.

Picking the step takes a little care. FDS restarts the `Iteration` column at 1
every time it enters the pressure loop, and the loops do not come two per time
step: when `CHECK_STABILITY` rejects a predictor, the step is retaken with a
smaller `dt` and the rejected attempt is in the file too. `eval.py` defaults to
the last step FDS did not have to retake, and `--step N` overrides it.

### Remaking the slide artwork

```bash
python eval.py iterations --dir reference --svg
python eval.py cost       --dir reference --svg
python eval.py error      --dir reference --svg --variants FFT,FFT_TP --step 2462
```

and copy `plots/Example_5_iterations.svg`, `_wall_time.svg` and
`_velocity_error.svg` over `Section_4_assets/slide-075-iterations.svg`,
`slide-075-wall-time.svg` and `slide-076-velocity-error.svg`.

The first two figures carry all three runs. The error figure carries only two,
on purpose: it is there to show how far the iteration count and the work fall
when the preconditioner is switched on, and that is a comparison between FFT
and the same FFT with `TUNNEL_PRECONDITIONER=T`. Putting UGLMAT beside them
would change the question the figure is asking, and it would stretch the y axis
by nine decades to fit a flat line at machine zero. What UGLMAT costs, and what
capping it at one iteration saves, is the iterations and cost figures' job.

`--step 2462` is a step both runs took cleanly and where FFT spends its full
2000 iterations on each half -- which is what the deck's own figure shows. Not
every step looks like that: at the deck's 2500 this run's predictor happened to
converge in 210, which makes a lopsided panel. Leave `--step` off and `eval.py`
picks the last step FDS did not have to retake, per variant, which is a fair
sample but puts a different step number under each panel.

## Directories

- `reference/` — runs made ahead of the class, committed; `eval.py` uses these
  when `results/` is empty, so you can plot before running anything. Each run
  keeps the input that produced it, its `.out` log, its `_devc.csv` and its
  `_pressit.csv`. The three shipped here were run on the spark cluster, one job each.
- `reference/plots/` — the figures already made from those runs.
- `results/` — your FDS output. Ignored by git.
- `plots/` — generated figures. Ignored by git.
