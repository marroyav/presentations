# VD Detector Protection System — 15-minute speaking script

I&I meeting, November 2026

**About 15 minutes**, with short pauses for diagrams and slide changes.  
1,710 spoken words across slides 1–25. The times are rehearsal cues.

Backups 26–46 are for questions.

## Slide 1 — VD Detector Protection System

**Target: 00:00–00:30**

We already have two useful starting points for the DPS: rack protection and the bottom-drift electronics. Today I want to show how we can build on them, and where we still need input from the consortia and LBNF.

The aim is to turn what we know into a full design that we can put on a test stand and check.

## Slide 2 — The hardware connection list is still growing

**Target: 00:30–01:05**

The biggest gap at the moment is the list of connections. We need every input, output and feedback signal that the DPS will use, together with the equipment at each end.

That information has to come from the people responsible for the equipment. Once we have it, we can see which parts of the BDE approach we can reuse and what we need to add.

## Slide 3 — DPS protects equipment; SC operates and records

**Target: 01:05–01:40**

The roles are fairly straightforward. DPS decides whether equipment is allowed to operate and acts when a protection condition is met. Slow controls lets us operate the equipment, see its state and keep the records. The consortia tell us the limits and how quickly we need to respond.

Protection takes priority over an operating request. Local interlocks can also act on their own, and personnel-safety alarms remain with SDSTA.

## Slide 4 — Facility interfaces may connect to SC or the DPS PLC

**Target: 01:40–02:20**

Here I’m grouping slow controls and the DPS together. The three systems above connect to that group. We haven’t decided whether each interface will go to slow controls, directly to the PLC, or to both.

The cryogenics link goes both ways. Inside the group, SC and DPS exchange through OPC UA. The lower links show how they reach the detector subsystems, power supplies and remote I/O.

## Slide 5 — Build the DPS brain on the BDE PLC architecture

**Target: 02:20–03:00**

Here’s why we’d like to use a PLC as the DPS brain. It gives us industrial off-the-shelf hardware and modular I/O, with an established route for expansion, maintenance and upgrades.

The BDE design already spreads its control and I/O panels along roughly seventy metres of mezzanine. We can build on that layout and add interfaces for other systems. The EtherCAT field network is separate from the supervisory Ethernet. The dashed part of the sketch shows the proposed extension.

## Slide 6 — Cryogenics presents one system to DUNE

**Target: 03:00–03:35**

Cryogenics keeps its own process controls in the CUC. For our purposes, we want one system interface to DUNE, even though there are several groups of controls behind it.

A state such as liquid-argon level can affect whether detector equipment is allowed to run. We need to agree what ready means for each load, which limits apply, and how the DPS should respond if a required signal disappears.

## Slide 7 — Trace each interlock from its source to the response

**Target: 03:35–04:15**

For each interlock, I’d like us to follow this chain all the way through. Start with the condition and where it comes from, identify the actual connection, then follow the decision and the action to the equipment’s response.

That gives us a useful way to review the design. We can see what hardware we already have, where a connection is missing, and which parts of the response we need to test.

## Slide 8 — Each group must identify its hardware connections

**Target: 04:15–04:50**

This is the information we’re asking each consortium and LBNF to provide. We need both ends of the connection, the connector or channel, what the signal means, and what action it should cause. We also need the expected feedback and the response if the signal is lost.

We’ll use one common register, with a contact and a source document for each entry, so we can work through the gaps together.

## Slide 9 — A trip removes the permit; recovery needs a new request

**Target: 04:50–05:25**

The basic behaviour I’m proposing is simple: allow operation when the request and the required conditions are valid. If something trips, remove the permit, keep the cause and check what the equipment did. Slow controls records the event.

Clearing the trip and turning the equipment back on are separate steps. We also need a clear rule for each load when an input is missing or no longer valid.

## Slide 10 — Build on the Batavia and SD DPS test setups

**Target: 05:25–06:15**

We’re building up the test capability in both Batavia and SD. Trevor’s slides say the initial BDE demonstrator design is complete and has been reviewed with the WIEC team at BNL. His next steps are to apply that feedback, test the fan tachometer reading, then assemble and install the demonstrator.

