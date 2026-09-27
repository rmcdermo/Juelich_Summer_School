#!/usr/bin/env bash
#
# Create a custom Jupyter kernel for Jupyter-JSC (JURECA), following the JSC
# how-to "Install kernel with venv":
#   1. virtual Python environment with extra packages
#   2. launch script kernel.sh (loads modules, activates venv, starts kernel)
#   3. kernel.json, linked into ~/.local/share/jupyter/kernels
#
# Run it in a JupyterLab terminal on JURECA (or on a JURECA login node).
# Afterwards the kernel appears in the JupyterLab launcher (restart JupyterLab
# if it doesn't show up after a minute).
#
#   ./make_jupyter_kernel.sh                   build the venv and register everything
#   ./make_jupyter_kernel.sh --link-only       link an existing (shared) venv into
#                                              this user's ~/.local/share/jupyter
#   ./make_jupyter_kernel.sh --link-only \
#       --venv /p/project1/<group>/jupyter/kernels/<name>
#
# Use --link-only for students: the venv is built once in the project directory,
# and every student links it into their own home. Jupyter-JSC runs JupyterLab from
# its own environment and searches each user's home for front-end extensions, so
# the linking has to happen per user even when the venv is shared.
#
# The venv is looked for under $PROJECT, which is each user's *primary* project --
# not necessarily the one holding the shared kernel. Set SHARED_VENV below to the
# absolute path so students need no arguments, or let them pass --venv.

set -eo pipefail

# ------------------------------------------------------------ settings
KERNEL_NAME=fire-summer-school-2026      # lower case, letters/digits/-/_ only
DISPLAY_NAME="Fire Summer School 2026"   # name shown in JupyterLab
STAGE_MODULE=Stages/2026                 # any stage works (not named STAGE: JSC uses that variable)

# Modules providing the base Python and (optionally) pre-built libraries.
# Pre-built JSC modules are preferable to pip for heavy packages.
MODULES=(GCC Python SciPy-bundle matplotlib)

# Extra packages installed with pip into the virtual environment
# (pygments already comes with ipykernel; listed to make it explicit)
PIP_PACKAGES=(fdsreader cantera seaborn pygments ipywidgets ipyfilechooser ipympl)

# Front-end (JupyterLab) extensions to expose to the Lab server. The server runs
# from its own environment and never looks inside this venv, so a package that ships
# a front end -- ipympl does, which is what makes %matplotlib widget render -- stays
# invisible until it is linked into the user's Jupyter data directory.
# List the extension directory names, or use "all" for everything the venv provides.
# Only ipympl is linked by default: the venv also carries its own copy of the
# ipywidgets manager, and overriding the server's with it is a good way to break
# widgets that currently work.
LINK_LABEXTENSIONS=(jupyter-matplotlib)

# Where the virtual environment lives. $HOME has a small quota, so the project file
# system is the better place.
#
# $PROJECT is whoever's *primary* project, which is not necessarily the one holding a
# shared kernel: a student in a different project would look in the wrong place and find
# nothing. Put the absolute path here once and everyone finds it, whatever their own
# project is. Leave it empty to work inside your own $PROJECT.

# e.g. /p/project1/cias-7/jupyter/kernels/fire-summer-school-2026
SHARED_VENV="/p/project1/cias-7/jupyter/kernels/fire-summer-school-2026"   

KERNEL_VENVS_DIR=${KERNEL_VENVS_DIR:-${PROJECT:-$HOME}/jupyter/kernels}
KERNEL_SPECS_DIR=$HOME/.local/share/jupyter/kernels

# ------------------------------------------------------------ mode
LINK_ONLY=0
VENV_OVERRIDE=${SHARED_VENV:-}
usage() { echo "usage: $(basename "$0") [--link-only] [--venv PATH]"; exit "${1:-1}"; }

while (( $# )); do
    case $1 in
        --link-only) LINK_ONLY=1 ;;
        --venv)      shift; [[ $# -gt 0 ]] || usage; VENV_OVERRIDE=$1 ;;
        --venv=*)    VENV_OVERRIDE=${1#--venv=} ;;
        -h|--help)   usage 0 ;;
        *)           usage ;;
    esac
    shift
done

# ------------------------------------------------------------ checks
KERNEL_NAME=$(echo "$KERNEL_NAME" | tr '[:upper:]' '[:lower:]')
if [[ -n $VENV_OVERRIDE ]]; then
    VENV=$VENV_OVERRIDE
    KERNEL_VENVS_DIR=$(dirname "$VENV")
