# PDS calibration using drunc

Four slides, including a title page. Audience: calibration and DAQ. Outcome:
request synchronized DAPHNE/calibration-box acquisition and a fast, repeatable
calibration loop in drunc with transitions that iterate
settings and runs while keeping readout services up until the scan completes.

The three grids are abstract parameter spaces, not measured response matrices.
The examples are VGAIN × offset, VGAIN × SiPM bias, and SiPM bias × LED bias.
Axes can be combined, including VGAIN × LED bias. LED bias is a drive setting,
not calibrated optical intensity; they are not two independent scan axes here.
No ranges, dependencies, device commands, or synchronization are implied.
The lifecycle diagram is a requested capability, not an implemented DAQ FSM.

The timing slide requires a shared master/command and measured LED-to-ADC delay.
The earlier independent-master exercise did not establish illuminated waveforms
or SSP synchronization. Pulse-count and phase checks are required when colocated.

The [branch review](branch-review.md) inventories the controls across all ten
remote branches, pinned in [branch-review.json](branch-review.json).

Build: `make decks/pds_calibration_daq_oct2026/main.pdf` from the repository root.
