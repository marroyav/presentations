# Grouped256 production campaign — 2026-09-16

Goal active; no board deployment authorized. Candidate committed in isolated
`daphne-firmware-256-5-production` worktree, branch
`codex/selftrigger-256-5-production`: current candidate
`e49c4aae562c7f13c4922098358179b293b8b3e5` (includes baseline
`7d0ea761248882a6781cd1e07df24788c98b6b02`).
Canonical dirty repositories preserved.

Implemented 256 samples, 64 pretrigger, five fixed compact descriptors,
63 words/504 bytes, packet format 4 separate from control ABI2. Continuation
retains the 447-tick posttrigger deadline with third accepted-frame history.
Gapless mux enabled only for grouped target; legacy default preserved.
Hermes packet reservation configured for63 words/512 FIFO. Dual-profile
packaging/identity checks preserve older full-stream ABI2 without reading new
packet-format MMIO. Build phase timing instrumentation added; no measured
synthesis speedup claimed.

Local evidence: 31 formal checks passed including gapless induction; full
logic suite reaches successful composable-top smoke completion. All five final
grouped replay modes passed with identical RTL manifests:30,428 grouped
packets,15,537,664 samples and303,470 descriptor words checked. Exact runs:
`/tmp/frame256-final-mode0`, `/tmp/frame256-frozen-mode1`, `mode2`, `mode3`,
`/tmp/frame256-final-mode4`. Legacy and new descriptor/continuation contracts
passed; agent reports37 PetaLinux tests passed. Register-map checker and diff
check passed immediately before commit. Formal/logic logs copied to evidence.

Candidate bundle `/tmp/daphne256-production-candidate1.bundle`, SHA256
`5a4d34db80b123ab1895806b992f10c87013061c12f6bc4f093367aa0d9147f8`.
Cooper preflight17:35UTC: no Vivado/XSim,23GiB available,612GiB free.
Launch confirmed, transfer session7614 exit0. Unique run
`/tmp/arroyave/work/dsc256-7d0ea761-20260916`, tmux
`daphne-256-7d0ea761`. Runner gates legacy+gapless real XPM FIFO, grouped
vendor tests, then clean synthesis/implementation/package. Inspect live handle
and campaign status before any restart. Four threads, one heavy build.
At17:36UTC both legacy and gapless Hermes vendor simulations PASS. Gapless
checked64 packets,63 words,reset during packet,stalled sink,backpressure and
contiguous boundaries with real XPM models. Stage advanced to vendor-grouped;
live XSim process observed. At17:40UTC grouped32_mode0 XSim PID1759307 live;
preceding vendor contracts passed. No restart required.

Followup commit `3e35e708` adds qualification-report extraction, phase-timing
unit test, test-fixture repair and cleanup record; no production RTL changes.
The DT fixture lacked uart0/uart1 labels; added stub nodes, full46 tests PASS
(evidence/petalinux-46-tests.log). Phase instrumentation unit test PASS on
Cooper against immutable candidate Tcl (local tclsh unavailable).
New qualification script must run on routed DCP after build; not yet executed.

Next: confirm launch, resolve vendor failures with new immutable revision/run
(never edit running source), qualify timing/CDC/DRC/resources and artifacts.
Measure synthesis turnaround alternatives after first baseline. Cleanup
cleanup complete for11 validated generated directories:76MiB local FuseSoC
plus12.7MiB Cooper XPM/XSim. Recursive asset scans clean, all targets absent,
reports/releases retained. Petalinux tmp trees deliberately not removed.
All agents finished; no pending edits. Goal remains incomplete: routed build,
report qualification, synthesis improvement/comparison and final packages.

At17:42:05UTC grouped vendor regressions PASS; runner advanced to implementation,
Vivado started17:42:13UTC, preflight stage. Local HEAD1807b3dd adds isolated
synth benchmark helper/docs only;
Cooper source remains7d0ea761. Compare RuntimeOptimized after baseline, same
source/tool/host/4threads, no cache/RTL changes; full routed QoR must qualify
any faster option. Historical near-full placement is a risk, not current evidence.
Full five-mode local replay archived in evidence/final-five-mode-replay.tar.gz,
SHA2567eb325ca7dd9b16b4b48d884a818915203303dba8f91a632311927c7b1d40f24.

17:45:13UTC authoritative live status: native build Vivado PID1765169
(preflight PID1762312 completed and flow advanced), synthesis started
PerformanceOptimized; device synthesis license acquired. IP generation warns
xxv_ethernet_0 locked for optional license checks despite PCS/PMA configuration;
existing flow generates its HDL before packaging (daphne_ip_gen.tcl436).
Do not call this a blocker absent failure; inspect synthesized black boxes and
final artifact gates. Process105%CPU/RSS1.65GiB, no exit-code file yet.
Current turn is a verified wait/progress observation, not a stalled build.

