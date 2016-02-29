Steering with `local.json`
================================================================================
Possible values for `purpose` are
- `disabled`: Do nothing
- `integrate`: Produce the integration grid for `events` or `histograms`
- `events`: Produce `.hepmc`s and move them to the `rivet` folder
- `histograms`: Setup FIFOs and directly produce `yodas` with rivet
- `scan`: Not functional yet
