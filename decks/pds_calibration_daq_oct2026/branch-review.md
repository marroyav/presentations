# PDS calibration control review

All ten remote branches fetched and inspected on 20 October 2026; revisions are
in `branch-review.json`. The three local branch heads match fetched branches.
Existing uncommitted PDS documentation was left untouched and is not evidence
for the conclusions below.

The original three grids were examples, not a complete control inventory.
SiPM bias must be represented. LED drive bias × SiPM bias is explicitly
implemented in the calibration matrix example and the VD coldbox scan branch.
The repository uses “intensity” as a label for LED drive codes; it supplies no
conversion to measured optical intensity. LED bias × intensity should therefore
not be drawn as two independent hardware axes.

| Controls | Evidence / treatment |
| --- | --- |
| VGAIN, SiPM bias, offset, trim | `marroyav/calibration`, `src/pds/calibration/plan.py`: composable axes. VGAIN and bias are shared by an AFE; offset and trim are per channel. |
| LED drive bias at 270 / 367 nm | Same planner: separate drive controls, not measured optical flux. |
| First / second LED width, pulse-pair delay | Same planner: composable axes. |
| LED mask, burst count | Same planner: supported controls; wavelength/channel selection belongs in point settings. |
| Pulse mode | `marroyav/vdcb-daq-scans`, `src/pds/core/ssp.py`: configurable SSP setting, not a numeric axis accepted by the matrix planner. |
| Correlation threshold | `main`, `src/pds/core/run.py`, `ScanXCorrThreshold`: legacy scan with LEDs off. |
| Self-trigger threshold | `marroyav/st-scan`, `src/pds/core/run.py`; `marroyav/vdcb-daq-scans`, `src/pds/core/scans.py`: explicit scan. Not supported by the newer calibration planner. |
| Bias-controller DAC; channel DAC gain flag | `marroyav/vdcb-daq-scans`, `src/pds/core/scans.py` and configuration examples; calibration planner validates gain flag for offset/trim. Retain as explicit settings, not extra claimed implemented axes. |
| Rate, acquisition duration/window, event count, settling | Acquisition settings; distinguish from detector/LED response axes. |
| Board/AFE/channel selection; timing domain | Point/run identity and configuration context. |
| Temperature, sensor identity | Optional context in matrix plans; not verified measurements or implemented sweep axes. |

The reviewed branch families are:

- `main`, `attscan_withLED`, `marroyav/commissioning_np02_02`,
  `marroyav/mezz_comissionning`: legacy LED-mask/drive and FE scans.
- `marroyav/st-scan`: adds explicit self-trigger threshold scans.
- `refactor/features_np02_commissioning`, `refactor/pds-run-simplify`:
  refactored scan/SSP controls and LED calibration workflows.
- `marroyav/vdcb-daq-scans`: explicit AFE-bias × LED-drive scan,
  VGAIN × LED-drive scan, LED mask selection and per-target settings.
- `marroyav/tp_ta_exploration`: runtime settings and single-axis acquisition.
- `marroyav/calibration`: Cartesian matrix planner and optical-settings callback.

Useful pinned examples:

- [SiPM bias × LED bias](https://github.com/DUNE/PDS/blob/bed0920192126456089d7d44930dbfb145268463/configs/calibration/sipm-bias-led-afe0.json)
- [Composable controls](https://github.com/DUNE/PDS/blob/bed0920192126456089d7d44930dbfb145268463/src/pds/calibration/plan.py)
- [VD coldbox scan implementations](https://github.com/DUNE/PDS/blob/06efc5c17558b81cc4237a449e75ea3646f267c5/src/pds/core/scans.py)

This is repository coverage, not proof that every physics calibration requirement
has been specified or qualified. The current matrix coordinator keeps DAQ running
between points; the slide's run-per-point transition loop remains the requested
DAQ capability. Control coverage is distributed across branches, not implemented
uniformly by one command.
