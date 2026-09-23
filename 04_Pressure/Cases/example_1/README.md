# Example 1 — single mesh, flow around a confined obstacle

A 3.2 x 1.6 x 1.6 m box on one 32x16x16 mesh, inlet on `XMIN`, a door left OPEN
on `XMAX`, and an obstruction in the middle. Two devices integrate the normal
velocity over the inlet and over the open vent, so `VDOT_IN` and `VDOT_OUT`
should agree once the flow is developed. How well they agree is set by the
pressure solver and its velocity tolerance — that is what this case is for.

## Running

Pick the solver first: exactly one of the four `&PRES` lines in `Example_1.fds`
is active, and switching between them is the exercise. Then copy the input into
`results/` under a name that says which variant it is, set its `CHID` to match,
and run it there:

```bash
cp Example_1.fds results/Example_1_FFT.fds
cd results
# then set CHID='Example_1_FFT' in the copy
mpirun -n 1 fds Example_1_FFT.fds
```

One process, because the input has one `&MESH`. Naming the copy and its `CHID`
after the variant makes FDS name everything it writes the same way, so the four
runs sit side by side in `results/` instead of overwriting each other, and
nothing has to be renamed afterwards. Running from inside `results/` also keeps
everything the run produced in one place — including the copy of the input that
produced it — rather than loose in the case directory.

On Windows, run the same four steps from the CMDfds prompt the FDS installer
creates — a plain command prompt does not have FDS on its path — with `copy`
in place of `cp` and `mpiexec` in place of `mpirun`:

```bat
copy Example_1.fds results\Example_1_FFT.fds
cd results
rem then set CHID='Example_1_FFT' in the copy
mpiexec -n 1 fds Example_1_FFT.fds
```

If `mpiexec` fails, `where mpiexec` should list the copy that came with FDS
first; a Microsoft MPI installed alongside it can take its place.

### run.sh — macOS and Linux

`run.sh` does all of that for you:

```bash
./run.sh FFT
```

It takes the variant name — `FFT`, `FFT_tight`, `ULMAT_PARDISO` or
`ULMAT_HYPRE` — and makes the copy, rewrites the `CHID` and runs it in
`results/`.

It does not touch the `&PRES` lines: choosing the solver stays yours to do by
hand. What it does check, before copying anything, is that the line you left
uncommented is the variant you asked for, and it stops if not:

```
The active &PRES line in Example_1.fds is FFT, but you asked for ULMAT_PARDISO.
Either edit Example_1.fds to uncomment the ULMAT_PARDISO line, or run:
  ./run.sh FFT
```

Since the variant becomes the `CHID`, a mismatch would otherwise bake the wrong
solver name into every output file, the `.smv` and the slices included.

## Viewing

```bash
In the results directory:
smokeview Example_1_FFT
```

Smokeview has to be started from `results/`: the `.smv` file names its slice
and boundary files without a path, so it only finds them when they are in the
working directory. Opening `results/Example_1_FFT.smv` from the case directory
gives you the geometry but no slices to load.

Each variant writes its own `.smv`, so once you have run several you can open
them one after another and compare.

## The four runs

`Example_1.fds` ships with one `&PRES` line active and three commented out. Run
it once per variant, commenting and uncommenting as you go:

Each `&PRES` line carries a `! VARIANT=` tag naming the argument to pass:

| variant         | `&PRES` line                                           | what to look for                                             |
| --------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| `FFT`           | `SOLVER='FFT'`                                         | the default; penetration error at the obstacle and back wall |
| `FFT_tight`     | `VELOCITY_TOLERANCE=0.001, MAX_PRESSURE_ITERATIONS=50` | error reduced, more pressure iterations                      |
| `ULMAT_PARDISO` | `SOLVER='ULMAT PARDISO', CHECK_POISSON=T`              | unstructured direct solve; error at machine precision        |
| `ULMAT_HYPRE`   | `SOLVER='ULMAT HYPRE', CHECK_POISSON=T`                | same solution, iterative, more scalable in memory            |

In Smokeview, load the temperature slice, the divergence slice, and the
**velocity error** boundary slice. `Example_1_FFT.out` reports the pressure
iterations taken, the maximum velocity error, and the mesh and cell where it
occurs.

## Plotting

```bash
python eval.py                       # FFT, from results/ or reference/
python eval.py ULMAT_PARDISO         # a different variant
python eval.py FFT --dir reference   # use the reference run
```

`eval.py` reads `results/` when you have run the variant and falls back to the
shipped `reference/` run when you have not, so it works before you run anything.
It writes a PDF to `plots/` and prints the maximum in-out volume flow difference
over the steady part of the run, signed: negative means more volume entering
than leaving at that instant. Against the reference runs those are 0.566 %,
-0.0198 %, -6.25E-13 % and -2.19E-11 % — the table on the slides. The reference set
was produced with FDS 6.11.1; a different build will shift the two FFT numbers.

The same four figures, made from `reference/`, are in `reference/plots/`, so you
can see what the runs look like before running one — or without a Python that
has pandas and matplotlib.

## Directories

- `reference/` — runs made ahead of the class, committed; `eval.py` uses these
  when `results/` is empty, so you can plot before running anything. Each run
  keeps the three files that describe it: the input that produced it
  (`Example_1_FFT.fds` and so on, `CHID` and `&PRES` line as they ran), its
  `.out` log and its `_devc.csv`.
- `reference/plots/` — the four figures already made from those runs.
- `results/` — your FDS output. Ignored by git.
- `plots/` — generated figures. Ignored by git.
