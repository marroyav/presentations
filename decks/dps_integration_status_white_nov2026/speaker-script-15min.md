# VD Detector Protection System — 15-minute speaking script

I&I meeting, November 2026

**About 15 minutes**, including pauses on the interlocks, group actions and work plan.
1,450 spoken words across slides 1–15. Timing cues are rehearsal targets.

Backups 16–53 are for questions.

## Slide 1 — VD Detector Protection System

**Target: 00:00–00:35**

We already have two useful starting points for the DPS: rack protection and the bottom-drift electronics. Today I want to show how we can build on them, and where we still need input from the consortia and LBNF.

The aim is to turn what we know into a full design that we can put on a test stand and check.

## Slide 2 — The hardware connection list is still growing

**Target: 00:35–01:10**

The biggest gap at the moment is the list of connections. We need every input, output and feedback signal that the DPS will use, together with the equipment at each end.

That information has to come from the people responsible for the equipment. Once we have it, we can see which parts of the BDE approach we can reuse and what we need to add.

## Slide 3 — DPS protects equipment; SC operates and records

**Target: 01:10–01:50**

The roles are fairly straightforward. DPS decides whether equipment is allowed to operate and acts when a protection condition is met. Slow controls lets us operate the equipment, see its state and keep the records. The consortia tell us the limits and how quickly we need to respond.

Protection takes priority over an operating request. Local interlocks can also act on their own, and personnel-safety alarms remain with SDSTA.

## Slide 4 — Facility interfaces may connect to SC or the DPS PLC

**Target: 01:50–02:25**

Here I’m grouping slow controls and the DPS together. The three systems above connect to that group. We haven’t decided whether each interface will go to slow controls, directly to the PLC, or to both.

The cryogenics link goes both ways. Inside the group, SC and DPS exchange through OPC UA. The lower links show how they reach the detector subsystems, power supplies and remote I/O.

## Slide 5 — Build the DPS brain on the BDE PLC architecture

**Target: 02:25–03:10**

Here’s why we’d like to use a PLC as the DPS brain. It gives us industrial off-the-shelf hardware and modular I/O, with an established route for expansion, maintenance and upgrades.

The BDE design already spreads its control and I/O panels along roughly seventy metres of mezzanine. We can build on that layout and add interfaces for other systems. The EtherCAT field network is separate from the supervisory Ethernet. The dashed part of the sketch shows the proposed extension.

## Slide 6 — Raritan PDU controls on dune-fd-test01

**Target: 03:10–04:05**

This is something we’d like to demonstrate to the collaboration using the Raritan PDU in our dune-fd-test01 setup. First, control one socket at a time and check its state and power. Second, use a compatible dry-contact actuator to send a fault or permit bit into the PLC, or another device.

We can also demonstrate the PDU’s own event rules and LuaPLC scripts: for example, a smoke/contact or threshold condition acting on selected outlets or a contact output, with delays and deliberate recovery. We still need to check the fitted accessory, firmware and PLC input before calling that demonstration complete.

## Slide 7 — FFDG BMS and SDSTA SCADA integration is progressing

**Target: 04:05–04:40**

We’re making progress with the FFDG BMS and SDSTA SCADA interfaces. For FFDG, the focus is monitoring and information for operator decisions; we are not assuming hard interlocks through that interface. The SDSTA work includes Oro Hondo ventilation status. We are still agreeing the signals to share.

## Slide 8 — Cryogenics presents one system to DUNE

**Target: 04:40–05:15**

Cryogenics keeps its own process controls in the CUC. For our purposes, we want one system interface to DUNE, even though there are several groups of controls behind it.

A state such as liquid-argon level can affect whether detector equipment is allowed to run. We need to agree what ready means for each load, which limits apply, and how the DPS should respond if a required signal disappears.

## Slide 9 — Trace each interlock from its source to the response

**Target: 05:15–05:50**

For each interlock, I’d like us to follow this chain all the way through. Start with the condition and where it comes from, identify the actual connection, then follow the decision and the action to the equipment’s response.

That gives us a useful way to review the design. We can see what hardware we already have, where a connection is missing, and which parts of the response we need to test.

## Slide 10 — Each group must identify its hardware connections

**Target: 05:50–06:25**

This is the information we’re asking each consortium and LBNF to provide. We need both ends of the connection, the connector or channel, what the signal means, and what action it should cause. We also need the expected feedback and the response if the signal is lost.

We’ll use one common register, with a contact and a source document for each entry, so we can work through the gaps together.

## Slide 11 — A trip removes the permit; recovery needs a new request

**Target: 06:25–07:00**

The basic behaviour I’m proposing is simple: allow operation when the request and the required conditions are valid. If something trips, remove the permit, keep the cause and check what the equipment did. Slow controls records the event.

Clearing the trip and turning the equipment back on are separate steps. We also need a clear rule for each load when an input is missing or no longer valid.

## Slide 12 — BDE is nearly complete; PDS has two decisions

**Target: 07:00–09:25**

