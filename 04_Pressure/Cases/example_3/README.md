# Example 3 — eight meshes, duct flow across every mesh boundary

The geometry is the FDS verification case
`Examples/Pressure_Solver/duct_flow.fds`, which is where the figures on the
slides come from. Only the `&PRES` line and the `CHID` differ.

A 6.4 m cube split into eight 16x16x16 meshes, 0.2 m cells. Inside it a
1 m x 1 m duct runs a circuit that crosses every internal mesh boundary: along
`+x` low down, around to `+y`, back along `-x`, up a riser, and the same circuit
again on the upper level. An `&HVAC` fan inside the duct drives 1 m³/s through
it. Both ends of the duct, and all six domain boundaries, open into the room
around it.

The duct walls are thin obstructions — each `&OBST` has one dimension of zero
thickness, so FDS places it on a cell face as a sheet with no cells of its own
(no `THICKEN_OBSTRUCTIONS` here). That is what the case is for: a wall a single
face thick is the hardest thing to hold flow inside, and how well the
pressure solver manages it is the difference between the five `&PRES` lines in
`Example_3.fds`.

`in_net` measures what the fan puts into the duct and `out_net` what leaves the
far end. They should agree. What separates them is volume the solver lets
through the duct walls, which the open boundaries then carry away — and the
open boundaries matter: seal the room and the two agree whatever happens at the
walls, because the leak would have nowhere to go.

The inflow curve both figures are drawn against is UGLMAT's `in_net`, not the
fan's nominal 1 m³/s and not each panel's own first run. FDS ramps the fan up
over the first couple of seconds, so a flat line would not match the curves
there; and the inlet measurement is not solver-independent — GLMAT reads 0.9871
to 1.0067 at the fan face, FFT 0.9910 to 1.0054, because they leave velocity
error there too. UGLMAT holds 0.999902 to 1.000000 with the ramp included, so
its inlet device is the prescribed fan flow to within a rounding error.

The verification case's own `flow_in` and `flow_out` are still in the input,
but the figures use `in_net` and `out_net`. The difference is that the original
pair integrate one sign of the velocity only: a vortex passing the duct mouth
briefly draws air back in, that back-flow is dropped from the integral, and
`flow_out` reads above the fan even for a solver that is conserving volume to
the last digit. On UGLMAT it puts a 2 % bump on a curve whose net error is
1e-13.

## Running

Pick the solver first: exactly one of the five `&PRES` lines in `Example_3.fds`
is active, and switching between them is the exercise. Then copy the input into
`results/` under a name that says which variant it is, set its `CHID` to match,
and run it there with one MPI process per mesh:

```bash
cp Example_3.fds results/Example_3_FFT.fds
cd results
# then set CHID='Example_3_FFT' in the copy
mpirun -n 8 fds Example_3_FFT.fds
```

Eight processes, because the input has eight `&MESH` lines. Naming the copy and
its `CHID` after the variant makes FDS name everything it writes the same way,
so the five runs sit side by side in `results/` instead of overwriting each
other, and nothing has to be renamed afterwards. Running from inside `results/`
also keeps everything the run produced in one place — including the copy of the
input that produced it — rather than loose in the case directory.

On Windows, run the same four steps from the CMDfds prompt the FDS installer
creates — a plain command prompt does not have FDS on its path — with `copy`
in place of `cp` and `mpiexec` in place of `mpirun`:

```bat
copy Example_3.fds results\Example_3_FFT.fds
cd results
rem then set CHID='Example_3_FFT' in the copy
mpiexec -n 8 fds Example_3_FFT.fds
```

If `mpiexec` fails, `where mpiexec` should list the copy that came with FDS
first; a Microsoft MPI installed alongside it can take its place.

Each run takes on the order of a minute; the tighter FFT and the global solvers
take longer.

### run.sh — macOS and Linux

`run.sh` does all of that for you:

```bash
./run.sh FFT
```

It takes the variant name — `FFT`, `ULMAT`, `FFT_tight`, `GLMAT` or `UGLMAT` —
and makes the copy, rewrites the `CHID` and runs it in `results/`.

It does not touch the `&PRES` lines: choosing the solver stays yours to do by
hand. What it does check, before copying anything, is that the line you left
uncommented is the variant you asked for, and it stops if not:

