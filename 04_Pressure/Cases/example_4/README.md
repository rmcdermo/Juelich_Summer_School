# Example 4 — sixteen meshes, a methane pool fire

The Sandia 1 m low flow rate methane pool fire, Test 14, at 3 cm resolution:
16 meshes of 48x48x32 cells, 1.18 million cells in total, 20 s of simulated
time. Sandia measured vertical and radial velocity across the plume at three
heights, and those measurements are in `experimental/`.

This is the case the earlier ones were building up to. Examples 1 to 3 are
arranged so that one solver is plainly right; here all five predict the same
flow, and what separates them is what they cost to get there.

**These runs belong on a cluster.** Sixteen MPI processes each, and from two to
sixteen hours of wall clock — see the table below. Nothing in the exercise
needs you to run them yourself: `reference/` holds the output of all five, so
every figure can be made on a laptop.

## The five runs

One input file per solver, each with its `CHID` already set. There is no line
to comment in and out — these are meant to be queued, not edited between runs.

| input                          | `&PRES` line                                             | wall clock |
| ------------------------------ | -------------------------------------------------------- | ---------- |
| `Example_4_FFT.fds`            | `SOLVER='FFT'`                                           | 2.2 h      |
| `Example_4_ULMAT.fds`          | `SOLVER='ULMAT'`                                         | 7.2 h      |
| `Example_4_FFT_tight.fds`      | `SOLVER='FFT', VELOCITY_TOLERANCE=1E-4, MAX_PRESSURE_ITERATIONS=1000` | 7.5 h |
| `Example_4_UGLMAT_HYPRE.fds`   | `SOLVER='UGLMAT HYPRE', MAX_PRESSURE_ITERATIONS=1`       | 5.4 h*     |
| `Example_4_UGLMAT_PARDISO.fds` | `SOLVER='UGLMAT PARDISO', MAX_PRESSURE_ITERATIONS=1`     | 11.7 h*    |

The wall clock column is the total elapsed time in each reference run's `.out`,
16 ranks with a core each. `UGLMAT_PARDISO` is the deck's `UGLMAT`, named for
the backend it uses and asking for it explicitly rather than leaving it to the
default, which has changed between FDS versions.

\* The two global runs carry `MAX_PRESSURE_ITERATIONS=1`, and so do their
reference runs, which average exactly one pressure iteration a step. A global
solve satisfies the velocity error in one pass — their `error` device reads
about 1e-15, round-off — so further iterations would only chase the inseparable
pressure residual after the velocity has already converged. Earlier runs
without the cap averaged about 2.5 iterations a step and took 6.2 h and 16.2 h
for the same velocity profiles. The cap is harmless here; in the long tunnel of
Example 5 it is not.

## Running

Each input defines its 16 meshes through a `&MULT`, so each wants 16 MPI ranks:

```bash
cp Example_4_FFT.fds results/
cd results
mpirun -n 16 fds Example_4_FFT.fds
```

Sixteen is not a suggestion: FDS stops with `ERROR(115)` if the process count
is below the mesh count, unless every `&MESH` names an `MPI_PROCESS`, and these
reach their sixteen through a `&MULT`. More than sixteen is simply idle.

Give each rank its own core. The third panel of the figure is a cost comparison
between solvers, and ranks sharing cores would show up in it as solver cost.

On macOS and Linux, `run.sh` does the copy and the run for one variant:

```bash
./run.sh FFT
```

### On a cluster

`submit.sh` queues all five as separate jobs — it is a Slurm example, so adapt
the directives to your own system. The five are independent and can sit in the
queue together.

```bash
./submit.sh
```

## Bringing the results back

Two files per run carry everything the figures need:

| file                          | what it is                                              |
| ----------------------------- | ------------------------------------------------------- |
| `Example_4_<V>_devc.csv`      | `iter`, `error` and `cputime` — all three solver panels |
| `Example_4_<V>_line.csv`      | `Wp3/Wp5/Wp9`, `Up3/Up5/Up9` — the velocity profiles    |

Ten small files for the five runs. Keep the `.out` log and the input that
produced it alongside them, as the other cases do, and the numbers stay
traceable; everything else a 1.18 million cell run writes can stay on the
cluster.

Those four `&DEVC` lines at the end of each input are what make this possible —
`PRESSURE ITERATIONS`, `MAXIMUM VELOCITY ERROR` and `CPU TIME` for the solver
comparison, and the six 32 point `POINTS` lines, time averaged from 10 s, for
the profiles.

## A note on the profile devices

The twelve radial `&DEVC` lines here do not ask for a `SPATIAL_STATISTIC`. The
deck's original inputs asked them for `'INTERPOLATION'`, and under FDS 6.10
that returned a value at each of the 32 points along the line. Under FDS 6.11
it returns one: the line spans four meshes in x and lies on the y mesh
boundary, and the interpolation stencil no longer reaches across a mesh, so 31
of the 32 points come back as zero and the profiles figure is empty.

Dropping `SPATIAL_STATISTIC` fixes it — FDS then reports the cell each point
falls in, which for these lines is the same thing to within half a cell, since
every one of the 32 points is already at an x cell centre. Moving the line off
the mesh boundary does not help; only dropping the statistic does. It is worth
knowing about if you ever lift these device lines into a case of your own: a
line device that crosses a mesh boundary is the thing to check.

The runs in `reference/` were made after the fix, so all five carry full
profiles and both figures come from the same set of runs.

## Plotting

```bash
python eval.py                       # the three solver panels
python eval.py profiles              # velocity profiles at z = 0.5 m
python eval.py profiles --height 0.9 # or at 0.3 and 0.9 m
python eval.py all                   # both
python eval.py all --dir reference   # use the reference runs
```

It reads `results/` once you have run anything there and falls back to
`reference/` when you have not, and writes PDFs to `plots/`. The same set, made
from `reference/`, is in `reference/plots/`.

`cputime` is FDS's `CPU TIME` device: seconds of processor time for the rank
that writes it, which is the run's wall clock when every rank owns a core. The
figure on the slide this replaces labels that axis in minutes, which it is not.

## Directories

- `experimental/` — Sandia's Test 14 measurements, vertical and radial velocity
  at z = 0.3, 0.5 and 0.9 m. Not ours, and read from here whichever run
  directory is in use.
- `reference/` — runs made ahead of the class, committed, so the figures can be
  made without running anything. All five match the inputs here, the two
  `UGLMAT` ones included, with `MAX_PRESSURE_ITERATIONS=1`.
- `reference/plots/` — the figures already made from those runs.
- `results/` — your FDS output. Ignored by git.
- `plots/` — generated figures. Ignored by git.