BDE is nearly complete. The cooling path is our starting point: a fan fault inhibits the low-voltage channel feeding the affected crate. We still need to close the remaining checks, including whether the associated bias must also switch off and in what order. Nearly complete describes the current status; it does not claim that every installed protection path has passed its tests.

The two PDS items in red need a decision from the group. First, PDS needs to assess whether the purity-monitor flash lamp creates a protection need for the SiPMs. If it does, we need an inhibition rule and a way to confirm that the affected bias is off. If it only affects data quality, tagging the activity may be enough. PDS should make that assessment with the purity-monitor team in CalCI, and involve DAQ and slow controls in the resulting data or control interface. We should not assume the outcome.

Second, PDS needs to define the inhibition path for power over fibre. The backup drawing shows PDU switching and a possible box-enable input. Those are candidates. We need to know what actually stops the affected boxes, how quickly it acts, what feedback confirms the result, and how recovery works.

## Slide 13 — Agree the CalCI, HV and TDE protection interfaces

**Target: 09:25–11:40**

CalCI and PDS need to finish the laser handshake. The proposed rule blocks conflicting requests. The groups need to agree which request takes priority and what confirms emission off or the shutter closed before PDS returns. The laser's local personnel-safety interlocks remain independent.

The backups also contain important high-voltage dependencies. Low liquid-argon level can require the relevant drift-HV or top-CRP-bias supply to switch off; those are separate level conditions and must be mapped to their actual sensors and limits. Relief-valve and boiling-risk conditions also affect drift HV. When a cathode HV supply trips, the associated field-cage termination supplies must follow. HVS, Cryogenics and CalCI need to identify the signals, affected supplies and shutdown order.

For TDE, our current external protection route is through the rack PDUs. TDE and DPS need to define the conditions that require that action, the outlets involved, the allowed response time and the feedback. The microTCA crate's own power and cooling protection stays local.

These are the critical interfaces I want to bring to the groups. The detailed PDS low-voltage supply mapping, sensor paths and full matrix remain in the backups for discussion.

## Slide 14 — Use Batavia and SURF benches to test the protection paths

**Target: 11:40–13:20**

We need the two test benches to turn those decisions into working protection paths. In Batavia, Trevor reports that the initial BDE demonstrator design is complete and has been reviewed with the WIEC team at BNL. The next work is to apply that feedback, check the fan tachometer readout, and assemble and install the demonstrator.

At SURF, in the Nevada room, we already have dune-fd-test01, the PDU, smoke sensors, relay and GIZMo, plus Ignition, OPC UA bridges and emulators. We need to expand that setup along the Batavia model, adding the PLC, I/O and relevant subsystem interfaces.

Both benches should exercise the same full path: introduce the fault, observe the inhibit and confirm the equipment state. Measure response time and test lost communications, reset and re-enable. Slow controls should record the cause and the final state. These are tasks to perform; the slide does not report new test results.

## Slide 15 — Gather inputs by January; complete the design by April

**Target: 13:20–15:00**

The first target is to gather the information by late January 2027. Each consortium and LBNF should return its connections, limits and required actions, together with feedback, response times and the expected behaviour when a signal is lost. Each list needs a contact, confirmed coverage and a clear record of what is still missing.

The second target is a comprehensive DPS design by mid-April 2027. That should bring together the architecture, controller and I/O allocation, interfaces and protection rules. It also needs the fault response, shutdown order and recovery, plus drawings, parts, power needs and a test plan. Open choices should be recorded for review.

The two benches support that design work in parallel. Representative tests will help us check the proposed paths and find missing hardware or unsuitable interfaces while we can still change the design. The April target is for the comprehensive design. Hardware qualification and installation remain separate steps.

## Slide 16 — Backups — after the main talk

The detector walkthrough, full matrix and planning details are available for questions.

## Optional backup notes

### Slide 18 — The FFDG BMS connection needs an API licence

For FFDG, the route we’re discussing uses the Metasys API through Batavia. We still need to agree whether the data reaches SC, the DPS PLC or both. We’ve exercised the API and OPC UA publication with SBN building data. Live FD data still needs the licence.

Once access is available, we need to check the actual variables, their meaning and how often they update, before deciding how to use them.

### Slide 19 — How FFDG BSI status can support detector protection

The discussion with FFDG also gave us a practical limit. They described support on the next business day, without a twenty-four-hour service for us. For critical equipment protection, they recommended that we install our own sensors.

So we need to work out which information helps an operator make a decision, which could support an interlock, and where we need our own measurement.

### Slide 20 — The SDSTA SCADA interface needs a hardware survey

For SDSTA, we’re still doing the hardware survey. That includes finding the controllers, connections and network access at Ross Dry, and agreeing which signals could be made available.

Modbus TCP and OPC UA have both been discussed. The next step is to turn that discussion into named signals, with a known source and someone responsible for maintaining them.

### Slide 21 — SDSTA proposes a restricted SCADA status interface

The more specific proposal from SDSTA is a restricted Modbus TCP interface. They would expose a selected set of variables and keep control of their systems. The intention is for us to read status.

