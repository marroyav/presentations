# Speaker notes

## 1. SURF facility status and DUNE response

The central idea is simple: facility information helps DUNE understand its
operating environment, while action authority stays with the system that owns
the response. The architecture therefore separates monitoring, an orderly DAQ
stop, detector protection, and local protection.

## 2. Why the interface matters

The detector operates within a facility whose power, fire, air, cooling,
water, network, weather, and access conditions can affect operations. SURF and
DUNE view many of the same events, but they have different responsibilities.
That distinction is the reason for an explicit interface.

## 3. Four functions remain distinct

One event can appear in several places without becoming the same control path.
Slow Controls provides context. DAQ owns an orderly run transition. DPS owns an
approved detector action. Local protection remains close to the affected
equipment. Each function has its own owner and failure behavior.

## 4. How facility signals reach DUNE

The upper path is the monitoring path. Selected facility status crosses a
controlled boundary and appears in Slow Controls and operations. The lower path
is the detector-protection path. Its interface is defined by the approved
cause and effect, and it remains available without BMS monitoring.

The boxes describe functions rather than a particular device arrangement.

## 5. Who owns the alarm, action, and reset

Ownership follows the action. SURF retains authority over facility alarms and
their reset. DPS retains authority over detector trips and inhibits. Slow
Controls owns the DUNE presentation, history, and acknowledgement. DAQ owns the
run state. Joint operations provides escalation and learning across the
boundary.

## 6. What crosses the boundary

The interface carries enough information to support an operating decision:
state, time, quality, age, meaning, and ownership. BACnet/IP represents the
facility-facing exchange. OPC UA presents a normalized DUNE view. SNMPv3
provides service-health information. NTP and protected logs support a coherent
event chronology.

These protocols carry information. They do not transfer source-alarm or reset
authority to DUNE.

## 7. What changes when the facility changes

The response map compares six familiar classes of event. Power and reserve can
lead to an orderly DAQ stop. Network loss changes information quality. Fire and
air events remain under facility authority. Cryogenic, cooling, and water
conditions follow their approved detector response. Weather and access remain
operational context unless SURF defines an actionable state.

## 8. Unavailable information stays visible

GOOD, STALE, and UNKNOWN are different operating facts. Old data can remain in
history without being presented as current. Missing data does not silently
become normal. When communication returns, recovery of the data path does not
clear a latch or authorize equipment restart.

## 9. What is established—and what remains open

The division of authority and the four functional paths are already clear.
The remaining questions concern the authoritative point definitions, the live
service boundary, the conditions that justify DUNE action, and the behavior of
the detector-protection interface. Those questions sit with the owners of the
affected systems.

## 10. Architecture acceptance

Acceptance rests on four ideas. Every action has an identifiable owner. The
information keeps its meaning from source to operator. Failure remains visible
and does not erase independent protection. Test evidence demonstrates the
claimed boundary, selectivity, loss behavior, and recovery behavior.

The resulting relationship is straightforward: facility status informs DUNE;
DPS and local protection retain their own action paths.
