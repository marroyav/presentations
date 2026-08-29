"""One concept: a SiPM is represented by repeated microcells in parallel."""

from __future__ import annotations

import schemdraw.elements as elm

from ..sheet import Sheet


def build() -> Sheet:
    sheet = Sheet(
        schematic_id="S09-01",
        concept="sipm-microcells-in-parallel",
        title="SiPM equivalent — microcells in parallel",
        description=(
            "Representative microcell branches place a quench resistor and "
            "Geiger-mode APD between common cathode and anode rails; an "
            "ellipsis denotes additional parallel branches."
        ),
        scope="ILLUSTRATIVE CIRCUIT  /  NOT ERC-VERIFIED",
        classification="illustrative-circuit",
        source={
            "title": "The DUNE Photon Detection System (Phase I)",
            "url": "https://indico.cern.ch/event/1390649/contributions/6061526/attachments/2916523/5118380/LIDINE2024-dune%20pds.pdf",
            "page": 9,
        },
    )

    top_y = 5.25
    bottom_y = 1.75
    branch_x = (1.75, 6.00, 12.00)

    for index, x in enumerate(branch_x, start=1):
        branch_name = "branch-n" if index == 3 else f"branch-{index}"
        sheet.element_group(
            branch_name,
            (
                elm.Resistor().at((x, top_y)).down().length(1.25),
                elm.Photodiode().at((x, 4.00)).down().length(1.50),
            ),
        )
        sheet.junction(
            f"{branch_name}-top-junction",
            (x, top_y),
            allow_overlap=(branch_name,),
        )
        sheet.junction(
            f"{branch_name}-bottom-junction",
            (x, bottom_y),
            allow_overlap=(branch_name,),
        )

    terminal_x = 7.50
    sheet.terminal("cathode-terminal", (terminal_x, 5.75))
    sheet.terminal("anode-terminal", (terminal_x, 1.00))

    sheet.text(
        "resistor-label",
        (3.00, 4.60),
        "QUENCH R",
        halign="left",
    )
    sheet.text(
        "apd-label",
        (3.00, 3.15),
        "GM–APD",
        halign="left",
    )
    sheet.text(
        "ellipsis-label",
        (9.00, 3.45),
        "…",
        size=16,
        color=sheet.style.muted,
    )
    sheet.text(
        "cathode-label",
        (8.00, 5.75),
        "CATHODE  K",
        halign="left",
    )
    sheet.text(
        "anode-label",
        (8.00, 1.00),
        "ANODE  A",
        halign="left",
    )

    sheet.text(
        "source-limit",
        (0.75, 0.35),
        "Values, parasitics, and total microcell count N are unspecified.",
        size=sheet.style.font_sizes.note,
        color=sheet.style.muted,
        halign="left",
    )

    top_objects = tuple(
        name
        for branch in ("branch-1", "branch-2", "branch-n")
        for name in (branch, f"{branch}-top-junction")
    )
    bottom_junctions = tuple(
        f"{branch}-bottom-junction"
        for branch in ("branch-1", "branch-2", "branch-n")
    )
    sheet.route(
        "cathode-rail",
        [(branch_x[0], top_y), (branch_x[-1], top_y)],
        touches=top_objects,
    )
    sheet.route(
        "anode-rail",
        [(branch_x[0], bottom_y), (branch_x[-1], bottom_y)],
        touches=bottom_junctions,
    )
    for index, x in enumerate(branch_x, start=1):
        branch_name = "branch-n" if index == 3 else f"branch-{index}"
        sheet.route(
            f"branch-{index}-tail",
            [(x, 2.50), (x, bottom_y)],
            touches=(branch_name, f"{branch_name}-bottom-junction"),
            joins=("anode-rail",),
        )
    sheet.route(
        "cathode-terminal-lead",
        [(terminal_x, top_y), (terminal_x, 5.75)],
        touches=("cathode-terminal",),
        joins=("cathode-rail",),
    )
    sheet.route(
        "anode-terminal-lead",
        [(terminal_x, bottom_y), (terminal_x, 1.00)],
        touches=("anode-terminal",),
        joins=("anode-rail",),
    )
    return sheet