In the Nevada room, we already have dune-fd-test01, the PDU, smoke sensors, relay and GIZMo, plus Ignition, OPC UA bridges and emulators. We’d like to expand that setup along the Batavia model and use it to work through trips, feedback and recovery.

## Slide 11 — Detector

**Target: 06:15–06:20**

I’ll now go through the detector systems and show where those connections fit.

## Slide 12 — Ten BDE groups use the existing bottom-drift design

**Target: 06:20–06:55**

BDE gives us the most developed starting design here. The documented VD layout has ten groups, each with eight warm crates and two PL506 supplies. That’s eighty warm crates and twenty supplies in total.

We also have drawings, parts lists, power calculations and Ignition screens to work from. In this diagram, the EtherCAT exchange, the supply inhibits and the forty-eight-volt power feed are shown as separate connections.

## Slide 13 — Extend the BDE approach into a full DPS concept

**Target: 06:55–07:35**

The idea is to extend that PLC and remote-I/O approach wherever it fits the wider DPS. First we map the additional connections; then we work out the controller and I/O we need.

Slow controls would carry operating requests and keep the record of states and trips. For every protection function we add, we’d test the path from the fault appearing to the equipment reaching the intended state.

## Slide 14 — A cooling fault removes power from the affected crate

**Target: 07:35–08:10**

Here, the fan-status signal goes to the PLC. The cooling rule then inhibits the supply channel feeding the affected crate. We check the supply state and voltage, and slow controls records why the trip happened.

The dashed branch shows a possible shutdown of the associated bias. That part still needs agreement for VD: which bias channels are affected, and in what order they should be switched off.

## Slide 15 — SC and DAQ use distinct DAPHNE service paths

**Target: 08:10–08:45**

There are two routes to keep in mind for DAPHNE. Slow controls and the DAQ CCM and monitoring clients use the OPC UA bridge. Hermes has its separate IPBus and UDP configuration path.

The proposed SiPM-bias action would go from DPS through slow controls to DAPHNE, with status coming back and DAQ being informed. We still need to check the acknowledgement, the actual bias state and the time taken before relying on that action.

## Slide 16 — DPS switches PoF power through the PDU

**Target: 08:45–09:25**

For power over fibre, the proposed way to remove power is through the rack PDU. A local controller collects the box measurements. A separate box-enable connection is another option to investigate.

Our working case is eighty boxes, each with four voltage readings and one temperature reading. That gives four hundred readings. Those values are gathered locally, so we still need to map the physical connections before counting central DPS inputs.

## Slide 17 — LV supplies power DAPHNE and PDS calibration boxes

**Target: 09:25–10:05**

Here we’re looking at the LV supplies for DAPHNE and the PDS calibration boxes. We’d control and read back the WIENER supplies over SNMP. The drawing separates DAPHNE’s forty-eight-volt supply from the calibration board and pulser feeds.

The working count is still thirty-four feeds. We need to map those feeds to loads, channels and inhibit groups, then agree the trip conditions and recovery. After a trip, we need to check the supply state, voltage and current.

## Slide 18 — Drift HV and bias supplies have separate inhibit paths

**Target: 10:05–10:35**

Drift HV and the CRP and field-cage bias supplies have their own wired inhibit interfaces, alongside normal control and monitoring. The documented bias scope is ten crates and five hundred and seventy-six channels.

Low liquid-argon level is one example of a drift-HV trip condition. For each rule, we need to identify the sensor, the inhibit connection and exactly which channels should respond.

## Slide 19 — Trace each protection input to a temperature sensor

**Target: 10:35–11:10**

For temperature, we need to know where the reading comes from and which limit applies before we can use it for protection. We also need to know how quickly to act and which equipment to switch off.

RTDs and fibre sensors use different readout systems. We need to follow the measurements through those systems to the particular protection rule they would support.

## Slide 20 — Proposed laser rules block conflicting PDS requests

**Target: 11:10–11:45**

