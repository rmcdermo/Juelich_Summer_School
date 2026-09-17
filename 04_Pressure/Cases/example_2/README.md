# Example 2 — specified mass flux from a sphere, and mass conservation

A 2.8 m cube on one 32x32x32 mesh with a `GEOM` sphere of radius 1 m at the
centre, blowing a propane tracer at a fixed 10 kg/m²/s for one second. The top
of the domain is OPEN. The sphere is cut into the Cartesian mesh, so this case
exercises the cut-cell discretisation and the unstructured pressure solve.

Total mass released is about 10 kg/m²/s x 12.6 m² x 1 s = 126 kg, and it has to
end up either out of the domain or still inside it.

## Running

Copy the input into `results/` and run it there:

```bash
cp Example_2.fds results/
cd results
mpirun -n 1 fds Example_2.fds
```

One process, because the input has one `&MESH`. Running from inside `results/`
keeps everything the run produced in one place — including the copy of the input
that produced it — rather than loose in the case directory.

On Windows the same steps work from the command prompt, with `copy` in place of
`cp`.

### run.sh — macOS and Linux

```bash
./run.sh
```

does exactly that.

## Viewing

```bash
cd results
smokeview Example_2
```

Smokeview has to be started from `results/`: the `.smv` file names its slice
and boundary files without a path, so it only finds them when they are in the
working directory. Opening `results/Example_2.smv` from the case directory
gives you the geometry but no slices to load.

## What to look at

In Smokeview: the geometry triangles (note how fine the surface mesh is, and
why), the temperature slice, and the tracer mass fraction as it leaves the
domain.

In `Example_2_devc.csv`, three devices carry the balance:

| device            | what it integrates                                        |
| ----------------- | --------------------------------------------------------- |
| `MASS IN TRACER`  | mass flux through the sphere surface, accumulated in time |
| `MASS OUT TRACER` | mass flux through the OPEN boundary, accumulated in time  |
| `MASS VOL TRACER` | tracer density integrated over the domain volume          |

and they should satisfy

```
MASS IN TRACER  ~=  MASS OUT TRACER + MASS VOL TRACER
```

Mass in and mass out are time integrals of a flux. FDS accumulates them with a
`&CTRL` PID controller whose proportional and derivative gains are zero and
integral gain is one, so the device reports a running total rather than a rate.

In the CSV, `MASS OUT TRACER` is negative: both flux devices measure
`MASS FLUX WALL`, and the wall normal at the OPEN boundary points the opposite
way to the one on the sphere. `eval.py` negates it, so what it prints and plots
is the magnitude.

## Plotting

```bash
python eval.py                    # results/, falling back to reference/
python eval.py --dir reference    # the reference run
```

Writes `plots/Example_2_mass_balance.pdf` and prints the three totals with the
closure error. Against the reference run:

```
mass in      1.2551E+02 kg
mass out     9.2833E+01 kg
mass in vol  3.2555E+01 kg
out + vol    1.2539E+02 kg   (0.10 % difference)
```

which is the balance on the slide. The same figure, made from `reference/`, is
in `reference/plots/`, so you can see it before running anything.

## The pressure solver

The sphere is a `GEOM`, so the domain has cut cells and the Poisson equation is
solved on an unstructured mesh — FFT cannot be used here. The input says so
explicitly:

```
&PRES SOLVER='ULMAT PARDISO' /
```

Three alternatives sit commented out below it. PARDISO is a direct solve and
HYPRE an iterative one; `ULMAT` solves each mesh on its own, `UGLMAT` solves all
meshes as one global system:

| `SOLVER`         | solve     | scope        |
| ---------------- | --------- | ------------ |
| `ULMAT PARDISO`  | direct    | mesh by mesh |
| `ULMAT HYPRE`    | iterative | mesh by mesh |
| `UGLMAT PARDISO` | direct    | all meshes   |
| `UGLMAT HYPRE`   | iterative | all meshes   |

With one mesh and one pressure zone all four give the same answer to round-off,
so what changes is the cost. Uncomment one at a time and compare the pressure
solver block near the top of `Example_2.out`, the wall clock time at the end of
it, and the mass balance from `eval.py`.

## Bonus

`&MISC CCVOL_LINK` sets the size threshold below which a small cut cell is
linked to a larger neighbour. The default is 0.5. Try 0.2 and 0.9 and watch what
happens to the number of time steps and to the mass balance — link fewer cells
and the smallest ones set the time step; link more and the balance loosens:

| CCVOL_LINK    | time steps | mass difference | time stepping |
| ------------- | ---------- | --------------- | ------------- |
| 0.2           | 704        | 0.06 %          | 171 s         |
| 0.5 (default) | 417        | 0.10 %          | 92 s          |
| 0.9           | 282        | 0.16 %          | 62 s          |

Measured with FDS 6.11.1 and `SOLVER='ULMAT PARDISO'` on one core; this is the
table on the slide. Only the default run is shipped in `reference/`, so these
three rows are something to reproduce rather than read back from a file.

## Directories

- `reference/` — a run made ahead of the class, committed; `eval.py` uses it
  when `results/` is empty, so you can plot before running anything. It keeps
  the three files that describe the run: the input that produced it
  (`Example_2.fds`), its `.out` log and its `_devc.csv`.
- `reference/plots/` — the figure already made from that run.
- `results/` — your FDS output. Ignored by git.
- `plots/` — generated figures. Ignored by git.

The reference run was made with FDS 6.11.1 with `SOLVER='ULMAT PARDISO'` at the
default `CCVOL_LINK=0.5`: 417 time steps, 92 s of time stepping on one core. A
different build will shift the last digits.
