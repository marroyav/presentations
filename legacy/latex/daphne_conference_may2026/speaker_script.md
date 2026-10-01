# Speaker Script - DAPHNE Conference Presentation

Lead, South Dakota - Wednesday, May 20, 2026

Target pace: about 10 to 12 minutes. This is written as a simple read-aloud script, with short pauses between slides.

## Slide 1 - Title

Good morning. I am Manuel Arroyave, speaking on behalf of the PDS and DAQ groups.

Today I want to give a short update on DAPHNE electronics. I will focus on what has been measured, what still needs to close, and how this connects to DAQ and PRR.

The main point is simple. The mezzanine results look strong. The main open hardware item is common-mode noise on new DAPHNE. And for PRR, we also need the DAQ data format and calibration workflow to be well defined.

## Slide 2 - What Are We Presenting?

This talk is about DAPHNE moving from board tests into system integration.

We have cold-box evidence for the mezzanines. We have a mitigation path for the new-DAPHNE noise issue. And we have DAQ pieces that now need to become stable interfaces, not ad hoc tests.

So I will keep coming back to two questions: what is already demonstrated, and what still needs a clear owner or decision?

## Slide 3 - Presentation Structure

The talk has four parts.

First, I will show where the evidence fits in the full readout chain.

Then I will go through the mezzanine results: signal-to-noise, pulse shape, and dynamic range.

After that I will cover the new-DAPHNE common-mode noise issue and the filter work.

Finally, I will connect this to DAQ integration, calibration in `pds-run`, and the remaining PRR items.

## Slide 4 - System Context: Where The Evidence Lands

This is the readout chain I want to keep in mind.

The cold electronics and mezzanines prepare the signal. Firmware turns it into a data product. DAQ receives it, decodes it, stores it, and makes it available for monitoring and analysis.

That is why the plots are not just electronics plots. Each result has to land somewhere in this chain.

## Slide 5 - Mezzanine Evidence: Module Variants

Here we show the three mezzanine flavors.

The important point is the matching: HD cold electronics with the HD mezzanine, VD with VD, and SoF with SoF.

That matters because DAPHNE has to support all three cases. We are not only showing that one board works. We are showing that the integration has been addressed for HD, VD, and SoF.

## Slide 6 - Mezzanine Evidence: Functions Under Test

The mezzanine has three main jobs.

First, it converts the signal and applies AFE compensation to control the undershoot.

Second, it protects and monitors the cold-electronics power rails, including the 5 volt and 3.3 volt lines.

Third, it has to fit the three mechanical and electrical flavors: HD, VD, and SoF. The two-board flex-cable split is specific to SoF.

So the mezzanine evidence is not just one waveform. It covers signal handling, power protection, and the different module flavors.

## Slide 7 - Mezzanine Evidence: Installed Cold-Box Chain

This slide shows the chain used in the cold-box work.

On the front-panel side we have the optical input, the transimpedance readout, and ADC offset measurements. The second board carries the AFE compensation stage, the flex cable, and the DAPHNE interface.

The point is that the following measurements come from a realistic readout path, not from an isolated bench setup.

## Slide 8 - Mezzanine Evidence Map: Three Tests

There are three checks in the mezzanine evidence package.

First, signal-to-noise. In the November 2025 and January 2026 cold-box tests, the SNR is above 4 for the 1500 photoelectron setting.

Second, pulse recovery. The compensation stage reduces the large undershoot to the sub-percent level.

Third, dynamic range. The membrane and cathode tests reach the region around 2000 photoelectrons.

I will go through these quickly, because the combined picture is more important than any single plot.

## Slide 9 - SNR Result: Cold-Box Curves Clear Threshold

These are representative SNR curves from the cold-box tests.

The main thing to see is that the curves clear the threshold for the 1500 photoelectron setting.

For the review package, we still need to keep the details attached: module IDs, run conditions, and the exact SNR definition. But the physics message is straightforward: the signal quality is there.

## Slide 10 - SNR Result: All Modules Clear Greater Than 4

This slide summarizes the SNR result across the tested modules.

All the cases shown are above 4 at the operating point we care about.

So for signal quality, the mezzanine chain is not the limiting factor in these tests.

## Slide 11 - Pulse-Shape Evidence: Compensation Method

Now we move from signal-to-noise to pulse shape.

The issue was undershoot after the active differential-to-single-ended stage. Without compensation, the undershoot was about 30 percent.

That is too large for stable baseline recovery. The AFE compensation stage brings it under control.

For PRR, the important thing is to treat this as a documented setting: which module, which setting, and what residual undershoot.

