Introduction
================================================================================
This repository is a collection of scripts to run `whizard` on a cluster via
`MPI`, extract the results and plot them with `matplotlib`.
Furthermore, various analyses are documented here in the form of sindarin
and Rivet C++ files.
All main plots of https://arxiv.org/abs/1609.03390 have been computed with
these scripts.
The steering of running `whizard` is done with a `run.json` in a process
folder.
The description of the plot is done with a `plot.json` in a process folder.
Various examples can be found in the folders named according to the respective
process.
The allowed variables and syntax of both `.json` files is documented and
validated against a schema: `plot-schema.json` and `run-schema.json`.

Example WHIZARD usage
================================================================================
Create a new process folder. Create in there a `whizard` folder and in that
folder a `myprocess-template.sin`. Create a `run.json` in the process folder
with e.g. a scan job in there that uses `myprocess`. Then run it with
`../mpi_run_this.sh` (note that you likely need a `host_file`, that specifies
the nodes and cores to use, above the process folder but this depends on your
MPI installation. Check if `mpi_run_this.sh` uses a command that fits your
installation). In case you did a scan, you can extract the results with
`../extract-results.py` and plot it with `../plot-data.py`.

Example stand-alone plot usage
================================================================================
Create a new process folder. Create in there a `scan-results` folder and
put in there the results you want to plot as a e.g. `myresults.dat`
file (the file is loaded with `numpy.loadtxt`, so a simple `1.0 1.0`
format for x, y values and `1.0 1.0 0.1` for x, y and yerr in each row
is fine).
Create a `plot.json` in the process folder that uses `myresults`
like
```
{
  "plots": [{
    "title": "myplot",
    "lines": [{"name": "myresults"}],
    "xlabel": "foo $x$",
    "ylabel": "bar $x^2$"
  }]
}
```
Create the plot with `../plot-data.py`. Enjoy your publication-level
plot in `plots/myplot.pdf`.
![example plot](https://bijancn.github.io/Whizard-wizard-mirror/standalone-example/plots/myplot.svg)
You can create any number of plots with any number of input data,
plotted as lines or bands, including automatic ratio plots normalized to
any of the input lines.  Furthermore, you can compose transformations of
data like rescalings, smoothing, fits to polynomials, combine two data
sets with an arbitrary function or even plot a custom function that you
supply, c.f. the steering with `plot.json`.

Steering with `run.json`
================================================================================
{% include run.html %}

Plotting with `plot.json`
================================================================================
{% include plot.html %}