```
The active &PRES line in Example_3.fds is FFT, but you asked for GLMAT.
Either edit Example_3.fds to uncomment the GLMAT line, or run:
  ./run.sh FFT
```

Since the variant becomes the `CHID`, a mismatch would otherwise bake the wrong
solver name into every output file, the `.smv` and the slices included.

## Viewing

```bash
In the results directory:
smokeview Example_3_FFT
```

Smokeview has to be started from `results/`: the `.smv` file names its slice
and boundary files without a path, so it only finds them when they are in the
working directory. Opening `results/Example_3_FFT.smv` from the case directory
gives you the geometry but no slices to load.

Load the velocity slices — `y = 1.5` and `y = 4.5` along the duct, `z = 1.5`
and `z = 4.5` across each level — to see whether the flow stays in the duct, and
the **velocity error** boundary slice to see where the solver is leaving error
behind. The `H` slices at the same planes show the pressure field the solver
produced. Each variant writes its own
`.smv`, so once you have run several you can open them one after another and
compare.

## The five runs

`Example_3.fds` ships with one `&PRES` line active and four commented out. Run
it once per variant, commenting and uncommenting as you go:

Each `&PRES` line carries a `! VARIANT=` tag naming the argument to pass:

| variant     | `&PRES` line                                                           | worst in–out gap | what to look for                                                 |
| ----------- | ---------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------------- |
| `FFT`       | `SOLVER='FFT'`                                                         | −60 %            | the default; most of the flow leaks through the duct walls       |
| `ULMAT`     | `SOLVER='ULMAT'`                                                       | −8 %             | unstructured per mesh; solid boundaries handled exactly          |
| `FFT_tight` | `SOLVER='FFT', VELOCITY_TOLERANCE=0.001, MAX_PRESSURE_ITERATIONS=1000` | −4 %             | the leak bought down with iterations — count them                |
| `GLMAT`     | `SOLVER='GLMAT'`                                                       | −79 %            | one structured matrix for all eight meshes, solved in every cell |
| `UGLMAT`    | `SOLVER='UGLMAT'`                                                      | 2e-11 %          | one unstructured matrix, gas cells only; velocity error at 1e-16 |

The gap column is what `eval.py` prints for the reference runs: the largest
instantaneous difference between `out_net` and `in_net` over the second half
of the run, as a percentage of the fan's 1 m³/s.

Nothing here is sealed, so there is one pressure zone and the two global
solvers default to HYPRE. 

## Plotting

```bash
python eval.py                       # volume flow in and out
python eval.py iterations            # pressure iterations and velocity error
python eval.py cost                  # wall clock time
python eval.py all                   # all three
python eval.py all --dir reference   # use the reference runs
```

Every figure overlays the variants, so `eval.py` plots whichever of the five it
finds and names the rest as missing — the figures are worth looking at after
the first run, not only after all five. It reads `results/` once you have run
anything there and falls back to the shipped `reference/` runs when you have
not, and writes PDFs to `plots/`.

`flow` comes out as two figures, the local solvers and the global ones, as on
the slide.

The three figures are the ones on the slides, literally: slides 68, 69 and 70
show these PDFs' SVG twins. Remaking the slide artwork is

```bash
python eval.py all --dir reference --svg
```

and copying `plots/Example_3_flow_local.svg`, `_flow_global.svg`,
`_iterations.svg` and `_cost.svg` over `Section_3_assets/slide-065-picture-02`,
`-065-picture-01`, `-066-picture-01` and `-067-picture-01`.

The same set as PDFs, made from `reference/`, is in `reference/plots/`, so you
can see what the runs look like before running one — or without a Python that
has pandas and matplotlib.

## Directories

- `reference/` — runs made ahead of the class, committed; `eval.py` uses these
  when `results/` is empty, so you can plot before running anything. Each run
  keeps the files that describe it: the input that produced it
  (`Example_3_FFT.fds` and so on, `CHID` and `&PRES` line as they ran), its
  `.out` log, its `_devc.csv` and its `_steps.csv`. The five were run one after
  another on an idle machine: a second job on the same cores would show up in
  the cost figure as solver cost.
- `reference/plots/` — the figures already made from those runs.
- `results/` — your FDS output. Ignored by git.
- `plots/` — generated figures. Ignored by git.
