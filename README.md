Steering with `run.json`
================================================================================
Run schema that shows which values can be used are found 
[here](http://desy.de/~bcho/docson/#run-schema.json) (because Bitbucket does not allow custom HTML/Javascript).

Some extra comments below:

### Possible values for `purpose` ###
- `disabled`: Do nothing
- `integration`: Produce the integration grid for `events` or `histograms`
- `events`: Produce `.hepmc`s and move them to the `rivet` folder
- `histograms`: Setup FIFOs and directly produce `yodas` with rivet
- `scan`: Setup a scan over values, see `scan_object`,

### General values ###
- `whizard_options`: (optional) argument to Whizard. Default is '--no-banner'

### For all processes ###
- `whizard`: (optional) Allows to set an absolute path to your Whizard binary.
  Default is `whizard` which works with an installed Whizard.
- `data_output`: Select a folder where to put the results (NOT FUNCTIONAL YET)

General behavior
================================================================================
- `mpi_generate` can create integration and simulation sindarins from the values
  in `run.json` for you. For this functionality just give a
  `processname-template.sin` with a line `#ITERATIONS` and potentially
  `#SETSCAN`. For a `scan`, it is mandatory to give a template.
  It is assumed that the process name in sindarin is the same as `processname`

Plotting with `plot.json`
================================================================================
Plot schema that shows which values can be used are found 
[here](http://desy.de/~bcho/docson/#plot-schema.json) (because Bitbucket does not allow custom HTML/Javascript).