## Slide 12 - Pulse-Shape Result: Undershoot Reduced To 0.23 Percent

Here is the compensated result.

The undershoot goes down to as low as 0.23 percent.

That is the number I would emphasize. It means the waveform recovers cleanly, and the downstream DAPHNE path sees a much better behaved signal.

## Slide 13 - Dynamic-Range Evidence: Measurement Method

The last mezzanine measurement is dynamic range.

For the March 2026 membrane cold-box run, we increased the LED intensity while DAPHNE was using high front-end attenuation.

The saturation point is taken from the goodness-of-fit curve. In practice, we compare the saturated plateau with the region where the fit starts to degrade, and use the crossing point.

That gives us a consistent way to quote the dynamic range.

## Slide 14 - Dynamic-Range Result: Membrane Near 2000 Photoelectrons

For the membrane measurements, both cases reach close to 2000 photoelectrons.

That is useful because these are cold-box results, not just ideal bench measurements.

Together with the SNR slides, this says the mezzanine path can keep good signal quality while still reaching the dynamic range we need.

## Slide 15 - Dynamic-Range Result: Cathode Reaches 2000 Photoelectrons

This is the cathode reference from the April 2024 cold-box measurement.

The cathode case also reaches about 2000 photoelectrons before saturation.

So the mezzanine section ends with a clear result: SNR is above threshold, the pulse-shape issue is corrected, and the target dynamic range is reached in the tested cases.

## Slide 16 - New-DAPHNE Gate: Common-Mode Noise

Now I want to shift to the main open hardware item for new DAPHNE.

In preliminary DAPHNE MEZZ tests, we saw significant common-mode noise, especially on the SoF and HD mezzanines.

The good news is that this is a defined problem. Milano-Bicocca and EIA University designed plug-in filters that reduce the DC/DC noise and suppress the 2 megahertz feature from the minus 5 volt charge pump.

The reduced filter is already part of the new board production. The next step is to test the produced board and confirm the noise performance in the integrated system.

## Slide 17 - New-DAPHNE Gate: Filter Suppression

These spectra show why the filter is a credible path.

The filter versions reduce the noise features we care about, including the DC/DC contribution and the minus 5 volt charge-pump feature.

I would still keep this as a yellow item. The filter data support the mitigation, and the new board is being produced; the remaining PRR evidence is the integrated-board validation.

## Slide 18 - DAQ/PRR Gate: Firmware Data Product

Now we connect the hardware to the data product.

DAQ needs a clear fragment boundary. That means the timestamp, channel identity, amplitude, timing, and descriptor validity all need to be defined.

There is also a resource question in the K26. Peak descriptors, x-correlation, and dead-time mitigation are useful, but they have to fit with enough margin.

So the goal here is a stable firmware output that DAQ can decode and review.

## Slide 19 - DAQ Integration Baseline

The basic DAQ path already exists.

DAPHNE Ethernet data taking has been established in DAQ. The next work is to freeze the fragment schema, keep the decoding in the DUNE-DAQ libraries, and preserve the path into HDF5, monitoring, and Waffles.

This is why DAQ integration belongs in the main DAPHNE story. It is part of making the system production-ready.

## Slide 20 - Calibration Moves Into DAQ Operations

Calibration needs the same treatment.

If calibration stays only in standalone board scripts, it is hard to repeat and hard to review.

The goal is to move selected calibration variables into `pds-run`. Then each scan point has run control, DAQ provenance, monitoring, and reproducible configuration.

That makes calibration an operations procedure, not only an expert workflow.

## Slide 21 - PRR Readiness: What Must Be Closed

This table is the PRR summary.

Mezzanine performance is green. The SNR, pulse-shape, and dynamic-range evidence are in hand. The remaining work is to package the evidence cleanly.

Noise mitigation is yellow. We have a filter solution, and the new board is being produced. The remaining step is to validate the integrated-board noise performance.

The firmware data product is yellow. The fields, rates, and fallback modes need to be frozen.

DAQ integration is green for the established Ethernet data-taking path, with schema and decoding freeze still to finish.

The red item is operations and trigger scope. We need owners, a schedule, and a clear boundary for what is inside the PRR scope.

## Slide 22 - Takeaway

Let me close with the main message.

The mezzanine evidence is strong. The new-DAPHNE noise issue has a clear mitigation path. And DAQ integration is now part of the production story.

The remaining work is specific: validate the integrated-board noise performance, freeze the firmware and DAQ data contract, make `pds-run` calibration repeatable, and assign ownership for the remaining trigger scope.

So the short version is this: DAPHNE is in good shape, but the last PRR items need to be closed as system-integration items, not as separate board tests.