else
    VENV=$KERNEL_VENVS_DIR/$KERNEL_NAME
fi
LABEXT_DIR=$HOME/.local/share/jupyter/labextensions

if (( LINK_ONLY )); then
    if [[ ! -d $VENV ]]; then
        echo "ERROR: no kernel at $VENV"
        echo
        echo "If the shared kernel lives in a project other than your own, point at it:"
        echo "  $(basename "$0") --link-only --venv /p/project1/<group>/jupyter/kernels/$KERNEL_NAME"
        echo "or set SHARED_VENV near the top of this script, once, for everyone."
        echo
        echo "To build your own instead, run it without --link-only."
        exit 1
    fi
    if [[ ! -r $VENV || ! -x $VENV ]]; then
        echo "ERROR: $VENV exists but is not readable by you."
        echo "The owner needs to make it group-readable:  chmod -R g+rX $VENV"
        exit 1
    fi
else
    [[ -e $KERNEL_SPECS_DIR/$KERNEL_NAME ]] && { echo "ERROR: kernel $KERNEL_NAME already exists in $KERNEL_SPECS_DIR"; exit 1; }
    [[ -e $VENV ]] && { echo "ERROR: $VENV already exists"; exit 1; }
fi

# ------------------------------------------------------------ helpers
# Link the venv's prebuilt front-end extensions into the user's Jupyter data
# directory, which the Lab server does search. Prebuilt ("federated") extensions are
# self-contained directories holding a package.json, one level deep for plain names
# and two for scoped ones such as @jupyter-widgets/jupyterlab-manager.
link_labextensions() {
    local src=$VENV/share/jupyter/labextensions
    if [[ ! -d $src ]]; then
        echo "  no front-end extensions in $src -- nothing to link"
        return 0
    fi

    local wanted_all=0 name
    for name in "${LINK_LABEXTENSIONS[@]}"; do
        [[ $name == all ]] && wanted_all=1
    done

    local pkg rel target linked=0
    while IFS= read -r pkg; do
        rel=${pkg#"$src"/}
        if (( ! wanted_all )); then
            local keep=0
            for name in "${LINK_LABEXTENSIONS[@]}"; do
                [[ $rel == "$name" ]] && keep=1
            done
            (( keep )) || continue
        fi

        target=$LABEXT_DIR/$rel
        if [[ -L $target ]]; then
            echo "  $rel -> already linked ($(readlink "$target"))"
            continue
        elif [[ -e $target ]]; then
            echo "  $rel -> SKIPPED, a real directory is already there: $target"
            continue
        fi
        mkdir -p "$(dirname "$target")"
        ln -s "$pkg" "$target"
        echo "  $rel -> $target"
        linked=$((linked + 1))
    done < <(find "$src" -mindepth 2 -maxdepth 3 -name package.json | while read -r f; do dirname "$f"; done | sort)

    (( linked )) || echo "  (nothing new linked)"
}

link_kernelspec() {
    local spec_dir=$VENV/share/jupyter/kernels/$KERNEL_NAME
    [[ -d $spec_dir ]] || { echo "ERROR: no kernelspec in $spec_dir"; exit 1; }
    mkdir -p "$KERNEL_SPECS_DIR"
    if [[ -e $KERNEL_SPECS_DIR/$KERNEL_NAME || -L $KERNEL_SPECS_DIR/$KERNEL_NAME ]]; then
        echo "  kernel $KERNEL_NAME already registered in $KERNEL_SPECS_DIR"
    else
        ln -s "$spec_dir" "$KERNEL_SPECS_DIR/$KERNEL_NAME"
        echo "  kernel $KERNEL_NAME -> $spec_dir"
    fi
}

# ------------------------------------------------------------ 4. launcher icon
# Jupyter shows logo-32x32.png / logo-64x64.png next to kernel.json in the
# launcher. They are embedded here as base64 so that this script stays the only
# file that has to be copied around. Decoded with python rather than `base64`,
# whose decode flag differs between GNU and BSD.
#
# To use a different icon, replace the two blocks below with the output of:
#   python -c 'import base64,sys,textwrap; \
#     print(textwrap.fill(base64.b64encode(open(sys.argv[1],"rb").read()).decode(), 76))' ICON.png
write_base64() {
    # --link-only never activates the venv, so do not rely on `python` being on PATH.
    local py=$VENV/bin/python
    [[ -x $py ]] || py=$(command -v python3 || command -v python || true)
    [[ -x $py ]] || return 1
    "$py" -c 'import base64,sys; open(sys.argv[1],"wb").write(base64.b64decode(sys.stdin.read()))' "$1"
}

write_logos() {
    local dir=$1
    [[ -d $dir ]] || return 0
    if [[ ! -w $dir ]]; then
        echo "  icons: $dir is not writable, leaving it alone"
        return 0
    fi

    write_base64 "$dir/logo-32x32.png" <<'LOGO32' || { echo "  icons: could not be written"; return 0; }
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
LOGO32

    write_base64 "$dir/logo-64x64.png" <<'LOGO64' || { echo "  icons: could not be written"; return 0; }
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
LOGO64

    # ipykernel installs its own Python logo, including an SVG. JupyterLab prefers an
    # SVG over the PNGs, so the stale one has to go or the icon never changes.
    rm -f "$dir/logo-svg.svg"
    echo "  icons: wrote logo-32x32.png and logo-64x64.png to $dir"
}

# ------------------------------------------------------------ link-only
if (( LINK_ONLY )); then
    echo "Linking the shared kernel into $HOME ..."
    write_logos "$VENV/share/jupyter/kernels/$KERNEL_NAME"
    link_kernelspec
    echo "Front-end extensions:"
    link_labextensions
    echo
    echo "Done. Restart JupyterLab itself (not just the kernel) so the Lab server"
    echo "picks up the front-end extensions, then choose '$DISPLAY_NAME'."
    exit 0
fi

# ------------------------------------------------------------ 1. venv
module purge
module load "$STAGE_MODULE"
module load "${MODULES[@]}"
PYV=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python $PYV from $(which python)"

mkdir -p "$KERNEL_VENVS_DIR"
python -m venv --system-site-packages "$VENV"
source "$VENV/bin/activate"
export PYTHONPATH=$VENV/lib/python$PYV/site-packages:$PYTHONPATH

pip install ipykernel
if (( ${#PIP_PACKAGES[@]} )); then
    pip install "${PIP_PACKAGES[@]}"
fi

# ------------------------------------------------------------ 2. kernel.sh
# Must load exactly the same modules as used for building the venv.
cat > "$VENV/kernel.sh" <<EOF
#!/bin/bash
module purge
module load $STAGE_MODULE
module load ${MODULES[*]}

source $VENV/bin/activate
export PYTHONPATH=$VENV/lib/python$PYV/site-packages:\${PYTHONPATH}

exec python -m ipykernel "\$@"
EOF
chmod +x "$VENV/kernel.sh"

# ------------------------------------------------------------ 3. kernel.json
python -m ipykernel install --name="$KERNEL_NAME" --prefix "$VENV"
spec_dir=$VENV/share/jupyter/kernels/$KERNEL_NAME

python - "$spec_dir/kernel.json" "$VENV/kernel.sh" "$DISPLAY_NAME" <<'PY'
import json, sys
path, launcher, name = sys.argv[1:]
spec = {
    "argv": [launcher, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    "display_name": name,
    "language": "python",
    "metadata": {"debugger": True},
}
with open(path, "w") as f:
    json.dump(spec, f, indent=2)
PY

# quick test: all packages importable in the kernel environment
python -c "import fdsreader, cantera, seaborn, pygments, numpy, matplotlib; print('imports OK, cantera', cantera.__version__)"

write_logos "$spec_dir"
link_kernelspec
echo "Front-end extensions:"
link_labextensions
deactivate

echo
echo "Kernel '$DISPLAY_NAME' ($KERNEL_NAME) installed:"
echo "  venv      : $VENV"
echo "  launcher  : $VENV/kernel.sh"
echo "  kernelspec: $KERNEL_SPECS_DIR/$KERNEL_NAME -> $spec_dir"
echo "  labexts   : $LABEXT_DIR"
echo
echo "Restart JupyterLab itself (not just the kernel) so the Lab server picks up the"
echo "front-end extensions -- otherwise %matplotlib widget reports"
echo "\"Failed to load model class 'MPLCanvasModel'\"."
echo
echo "Students use the same venv without rebuilding it:"
echo "  ./$(basename "$0") --link-only --venv $VENV"
echo "(or set SHARED_VENV in the script so they need no arguments)"
echo
echo "Add packages later with:"
echo "  module purge; module load $STAGE_MODULE ${MODULES[*]}"
echo "  source $VENV/bin/activate; pip install <package>; deactivate"
echo "Then restart the kernel in JupyterLab."