We still need to agree and check that restriction. We’re also waiting for the variable list, including Oro Hondo and HVAC information, and the details of how we recognise stale or missing data.

### Slide 22 — Detector

I’ll now go through the detector systems and show where those connections fit.

### Slide 23 — Ten BDE groups use the existing bottom-drift design

BDE gives us the most developed starting design here. The documented VD layout has ten groups, each with eight warm crates and two PL506 supplies. That’s eighty warm crates and twenty supplies in total.

We also have drawings, parts lists, power calculations and Ignition screens to work from. In this diagram, the EtherCAT exchange, the supply inhibits and the forty-eight-volt power feed are shown as separate connections.

### Slide 24 — Extend the BDE approach into a full DPS concept

The idea is to extend that PLC and remote-I/O approach wherever it fits the wider DPS. First we map the additional connections; then we work out the controller and I/O we need.

Slow controls would carry operating requests and keep the record of states and trips. For every protection function we add, we’d test the path from the fault appearing to the equipment reaching the intended state.

### Slide 25 — A cooling fault removes power from the affected crate

Here, the fan-status signal goes to the PLC. The cooling rule then inhibits the supply channel feeding the affected crate. We check the supply state and voltage, and slow controls records why the trip happened.

The dashed branch shows a possible shutdown of the associated bias. That part still needs agreement for VD: which bias channels are affected, and in what order they should be switched off.

### Slide 26 — SC and DAQ use distinct DAPHNE service paths

There are two routes to keep in mind for DAPHNE. Slow controls and the DAQ CCM and monitoring clients use the OPC UA bridge. Hermes has its separate IPBus and UDP configuration path.

The proposed SiPM-bias action would go from DPS through slow controls to DAPHNE, with status coming back and DAQ being informed. We still need to check the acknowledgement, the actual bias state and the time taken before relying on that action.

### Slide 27 — PDS must define the PoF inhibition path

For power over fibre, PDS still needs to define the inhibition path. The rack PDU and a possible box-enable connection are candidates. A local controller collects the box measurements.

Our working case is eighty boxes, each with four voltage readings and one temperature reading. That gives four hundred readings. Those values are gathered locally, so we still need to map the physical connections before counting central DPS inputs.

### Slide 28 — LV supplies power DAPHNE and PDS calibration boxes

Here we’re looking at the LV supplies for DAPHNE and the PDS calibration boxes. We’d control and read back the WIENER supplies over SNMP. The drawing separates DAPHNE’s forty-eight-volt supply from the calibration board and pulser feeds.

The working count is still thirty-four feeds. We need to map those feeds to loads, channels and inhibit groups, then agree the trip conditions and recovery. After a trip, we need to check the supply state, voltage and current.

### Slide 29 — Drift HV and bias supplies have separate inhibit paths

Drift HV and the CRP and field-cage bias supplies have their own wired inhibit interfaces, alongside normal control and monitoring. The documented bias scope is ten crates and five hundred and seventy-six channels.

Low liquid-argon level is one example of a drift-HV trip condition. For each rule, we need to identify the sensor, the inhibit connection and exactly which channels should respond.

### Slide 30 — Trace each protection input to a temperature sensor

For temperature, we need to know where the reading comes from and which limit applies before we can use it for protection. We also need to know how quickly to act and which equipment to switch off.

RTDs and fibre sensors use different readout systems. We need to follow the measurements through those systems to the particular protection rule they would support.

### Slide 31 — Proposed laser rules block conflicting PDS requests

For the four laser stations, our starting proposal is to block operating requests that conflict with PDS operation. Slow controls, DPS and the calibration interface would exchange the requests and status.

Before returning to the PDS operating state, we’d need confirmation that emission is off or the shutter is closed. The laser’s own safety interlocks remain independent. The exact excluded states and the affected equipment still need agreement.

### Slide 32 — The purity-monitor inhibit rule still needs agreement

This is one we still need to settle. Our current proposal is to keep taking data and tag the times when the purity-monitor flash lamp is active. The older PDS interface document requires the SiPM bias to be off during that activity.

We need PDS and the purity-monitor group to agree which rule applies. That decision tells us what operating sequence and what hardware or software action we need to provide.

### Slide 33 — Measure the full path from fault to confirmed shutdown

I want us to measure the time from a fault appearing to the equipment reaching its intended state. That includes the PLC decision, the output action and the feedback. Then we should repeat the tests for lost communications, reset and re-enable, and check the logs.

We can build that work into the Batavia demonstrator and the SD expansion. So far, we haven’t identified a critical function needing less than one millisecond. The consortium review and hardware tests need to check that assumption.

### Slide 49 — Use rack sensors and PDUs for shared protection

Where detector systems share a rack, they also share its protection hardware. We should count that package once and map the equipment to its PDU outlets. The PDU can act on its fitted sensors, while DPS supervises the agreed power actions and slow controls keeps the records.

Humidity monitoring still needs a separate requirement before it becomes a trip condition. For TDE, our current DPS scope is PDU control; crate-status and external-inhibit connections remain possible additions.
