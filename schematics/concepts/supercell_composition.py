"""One concept: the confirmed composition of a SuperCell."""

from __future__ import annotations

from ..sheet import Sheet


def build() -> Sheet:
    sheet = Sheet(
        schematic_id="S14-01",
        concept="supercell-composition",
        title="SuperCell composition",
        description=(
            "One SuperCell contains eight mounting boards; each board "
            "passively gangs six SiPMs, yielding 48 SiPMs and one channel."
        ),
        scope="STRUCTURE ONLY  /  NOT ELECTRICAL NETS",
        classification="system-structure",
        source={
            "title": "The DUNE Photon Detection System (Phase I)",
            "url": "https://indico.cern.ch/event/1390649/contributions/6061526/attachments/2916523/5118380/LIDINE2024-dune%20pds.pdf",
            "page": 14,
        },
    )

    sheet.block(
        "supercell",
        (7.00, 5.25),
        6.50,
        1.50,
        "SUPERCELL\n48 SiPMs / 1 CHANNEL",
        fill=sheet.style.surface,
    )
    sheet.block(
        "mounting-boards",
        (7.00, 3.25),
        6.50,
        1.50,
        "MOUNTING BOARDS\n8 PER SUPERCELL",
    )
    sheet.block(
        "sipms-per-board",
        (7.00, 1.25),
        6.50,
        1.50,
        "SiPMs PER BOARD\n6 / PASSIVELY GANGED",
    )

    sheet.route(
        "supercell-to-mounting-boards",
        [(7.00, 4.50), (7.00, 4.00)],
        touches=("supercell", "mounting-boards"),
    )
    sheet.route(
        "mounting-board-to-sipms",
        [(7.00, 2.50), (7.00, 2.00)],
        touches=("mounting-boards", "sipms-per-board"),
    )
    return sheet
