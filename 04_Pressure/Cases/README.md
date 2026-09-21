# Cases

FDS inputs for the pressure-solver exercises, one directory per case.

Each case holds its input file, a `README.md` describing what to run and what to
look for, an `eval.py` that turns device output into a figure, and three data
directories:

| directory          | contents                     | in git |
| ------------------ | ---------------------------- | ------ |
| `reference/`       | runs made ahead of the class | yes    |
| `reference/plots/` | figures made from those runs | yes    |
| `results/`         | output from your own run     | no     |
| `plots/`           | figures made by `eval.py`    | no     |

Each reference run keeps the input that produced it alongside its output, so a
reference number can always be traced back to the exact case that gave it.

`reference/` matters more than it looks. Not every case can be run in a
classroom — some want many MPI processes and a long wall clock — so for those it
is the only data there will ever be, and it is what the figures on the slides
were made from. `eval.py` therefore reads `results/` when you have run the case
and falls back to `reference/` when you have not, saying which it used. Nobody
has to remember a flag, and every case can be plotted on a laptop.

## Requirements

`fds` and `mpirun` have to be on your PATH. `eval.py` also needs pandas and
matplotlib:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib
```

## Running a case

Run a case from inside its `results/` directory, so everything FDS writes stays
with the copy of the input that produced it, and one MPI process per mesh:

```bash
cd example_1
cp Example_1.fds results/Example_1_FFT.fds   # name the copy for the variant
cd results
# then set CHID='Example_1_FFT' in the copy
mpirun -n 1 fds Example_1_FFT.fds            # one &MESH, so -n 1
```

Each case's own `README.md` gives the exact steps — `example_1` labels its runs
by solver variant, `example_2` has nothing to rename. On macOS and Linux, a
`run.sh` in each case does the whole sequence for you:

```bash
./run.sh            # example_2
./run.sh FFT        # example_1 and example_3, labelling the run by solver variant
./run.sh FFT        # example_4 and example_5, where FFT names one of several
                    # separate inputs
```

`example_4` and `example_5` also have a `submit.sh`, which queues their runs as
batch jobs, and `example_5` a `run_all.sh`, which does the same sequence one job
at a time on the machine you are sitting at.

## Cases

| case        | meshes / `-n` | runs in class | what it shows                                                          |
| ----------- | ------------- | ------------- | ---------------------------------------------------------------------- |
| `example_1` | 1             | yes, seconds  | single mesh, flow past an obstacle; velocity error vs pressure solver  |
| `example_2` | 1             | yes, seconds  | cut-cell sphere with a specified mass flux; tracer mass conservation   |
| `example_3` | 8             | yes, minutes  | duct across eight meshes; five solvers on flow, iterations and cost    |
| `example_4` | 16            | no, cluster   | methane pool fire; same five solvers on cost and on predicted velocity |
| `example_5` | 8             | no, hours     | fire in a sloped tunnel; the tunnel preconditioner, and UGLMAT         |

The process count follows the number of meshes in the input: a case with five
meshes wants `mpirun -n 5`. `example_4` and `example_5` reach theirs through a
`&MULT` rather than a `&MESH` line each. Neither belongs in a classroom hour:
`example_4` is two to sixteen hours a run on sixteen ranks, `example_5` a
quarter of an hour to a couple of hours on eight. Both ship a `reference/` with
every variant in it, so their figures can still be made on a laptop.

Figures that appear on the slides live in `../Section_2_assets/`,
`../Section_3_assets/` and `../Section_4_assets/`, not here, so the deck renders
without anyone having run a case.
