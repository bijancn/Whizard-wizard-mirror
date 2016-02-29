Steering with `local.json`
================================================================================

`processes`
--------------------------------------------------------------------------------
This is an array of processes. Each process object can have the following values

### Possible values for `purpose` ###
- `disabled`: Do nothing
- `integrate`: Produce the integration grid for `events` or `histograms`
- `events`: Produce `.hepmc`s and move them to the `rivet` folder
- `histograms`: Setup FIFOs and directly produce `yodas` with rivet
- `scan`: Define a `scan_object` within the `process` object together with
  `start`, `stop` and `stepsize`

### Values that depend on the `purpose` ###

### General values ###

More general values
--------------------------------------------------------------------------------
These apply for all processes:
- `whizard`: Set your own Whizard binary or just use `"whizard"` for an
  installed Whizard
- `data_output`: Select a folder where to put the results (NOT FUNCTIONAL YET)

General behavior
================================================================================
- `mpi_generate` can create integration and simulation sindarins from the values
  in `local.json` for you. For this functionality just give a
  `processname-template.sin` with a line `#ITERATIONS` and potentially
  `#SETSCAN`. For a `scan`, it is mandatory to give a template.
  It is assumed that the process name in sindarin is the same as `processname`