Follow-up monitoring: synthesis phase closed in17m16s (Tcl elapsed1036112ms),
tcl status0. Post-synth resource report: LUT101585/117120 (86.74%), registers
91207/234240(38.94%), BRAM91/144(63.19%), URAM32/64(50%), DSP832/1248
(66.67%). For clock_raw_s_1 post-synth setup WNS+1.069ns/TNS0, hold WHS
-0.066ns/THS-147.890ns with4095 failing endpoints; estimated synthesis data,
not final hold result. Four 10Gb links instantiated and GT locations reported.
Synthesis completed0 errors/0 critical warnings/2578 warnings. A second
design-synth flow report says0 errors,104 critical warnings,665 warnings;
resolve sources before release claim. Place warning: IOB constraint on
unconnected QSPI IO0 register. Clock warning: manual user clock suppresses
auto derivation at PDTS MMCM CLKOUT0. Capture and inspect methodology, clock,
exception and routed DRC reports. Build phase timing log currently records
prepare2894ms, generate_ip105087ms, synthesis1036112ms. Implementing now; at
18:19:45UTC synthesis TSV holds prepare2.894s, IP generation105.087s and
synthesis1036.112s, each Tcl status0. Placement and post-place phys-opt also
completed successfully; post-place DCP written (~180MiB). Provisional placer
WNS moved from -0.164 to +0.104ns. Vivado is extracting post-place methodology,
timing and clock reports before routing. PID1765169 remains active at36:25
elapsed,59:29 CPU,8.35GiB RSS. Source immutable. Local copies of post-synth
reports and timing manifest plus SHA file are in evidence/.

Monitoring update (2026-09-16 13:58 UTC): Cooper implementation/package flow
finished with exit0; checksummed bit/bin/XSA/DTBO/overlay artifacts and routed
DCP were produced. Full routed timing summary reports setup WNS+0.126ns,
TNS0, no failing setup endpoints; hold WHS+0.011ns, THS0, no failing hold
endpoints. This only covers constrained paths. Independent detailed report
extraction completed cleanly (`exit-code.txt`=0) from the immutable post-route
DCP; preserved with SHA256 manifest under
`evidence/routed-qualification-7d0ea761/`. The methodology report finds eight
TIMING-7 critical warnings: the four RX/TX clock pairs (both directions) are
timed related despite having no common node. Review suggests these recovered
GT clocks should be asynchronous, but any clock-group correction must be
validated in a new immutable full implementation, not retroactively applied.
It also reports 60 TIMING-18 checks: missing external timing bounds on nine
inputs and 51 outputs (AFE serial controls/data, PMBus/I2C/reset/fan/timing,
trim and offset controls). Existing manifest intentionally defers AFE capture
input delays pending board/serializer skew measurements. Do not add guessed
zero delays or broad false paths; obtain defensible interface timing bounds.
The detailed CDC report is large and flags CDC-1/10/11/12/13/14 critical
classes, including IDELAY control, GT/FIFO and vendor structures; classify
them by endpoint and intended CDC contract before calling them defects or
waiving them. Post-route DRC has no reported errors; 842 warnings include 832
DSP input-pipelining advisories plus IO/RAM/no-load checks. Timing/CDC/DRC
review is therefore still open and this is not a production release.

Clock-group hypothesis test (same frozen routed DCP; no RTL changes and no
reroute): the candidate Hermes Tcl now resolves exactly one RX/TX clock per
lane and applies four pairwise asynchronous groups. Vivado accepted the
constraints. Methodology TIMING-7 fell from eight critical warnings to zero;
all four lane pairs are explicitly reported as asynchronous, while cross-lane
relations remain unchanged. Setup/hold summary is numerically unchanged
(WNS+0.126ns, WHS+0.011ns; zero failing setup/hold endpoints). Trial reports,
Tcl inputs, console log and checksums are archived under
`evidence/rx-tx-clockgroup-review-7d0ea761/`. This is useful evidence for the
constraint model only, not a replacement routed result. Next create a new
immutable source revision, rerun applicable regression/vendor formal tests and
a complete Cooper implementation before promoting that change. The main open
qualification issues remain CDC classifications and defensible external I/O
delay bounds (nine inputs and 51 outputs), plus the existing timing/constraint
methodology warnings.

New immutable revision `e49c4aae562c7f13c4922098358179b293b8b3e5` adds only
lane-local recovered RX/TX asynchronous timing groups, checks exact one-clock
resolution per lane, and parameterizes checkpoint qualification to test an
extra constraint hypothesis. The constraint contract test passes. Bundle
`/tmp/daphne256-production-e49c4aae.bundle`, SHA256
`f510eadbe790d0bb53170752a921f57f9d72db8bec4dc2e7373f25ccecbd2ed9`, is
cloned on Cooper at `/tmp/arroyave/work/dsc256-e49c4aae-20260916` and running
in tmux session `daphne-256-e49c4aae`. Launch preflight had no heavy Vivado
jobs,23GiB available RAM and611GiB free disk. At19:15UTC the runner was in
`vendor-hermes` with xelab compiling; monitor `campaign.stage`, exit code,
vendor logs and Vivado/XSim processes before considering any restart. This
re-run is required to qualify the committed constraints against the complete
build flow. The Hermes gate passed on this revision: legacy and gapless
admission simulations PASS (64 packets,63 words,reset while transmitting,
stalled sink and gapless boundaries). At19:19UTC the runner had advanced to
vendor-grouped simulation (`frame256_late447` active); no campaign exit code
yet.

