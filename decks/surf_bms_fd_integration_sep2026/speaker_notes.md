# Speaker notes

## 1 — How facility signals reach DUNE

BMS means building management system. Monitoring brings facility context into
DUNE; the separate DPS path carries approved protection states. Its design is
intended to retain the required function when monitoring is unavailable.
Power, communication, supervision and timing still need an agreed design.

## 2 — Alarm flow and ownership

Facility and DPS authority are parallel, not successive levels of control.
Dashed arrows carry status copies into Slow Controls. Run Control receives an
agreed availability state or stop request and owns the run transition.
A source owner may be SURF, cryogenics or another responsible system.

## 3 — Facility conditions

These are possible responses, subject to the source definition and agreed
cause and effect. LAr means liquid argon: pressure, level or low oxygen alone
does not establish a leak signal. An orderly DAQ stop depends on the agreed
timing and available power reserve.

## 4 — Proposed data exchange

BACnet/IP readout and an OPC UA bridge are a proposed route, not a selected or
verified installation. Read requests and replies do not imply write authority.
BACnet/SC and SNMPv3 depend on installed support. Protocol selection for the
protection interface remains separate.

## 5 — From concept to agreed interface

The discussion concerns point meaning, information flow and expected response.
Demonstration includes stale data, source faults, alarm routing, DAQ response,
recovery and the separation of acknowledgement and reset. Required protection
actions are checked with the monitoring service unavailable.

## Design references

DUNE-doc 37315 (Slow Controls communication proposal), EDMS 2907050 (FD1/FD2
interfaces), and DUNE-doc 36462 (Far Site safety configuration). These support
the proposal; they do not demonstrate an installed interface.
