# Monochrome presentation variants

`DUNElogo_gray.svg` and `FNAL-Logo-Black.svg` retain the alpha-channel shapes of
the existing `logosolo.png` and `FNAL-Logo-NAL-Blue.png`. Their SVG masks apply
one neutral grey or black fill. The source PNGs are embedded unchanged; the
original assets are not replaced, redrawn or rescaled out of proportion.

The matching PDFs are exported from these SVGs with Chromium at the SVG's
intrinsic page size and zero margins. Decks consume the PDFs directly, so
building a presentation needs no SVG renderer or browser.

These variants were added for the November 2026 DPS meeting deck at Manuel's
request. The grey DUNE mark is used on its title and Detector transition; the
black Fermilab mark is used on its content slides.