Correction/follow-up: vendor-grouped then passed successfully: mode0 produced
6752/6752 byte-identical grouped/reference packets, with 3,457,024 samples and
67,520 descriptor words checked; zero unmatched packets (summary
`vendor-grouped/summary.json`, CSV SHA256
`26e254d3755dac5c237042ec78dda6ce557f91a1d3b013e5346dc0c5c33b1b45`). The
campaign advanced to implementation and clean Vivado synthesis started at
19:22UTC. At19:25UTC it remained active in synthesis at ~6m elapsed, ~6.9GB
RSS, with14GiB memory available; no build exit code yet. One intentional
synthesis note says the IPbus transport TX RAM uses BRAM rather than URAM
because zero pipeline stages are available; inspect resource mapping in final
utilization reports.

Initial CDC triage of the full report shows this is not merely report noise:
of 19,659 CDC-1 rows, 18,817 repeat one analog-control `signal_delay` register
feeding grouped record-builder logic across the clock_pl_0/frontend_clock
domain; 448 involve FE-AXI `iserdes_bitslip` controls reaching capture output
registers; 394 are self-trigger register-bank crossings to grouped datapath.
These may rely on software/configuration quiescence, but that contract is not
proved by the CDC report and must be verified in RTL/control sequencing before
waiving. Other CDC-10/11/12/13/14 flags remain to be traced. Do not conflate
the lane-local RX/TX timing fix with resolution of these independent CDCs.
At19:33UTC in the e49 build, the grouped fabric top synth completed successfully
with0 errors,0 critical warnings,2672 warnings; the separate IP synthesis
summary continues to report104 critical warnings, so the same warning-source
triage requirement remains. The new `hermes_control_cdc.tcl` loaded through
the real managed build flow and finished sourcing without a lane-count error.
Post-synth power/timing extraction is active; full implementation has not yet
started. At19:35UTC phase TSV reported prepare2.903s, generateIP105.381s,
synthesis1032.233s, all status0 and PerformanceOptimized/four threads. Placement
is now in Global Place Phase1. Peak parent RSS~8.5GiB and system has~16GiB
available. Do not benchmark another Vivado directive until this implementation
releases the host. Post-place checkpoint is now written (~189MB) and the
methodology report confirms TIMING-7 is gone with the real managed constraint
flow. It still has TIMING-18 missing delay checks on9 inputs/51 outputs, 17
large hold checks in the timing-endpoint recovered-clock crossing, and existing
TIMING-9/TIMING-24/TIMING-30 warnings. The worst early hold finding is about
-2.36ns; this stage can improve during route, so judge final hold only from the
routed checkpoint. Do not paper over the board-I/O timing gap.

Final e49c4aae monitoring result: Cooper campaign exited0 and produced the
candidate bit/bin/XSA/DTBO/overlay package. Final independent checkpoint
qualification also exited0; all reports and SHA256 manifest are archived at
`evidence/final-qualification-e49c4aae/`. Routed timing is positive but very
tight: setup WNS+0.011ns/TNS0, hold WHS+0.010ns/THS0, no failing endpoints.
The lane-local TIMING-7 warnings are gone. Qualification remains open: 60
TIMING-18 external-delay omissions (9 inputs/51 outputs), TIMING-9/24/30 and
other methodology findings, plus CDC classes requiring endpoint-level
classification (CDC-1 19,659; CDC-3 243; CDC-6 8; CDC-9 13; CDC-10 35;
CDC-11 12; CDC-12 3; CDC-13 65,875; CDC-14 32; CDC-15 14,608). Do not call
this production-qualified or program hardware until these have an accepted
disposition and board-level timing constraints are defensible. Candidate
release files and verified local hashes are in
`releases/daphne-selftrigger-e49c4aae/`; no hardware was programmed.

The same-source PerformanceOptimized Cooper synth phase took1,032,233ms
(17m12s) on four threads; full implementation/package and the real vendor
regressions passed. This is essentially the same as the earlier baseline
1,036,112ms, so no synthesis-time improvement is demonstrated. A paired
RuntimeOptimized synth-only comparison remains desirable, but the Cooper SSH
endpoint timed out during the latest monitor check; do not start a benchmark
until connectivity and idle vendor-process status can be verified. Current
local source worktree is clean at e49c4aae; bundle and release evidence are
preserved locally. A fresh SSH retry after a 20-second pause still timed out
on Cooper port22; remote process status is therefore unknown, not assumed
idle. Local candidate artifact hashes and the final independent qualification
report manifest were rechecked successfully.
