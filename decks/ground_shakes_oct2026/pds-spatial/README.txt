APA2 PDS activity by physical section

Open viewer.html to play the channel map and section bars together.
Open apa2-pds-sections.pdf for the six-page printable supplement.
Open population/viewer.html for histograms across all 1,377 available APA2
records with a main-shake time. The paired plots compare the same recorded
channels at both stages of each event. The four-page report is
population/apa2-all-event-histograms.pdf.
The original five-event APA1/APA2 player remains at:
../../../../ground-shake-data/analysis/whole-event-spatial/viewer.html

Run 32731 events 52 and 33 are the two existing APA2 examples.
Each event has a channel map, six section histograms and a section-versus-time plot.
The main nine-slide presentation remains a separate file.

What a section means
Each of the ten sections is one physical PDS module, with four mapped inputs.
The module and channel order follows EDMS 3493627 v1, page 18.
This is a physical ordering, not a survey in centimetres.
Module 8 contains reported disconnected inputs 11, 13, 14 and 16.
Their recorded signals remain visible in the channel map but are excluded from
the connected-channel section bars. Missing inputs 10 and 17 are not labelled
disconnected.

What the plots measure
Signal size is the absolute distance from the channel's fixed baseline, in ADC
counts. It ignores pulse sign. It is not calibrated light or a photon count.
Each section bar takes the largest recorded connected-channel value in that
module. It does not sum or integrate channels. Counts beside the bars tell you
how many channels contributed. A missing channel can hide a larger signal.

The static channel maps and section histograms have separate scales for each
stage. The section time plot and player use one fixed logarithmic scale, which
shows both the small precursor and the large main shake.

What the existing maps show
In event 52 the largest recorded connected-channel response is in M6 (channel 1)
at the first pulse, M2 (24) at the second, M1 (20) at -60 us and M5 (5) at +10 us.
In event 33 the corresponding sections are M6 (1), M9 (47), M1 (22) and M7 (12).
The distribution changes, but these two examples do not establish a moving
source or one common source location. M7 has incomplete recording.
At +50 us, only four connected channels in event 52 and five in event 33 have
usable samples. Those snapshots cannot establish that other sections are quiet.

Timing and coverage
Snapshots are existing 0.512 us medians. Times are relative to the main TPC
threshold marker. Fixed stage labels are illustrative, not measured PDS onsets.
The full time series uses existing 0.512 us bins with at least 26 of 32 native
samples. Missing bins stay missing. Bins containing raw rail codes are excluded.
No detector data were decoded again to make these spatial plots.

Inputs and reproduction
input-snapshots.json preserves the selected events and hashes their original
results and validation records. input-time-series.npz preserves their existing
channel medians, sample counts and rail flags. input-time-series-source.json
identifies and hashes the original array archive.

From this directory:
python3 build.py
python3 make_viewer.py

channel-values.csv contains all signed snapshot values and coverage flags.
section-values.csv contains the plotted section maxima and channel counts.
section-time-values.npz contains the full section histories and coverage.
Each build creates a new dated evidence record. This is analysis evidence,
not an approved hardware diagnosis.