For the four laser stations, our starting proposal is to block operating requests that conflict with PDS operation. Slow controls, DPS and the calibration interface would exchange the requests and status.

Before returning to the PDS operating state, we’d need confirmation that emission is off or the shutter is closed. The laser’s own safety interlocks remain independent. The exact excluded states and the affected equipment still need agreement.

## Slide 21 — The purity-monitor inhibit rule still needs agreement

**Target: 11:45–12:20**

This is one we still need to settle. Our current proposal is to keep taking data and tag the times when the purity-monitor flash lamp is active. The older PDS interface document requires the SiPM bias to be off during that activity.

We need PDS and the purity-monitor group to agree which rule applies. That decision tells us what operating sequence and what hardware or software action we need to provide.

## Slide 22 — Use rack sensors and PDUs for shared protection

**Target: 12:20–13:00**

Where detector systems share a rack, they also share its protection hardware. We should count that package once and map the equipment to its PDU outlets. The PDU can act on its fitted sensors, while DPS supervises the agreed power actions and slow controls keeps the records.

Humidity monitoring still needs a separate requirement before it becomes a trip condition. For TDE, our current DPS scope is PDU control; crate-status and external-inhibit connections remain possible additions.

## Slide 23 — Measure the full path from fault to confirmed shutdown

**Target: 13:00–13:45**

I want us to measure the time from a fault appearing to the equipment reaching its intended state. That includes the PLC decision, the output action and the feedback. Then we should repeat the tests for lost communications, reset and re-enable, and check the logs.

We can build that work into the Batavia demonstrator and the SD expansion. So far, we haven’t identified a critical function needing less than one millisecond. The consortium review and hardware tests need to check that assumption.

## Slide 24 — Collect the inputs, then review the full DPS concept

**Target: 13:45–14:20**

The next steps come in two parts. First, complete the connection lists with the consortia and LBNF, confirm what they cover, and give the remaining gaps a contact. Then review the full concept: the architecture, controller and I/O, interfaces, fault response and test plan.

The dates are still open. We’ll agree them with the contributors once we know the scope and the resources available.

## Slide 25 — Prepare the hardware review

**Target: 14:20–15:00**

For the hardware review, we should be able to show what we can reuse, what we need to add, how it connects, and what the tests tell us. That gives us the basis for the drawings, space and power needs, parts and costs.

What I need from this meeting is a contact for each contributing group and control-engineering support. With those in place, we can complete the connection register and bring a full DPS concept back for review.

## Slide 26 — Backups — after the main talk

I’ll stop here. The remaining slides are available if we need them for questions.

## Facility details — optional backup notes

Use these only if the corresponding questions come up.

### Slide 28 — The FFDG BMS connection needs an API licence

For FFDG, the route we’re discussing uses the Metasys API through Batavia and then into DUNE slow controls. We’ve exercised the API and OPC UA publication with SBN building data. Live FD data still needs the licence.

Once access is available, we need to check the actual variables, their meaning and how often they update, before deciding how to use them.

### Slide 29 — How FFDG BSI status can support detector protection

The discussion with FFDG also gave us a practical limit. They described support on the next business day, without a twenty-four-hour service for us. For critical equipment protection, they recommended that we install our own sensors.

So we need to work out which information helps an operator make a decision, which could support an interlock, and where we need our own measurement.

### Slide 30 — The SDSTA SCADA interface needs a hardware survey

For SDSTA, we’re still doing the hardware survey. That includes finding the controllers, connections and network access at Ross Dry, and agreeing which signals could be made available.

Modbus TCP and OPC UA have both been discussed. The next step is to turn that discussion into named signals, with a known source and someone responsible for maintaining them.

### Slide 31 — SDSTA proposes a restricted SCADA status interface

The more specific proposal from SDSTA is a restricted Modbus TCP interface. They would expose a selected set of variables and keep control of their systems. The intention is for us to read status.

We still need to agree and check that restriction. We’re also waiting for the variable list, including Oro Hondo and HVAC information, and the details of how we recognise stale or missing data.
