# Proposed responsibilities

**You own your equipment. Manuel connects the protection.**

Draft assignments for discussion; each person can correct or redirect their part.

| Who | First job |
|---|---|
| **Manuel** | Define the detector response. Connect HD and VD protection. |
| **Subsystem leads** | State what causes damage, how to stop it and how to verify the result. |
| **Trevor** | Connect the protective inputs to DPS and the required PDU/inhibit actions. |
| **Brandon** | Map smoke sensors and PDU outlets; expose their status and permitted configuration in SC. |
| **Linda + Terri** | Check power, grounding and local equipment boundaries. |
| **Arnab + Nick** | Mark the existing normal/UPS circuits and loads. |
| **Jack** | Route CUC space and cooling questions. |
| **Geoff** | Check who will support it and whether the effort is realistic. |
| **Ting** | Keep SC interfaces and decisions together. |
| **Joe Pygott** | Route facility ownership questions to the right source team. |
| **Michelle Stancari** | Connect interface decisions to the handover plan. |
| **Eric / Marco** | Settle the route for priority and resources. |

**First result:** one agreed boundary map, with an owner on each side of every connection.

**DPS protects. Slow Controls monitors and configures in parallel.** Protection decisions stay in DPS/local protection controllers; SC does not embed DPS logic.

For rack protection: **sensor → DPS decision → PDU outlet → equipment**. Manuel owns the response; Brandon/Trevor map the hardware; subsystem owners confirm what may be switched off.

Manuel's overall DPS responsibility is user-confirmed. Other names are proposed contacts based on the supplied September discussion, July electrical review or document authorship; these sources do not establish current line-management or acceptance authority. The source-system owner, maintainer and acceptance authority must be recorded separately where they differ.
