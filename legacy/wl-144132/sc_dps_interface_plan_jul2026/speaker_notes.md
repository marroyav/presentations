# Speaker notes

## 1. From Interfaces to an Executable SC/DPS Plan

This is a coordination proposal, not a subsystem status review. The objective
is to make the existing work easier to integrate, schedule, and verify while
there is still time to change interface and infrastructure decisions.

## 2. This proposal connects existing work

Open by recognizing that the audience has already spent months or years on
these systems. The proposal is not to replace working code or revisit every
decision. The missing piece is a single, controlled representation of
cross-system behavior that survives across installation, integration,
commissioning, operation, and recovery.

The key sentence is: reuse the work and connect it into a versioned, executable
system contract.

## 3. Why move now?

The cost of an unresolved interface grows as it turns into procured equipment,
cabling, PLC logic, firmware assumptions, and underground procedures. Moving
fast means identifying and assigning the unknowns now. It does not mean
short-cutting safety or review.

## 4. A draft bench already exists

Explain the scope without selling the simulator as the detector. It represents
DAPHNE and WIB through their shared OPC-UA fleet-bridge implementation. PDU
telemetry remains on the SNMP path; power supplies retain SCPI or native
OPC-UA adapters; and sensor, permit, and alarm status comes through PLC/DPS or
native OPC-UA interfaces. These paths converge at the Ignition operator and
test view, not in the DAPHNE/WIB fleet bridge. DAQ continues to use the native
ZMQ/protobuf board-service interface. The evidence harness can time operations
and inject faults across both client surfaces.

The synthetic permit/alarm path is not a production DPS implementation, and no
production hard-interlock path should be inferred from the diagram.

## 5. Evidence must remain labelled

Separate what was actually run on the workstation from what was calculated
from source and from what still requires owners or hardware. This is central to
the credibility of the proposal. Zero observed simulator failures is useful
regression evidence; it is not a real-network reliability claim.

## 6. Monitoring is not the sizing workload

The OPC-UA snapshot is fast because it is a local software read. A
configuration campaign includes firmware waits, controller fan-out, queues,
timeouts, retries, prerequisites, and readback. The DAQ initialization and
configuration path is therefore the useful stress case.

The four-bridge, 48-leaf result is a planning point. Each shared DAPHNE/WIB
queue carries 47--48 DAPHNEs and 120 WIBs. Under the candidate active-leaf
budget, the DAPHNE fleet forms one projected 2.69 second wave while the WIB
fleet forms three projected 16.10 second waves, or 48.30 seconds. These are
source-derived no-failure floors, not hardware measurements, and the queue
model is not yet implemented by the current synchronous WIB bridge.

## 7. The proposal in one line

Pause here. This is the principal proposal:

Interface inputs lead to the interaction matrix. The matrix exposes the
dependency and hazard graph. Those dependencies become owned work packages and
acceptance tests. Only then can effort and staffing turn the work into dates.

The schedule is derived from the matrix, but the matrix alone does not estimate
labor.

## 8. What must be captured in the matrix?

The matrix is not simply a signal list. It must include authority, states,
interlocks, timing, failure behavior, recovery, ownership, and evidence.
Missing information should remain visible rather than being filled with an
integration-team assumption.

## 9. Stage and state both matter

Cryogenic state is important, but it is not the only axis. Partial
installation, commissioning authority, DAQ and timing state, power state,
network partitions, and maintenance bypasses can all change whether an action
is allowed. Each consortium must provide its normal-control and failure/protection
contract so that the integration team does not infer it.

## 10. One actor, two clients, independent protection

This is the software architecture rule that follows from sharing the same
physical control path. One target-side process owns hardware transactions.
DAQ and Slow Controls are clients of that process and may read cached status
in parallel. Writes are serialized and allowed only under an agreed state and
authority contract. The independent protection path may overtake software and
reports status back for diagnosis.

The unheaded lines are deliberately neutral about request and response
direction. Arrowheads are reserved for actual protection actions.

The DAQ operational-monitoring schema is a projection of selected status; it
must not become another independently evolving device protocol.

## 11. Example: power loss exposes a system requirement

Keep this conditional. Do not assert that the current design is unsafe. Ask:
if WIB power is not sustained, what mechanism guarantees the required ordering
with APA-bias removal? Ignition or a networked SC process may disappear during
the event, so any required guarantee must be owned by an independent path.

