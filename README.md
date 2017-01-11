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

Example usage
================================================================================
Create a new process folder. Create in there a `whizard` folder and in that
folder a `myprocess-template.sin`. Create a `run.json` in the process folder
with e.g. a scan job in there that uses `myprocess`. Then run it with
`../mpi_run_this.sh` (note that you likely need a `host_file`, that specifies
the nodes and cores to use, above the process folder but this depends on your
MPI installation. Check if `mpi_run_this.sh` uses a command that fits your
installation). In case you did a scan, you can extract the results with
`../extract-results.py` and plot it with `../plot-data.py`.

Steering with `run.json`
================================================================================
The run schema that shows which values can be used and what they do are found
[here](http://desy.de/~bcho/docson/#run-schema.json) (because Gitlab does not
allow custom Javascript, we can't show them here).

Plotting with `plot.json`
================================================================================
The plot schema that shows which values can be used and what they do are found
[here](http://desy.de/~bcho/docson/#plot-schema.json).
