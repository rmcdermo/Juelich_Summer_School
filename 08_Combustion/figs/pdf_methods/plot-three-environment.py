"""Generate field images and pixel-count histograms from tracked grayscale inputs."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

output = Path(__file__).resolve().parent
inputs = output.parents[1] / "examples" / "variance_example"
cases = [("continuous", "transport_vs_mixing_0461_b.png"),
         ("discrete", "transport_vs_mixing_0461_a.png")]

for name, filename in cases:
    # Luminance gives one scalar sample per pixel, excluding the opaque alpha
    # channel. These inputs encode scalar fields as grayscale intensities.
    with Image.open(inputs / filename) as source:
        gray = source.convert("L")
    pixels = np.asarray(gray)
    counts = np.bincount(pixels.ravel(), minlength=256)
    low, high = gray.getextrema()
    if low == high:
        raise ValueError(f"Cannot normalize a constant image: {filename}")
    levels = np.clip((np.arange(256, dtype=float) - low) / (high - low), 0, 1)
    if name == "continuous":
        # Teaching-figure contrast adjustment requested for the continuous field:
        # keep the dark background at Z=0 and saturate roughly the brightest
        # 3% at Z=1. The background intensity is 55; a few antialiased pixels
        # fall below it and must not shift that entire region away from zero.
        # This remaps the image-derived scalar values, not just the colormap;
        # use the same lookup table for the field and its histogram below.
        white = np.searchsorted(np.cumsum(counts), 0.97 * pixels.size)
        black = 55
        levels = np.clip((np.arange(256, dtype=float) - black) / (white - black), 0, 1) ** 0.65
    bins = np.linspace(0, 1, 100)
    histogram, edges = np.histogram(levels, bins=bins, weights=counts)
    assert histogram.sum() == pixels.size

    # Only the displayed image is resized; the histogram uses every input pixel.
    display = gray.resize((800, 800), Image.Resampling.NEAREST)
    field = levels[np.asarray(display)]
    fig = plt.figure(figsize=(8, 3.5))
    cell = fig.add_axes([0.02, 0.17, 0.34, 0.777142857])
    im = cell.imshow(field, cmap="inferno", vmin=0, vmax=1,
                     interpolation="nearest", aspect="equal")
    cell.set(xticks=[], yticks=[])
    scale = fig.add_axes([0.38, 0.17, 0.018, 0.777142857])
    fig.colorbar(im, cax=scale, ticks=[0, 0.5, 1])
    scale.tick_params(labelsize=10)
    ax = fig.add_axes([0.52, 0.17, 0.46, 0.777142857])
    ax.bar(edges[:-1], histogram, width=np.diff(edges), align="edge",
           color="blue", edgecolor="black", linewidth=0.3)
    ax.set(xlim=(0, 1), xlabel=r"$Z$")
    ax.tick_params(direction="in", labelsize=10)
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax.xaxis.label.set_size(13)
    for axes in (cell, scale, ax):
        for spine in axes.spines.values():
            spine.set_color("0.5")
    fig.savefig(output / f"three-environment-{name}.svg")
    plt.close(fig)
    mean = np.dot(counts, levels) / pixels.size
    variance = np.dot(counts, (levels - mean) ** 2) / pixels.size
    print(f"{name}: {pixels.size:,} pixels; mean={mean:.6f}; variance={variance:.6f}")
    print(f"  Z<0.01: {counts[levels < 0.01].sum() / pixels.size:.2%}; "
          f"Z=1: {counts[levels == 1].sum() / pixels.size:.2%}")
