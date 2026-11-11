# VD Detector Protection System — 15-minute speaking script

I&I meeting, November 2026

**About 15 minutes**, including short pauses to explain the matrix and delivery checks.  
1,640 spoken words across slides 1–15. Timing cues are rehearsal targets.

Backups 16–50 are for questions.

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

## Slide 7 — Cryogenics presents one system to DUNE

**Target: 04:05–04:45**

Cryogenics keeps its own process controls in the CUC. For our purposes, we want one system interface to DUNE, even though there are several groups of controls behind it.

A state such as liquid-argon level can affect whether detector equipment is allowed to run. We need to agree what ready means for each load, which limits apply, and how the DPS should respond if a required signal disappears.

## Slide 8 — Trace each interlock from its source to the response

**Target: 04:45–05:25**

For each interlock, I’d like us to follow this chain all the way through. Start with the condition and where it comes from, identify the actual connection, then follow the decision and the action to the equipment’s response.

That gives us a useful way to review the design. We can see what hardware we already have, where a connection is missing, and which parts of the response we need to test.

## Slide 9 — Each group must identify its hardware connections

**Target: 05:25–06:05**

This is the information we’re asking each consortium and LBNF to provide. We need both ends of the connection, the connector or channel, what the signal means, and what action it should cause. We also need the expected feedback and the response if the signal is lost.

We’ll use one common register, with a contact and a source document for each entry, so we can work through the gaps together.

## Slide 10 — A trip removes the permit; recovery needs a new request

**Target: 06:05–06:40**

The basic behaviour I’m proposing is simple: allow operation when the request and the required conditions are valid. If something trips, remove the permit, keep the cause and check what the equipment did. Slow controls records the event.

Clearing the trip and turning the equipment back on are separate steps. We also need a clear rule for each load when an input is missing or no longer valid.

## Slide 11 — Build on the Batavia and SD DPS test setups

**Target: 06:40–07:30**

We’re building up the test capability in both Batavia and SD. Trevor’s slides say the initial BDE demonstrator design is complete and has been reviewed with the WIEC team at BNL. His next steps are to apply that feedback, test the fan tachometer reading, then assemble and install the demonstrator.

In the Nevada room, we already have dune-fd-test01, the PDU, smoke sensors, relay and GIZMo, plus Ignition, OPC UA bridges and emulators. We’d like to expand that setup along the Batavia model and use it to work through trips, feedback and recovery.

## Slide 12 — Use the interlock matrix to track each protection function

**Target: 07:30–10:25**

This is the interlock matrix we put together earlier. It has forty-six rules, and I’ve selected a few rows here so we can read it together. Each row starts with a condition and shows which systems act. The last column tells us what kind of source supports that entry.

For example, the low-level and rack-smoke rows come from released sources. The fan-cooling row is still marked as an inference. For the purity-monitor lamp, the response is explicitly unresolved. Those labels matter: finding a requirement in a document doesn’t tell us that the wiring is mapped, the owners have agreed the function, or the hardware has passed a test.

This is where I’d like us to record the work as it comes in. For each row, we need the source, the physical input, the controller and output, the equipment response, the timing requirement and a contact. A function can need several connections, so the number of rules is different from the number of wires or I/O channels. The full matrix is available in the backups and the companion document.

Take the BDE fan row as an example. We’d ask the BDE team to identify the fault definition, the signal that tells us about it, the WIEC concerned and the supply channel to inhibit. We’d also need the allowed response time and the feedback that confirms power is off. The matrix entry then links those details to the hardware register and the test case.

The purity-monitor row shows why we need to keep unresolved decisions visible. Until PDS and the purity-monitor group agree the rule, we should record the conflict and the people needed to resolve it. That row gives us a specific review task.

Several functions may use the same sensor, controller or output. We should reference that shared equipment consistently and count it once in the inventory. The matrix describes what must happen; the connection register tells us exactly how we would make it happen.

## Slide 13 — Measure milestones with completed records and evidence

**Target: 10:25–13:40**

To measure delivery, we need to agree what complete means and which records are in scope. For the information-collection milestone, I’d count complete connection records against the required inventory for each consortium and LBNF. Complete means that we know both endpoints, the signal, the action, the feedback, the timing, the source and the contact. Each group also needs to confirm that its list covers its equipment.

For the conceptual-design milestone, the unit is a protection function. We should be able to follow each in-scope function through the proposed hardware and logic, identify the I/O we need, and show the review of failure behaviour and recovery. Remaining decisions should be visible, with a contact and a way to resolve them. The concept also needs a test plan.

Hardware evidence is a separate step. That’s where we report the test cases passed, the actual fault-to-equipment response time against the agreed budget, and the results for communications loss, reset and recovery. I don’t want us to count a reviewed diagram as a passed hardware test. We still need agreement on the scope and the reviewers, and the dates remain open.

For progress reporting, I’d show the position for each contributing group, the records completed since the previous review, and the gaps still blocking coverage. We need to agree the denominator before quoting a percentage. A partial list can look complete if we haven’t checked which equipment and operating conditions it is supposed to cover.

The review should leave a record: the source revision, the person who checked it, the result, and the remaining decisions. For the concept, we should be able to hand someone the matrix, interface and I/O allocation, proposed fault behaviour and test plan, and have them follow a function without relying on this presentation.

For a hardware test, the evidence needs to show the input condition, the output action and the resulting equipment state. We measure the delay across that whole path and compare it with the response requirement agreed for the function. A successful command is one piece of that record; we also need the equipment feedback and the results when communications are lost or the system restarts.

## Slide 14 — Collect the inputs, then review the full DPS concept

**Target: 13:40–14:15**

The next steps come in two parts. First, complete the connection lists with the consortia and LBNF, confirm what they cover, and give the remaining gaps a contact. Then review the full concept: the architecture, controller and I/O, interfaces, fault response and test plan.

The dates are still open. We’ll agree them with the contributors once we know the scope and the resources available.

## Slide 15 — Prepare the hardware review

**Target: 14:15–15:00**

For the hardware review, we should be able to show what we can reuse, what we need to add, how it connects, and what the tests tell us. That gives us the basis for the drawings, space and power needs, parts and costs.

What I need from this meeting is a contact for each contributing group and control-engineering support. With those in place, we can complete the connection register and bring a full DPS concept back for review.

## Slide 16 — Backups — after the main talk

I’ll stop here. The Detector walkthrough and the other technical details are available for questions.

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

### Slide 27 — DPS switches PoF power through the PDU

For power over fibre, the proposed way to remove power is through the rack PDU. A local controller collects the box measurements. A separate box-enable connection is another option to investigate.

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