The important result is not the answer on this slide. It is that one matrix row
turns the question into owners, timing inputs, a design task, a proof test, and
a schedule dependency.

## 12. What must be managed---and where

The managed baseline includes requirements, schemas, firmware ABI, services,
DAQ and SC projections, PLC logic, deployment, rollback, and evidence.
Different systems remain authoritative for different information: EDMS for
approved interfaces, HWDB for installed topology, a secrets service for
credentials, and an artifact registry for built releases. The system release
pins the exact compatible set rather than assuming that each repository's
latest commit works with every other latest commit.

## 13. Make the repositories enforce the contract

The repository structure should be collaboration-owned and sustainable. Ask
the DAQ Git administrators for help defining protections, maintainers, required
reviews, releases, and evidence retention. The simulator should consume the
same schemas as the development packages and should test compatibility on
change.

Call this a formal interface-verification framework. Do not claim complete
formal proof until controlled properties and model-checking/proof evidence
exist.

## 14. Parallel lanes, explicit convergence gates

The diagram now groups the independent work into three swimlanes: board
services; clients plus protection; and test plus deployment. DAPHNE and WIB
hooks can proceed in Lane A while bridge/DAQ and rack-power/DPS work proceeds
in Lane B and the simulator, evidence, and infrastructure work proceeds in
Lane C. All lanes share one controlled baseline and must converge before
production writes or a system release: schema ownership, authority, state
constraints, physical protection timing, recovery, and the tested artifact
bill of materials are shared gates.

## 15. Begin with two vertical slices

The two pilots are deliberately complementary. The DAPHNE/WIB path exercises
device protocols, configuration fan-out, and DAQ orchestration. The rack-power
path exercises permits, interlocks, shutdown, alarms, and recovery. A crossing
fault proves that the framework can reason across subsystem boundaries.

## 16. A practical Vertical Slice Test platform

Two available Dell Precision 7680 workstations are suitable development nodes,
not a production server proposal. A managed switch is needed so traffic,
VLANs, counters, and mirroring can be controlled and measured. Representative
PLC/power/board hardware can be introduced gradually behind safe interfaces.

Ask for the actual SURF Ignition and network specifications. The production
architecture should come from measurements against those constraints.

## 17. Move quickly in the right order

The immediate actions are governance, named owners, one information template,
and matrix version zero. Do not wait for a perfect matrix: publish the unknowns
and use the pilots to close rows. Detailed dates follow staffing and estimates.

## 18. Decisions requested from this group

End with decisions, not a general request for feedback. Ask the group to agree
to create the collaboration-controlled SC/DPS Git group with DAQ Git-admin
support, and to define its owners, protections, CI, reviews, and release
policy. This is Gate 0, not repository housekeeping: it provides the versioned
place where firmware hooks, protobuf schemas, target services, DAQ packages,
SC/DPS bridges, the simulator, and their verification evidence can be
integrated without duplicating implementations.

Then ask the group to agree that the matrix drives the schedule, identify the
interface owners, approve the pilots, and provide the SURF/VST inputs. Explain
that credible labor and completion estimates depend on seeing those shared
development branches and their missing interfaces in the controlled system.

The first concrete outputs should be the shared Git group and matrix version
zero with sources, owners, open questions, and evidence routes.

## Appendix slides

Use the appendices only if the discussion needs the quantitative evidence,
terminology around Gateway/bridge/leaf/host, a concrete starter matrix row, or
the comparison between the March WIB/Quasar spin test and the local fleet bench.

For the comparison slide, correct the shorthand first: Quasar is the
ZMQ-to-OPC-UA bridge, not the simulator. The March test used Python WIB
emulators, Quasar bridge processes, and a much larger Ignition tag model. Its
480-WIB measurements attribute 21.7 GB to the emulator host, 3.23 GB to
Quasar, and 55.6 GB to Ignition. The 1,000-WIB project contained about
5.5 million Ignition tags, most of which were alarms, interlocks, or other
derived tags rather than OPC tags.

The local bench uses in-process logical devices on a shared asynchronous
runtime and publishes 40,755 OPC-UA variables across the full 1,818-object
fleet. Its smaller footprint demonstrates an efficient implementation, but it
does not yet establish a Quasar-versus-local-bridge result because the tag
definitions, scan classes, clients, historian load, and runtime shapes differ.
Use the proposed A/B protocol to explain how the two approaches can be compared
fairly.
