# Speaker notes

## 1 — SURF–DUNE interface

The upper path carries facility information to operators. The lower path carries
an agreed protection input to DPS. Independence covers the monitoring service's
failure; power, transport and supervision still need an agreed design. The
diagram specifies functions and information flow, not equipment placement.

## 2 — Alarm and action ownership

An alarm can appear in DUNE without transferring control of its source. DUNE
acknowledgment records operator awareness. Source reset, run state and protection
reset remain separate actions. A source owner may be SURF, cryogenics or another
responsible system.

## 3 — Facility conditions and DUNE response

Each row is a proposed mapping for discussion with its owner. Network loss marks
uncertainty rather than a healthy condition. A leak response uses an explicit
source state; low oxygen or temperature alone does not establish a liquid argon
leak. Protection action follows the agreed mapping.

## 4 — Protocol choices

These are candidates pending confirmation of SURF services. BACnet read requests
and their replies are distinct from write authority. OPC UA provides the DUNE
view. SNMPv3 applies where the equipment supports it. None of these selections
defines the protection interface.

## 5 — From concept to agreed interface

The next discussion can resolve three items: what each point means, how its
information arrives, and what the systems do when information or equipment
fails. Observing reset and recovery is part of agreeing the interface, alongside
the initial alarm response.
