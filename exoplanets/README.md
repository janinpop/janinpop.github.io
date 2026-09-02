# Exoplanet Bestiary — static version

This version has no production backend.

## Fast update (recommended)

From the `exoplanets` directory:

```bash
python3 update_exoplanets.py
```

This downloads only the PSCompPars columns actually used by the bestiary.
It is much faster than downloading the whole table.

## Full PSCompPars snapshot

Only if you really want every NASA column:

```bash
python3 update_exoplanets.py --full
```

The website itself does not need full mode.

## Test locally

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

## GitHub Pages

Copy this folder as:

```text
janinpop.github.io/exoplanets/
```

Then the public page is:

```text
https://janinpop.github.io/exoplanets/
```

The included GitHub Action uses compact mode by default.


## Stellar rotation

The compact snapshot also downloads `st_rotp` (and uncertainties). When available, the stellar coloured-noise amplitude is sinusoidally modulated with that rotation period using the same time-compression factor as the planetary orbits.


## Permalinks and navigation

When a system is open, the URL stores:
- the host system,
- selected planets,
- stellar volume,
- planetary master volume,
- time-compression setting.

The modal includes previous/next-system arrows and a real `Permalien` hyperlink.
The left/right keyboard arrows also navigate between systems.


## Directional boost

The `Effet directionnel` control ranges from 1x to 3x.
It exaggerates the horizontal azimuth sent to the Web Audio HRTF panner while
keeping source distance unchanged. The value is stored in the permalink as
the `spatial` URL parameter.


## Permalink → catalogue card

Permalinks now also preserve the catalogue sort/filter context.
Every system card has a stable DOM anchor. Closing a system opened from a
shared permalink automatically renders, scrolls to, and highlights the
corresponding catalogue thumbnail.


## Planet timbre

Planetary voices use a continuous fat/metallic synthesizer:
- two slightly detuned saw oscillators for width/body,
- a quiet sub square,
- two inharmonic sine partials at sqrt(2) and 1+sqrt(2),
- resonant low-pass filtering,
- soft waveshaper saturation.

The fundamental frequency remains strictly determined by orbital period.
Planetary mass still controls only the final voice amplitude.


## Physical audio mappings (current)

- Orbital period -> fundamental pitch
- Planetary mass -> relative volume
- Eccentricity -> synth dirt / metallicity
  - detuning
  - inharmonic partial strength
  - resonant filter Q
  - saturation
- Orbital inclination -> 3D HRTF plane
  - i = 0 deg: face-on, left/right + up/down
  - i = 90 deg: edge-on, left/right + front/back
- Stellar rotation period -> stellar-noise amplitude modulation

Missing planetary inclinations still inherit the median measured inclination
of the system; this inferred value is explicitly labelled in the UI.


## Stellar heartbeat envelope

The stellar rotation period no longer produces sinusoidal amplitude modulation.

One stellar rotation corresponds to one two-contraction envelope:
- first contraction: strong `BOUM`
- second contraction: ~15% of a rotation later and slightly weaker
- low residual stellar noise between both contractions and the next cycle

The heartbeat period uses the same accelerated time scale as the planetary
orbits, so `P_rot,audio = year_seconds * P_rot(days) / 365.25`.


## Focused planet in permalinks

Permalinks now store the planet currently displayed in the detail card
independently from the list of planets selected for sonification.

Example:
`?system=TRAPPIST-1&selection=all&focus=TRAPPIST-1%20e`

On reload/paste, the system modal opens and the same planet detail card is restored.


## Pasted permalink behaviour

A pasted/shared permalink now lands on the corresponding catalogue thumbnail
instead of opening the system modal immediately.

The app:
1. restores catalogue filters/sort and sound controls,
2. renders enough catalogue batches to reach the system,
3. scrolls the thumbnail into view,
4. highlights it.

Clicking that highlighted thumbnail then opens the system while restoring the
permalink's planet selection and focused planet.


## Final permalink opening behaviour

A pasted permalink now:
1. restores catalogue filters/sort and sound controls,
2. renders enough catalogue batches to create the target system card,
3. positions the page on that card,
4. automatically reopens the system modal,
5. restores the focused planet and sonification selection.

Closing the modal returns to the same highlighted catalogue card.


## Permalink direct-open fix

When `?system=...` is present, the system modal now opens directly after the
local catalogue has loaded.

Important implementation detail: the modal is displayed before any attempt
to resume a Web Audio `AudioContext`. Browser autoplay restrictions therefore
cannot block the system sheet from opening. Audio unlocking is attempted only
during a real user interaction and is non-blocking.


## Smooth 3D HRTF motion

The auditory source direction is now angular-rate-limited before being sent to the Web Audio HRTF panner. Azimuth uses shortest-angle wrapping and is capped at one audible revolution per second; elevation is capped at half that angular speed. This prevents extremely time-compressed short-period planets from flipping abruptly between left/right while preserving inclination-driven front/back and up/down geometry.


## Adaptive time compression

The time-compression slider is now initialized from the fastest selected
orbital period in the opened system.

Rule:
- never faster than the historical baseline `1 year = 20 s`;
- compact systems are slowed so the fastest selected planet takes at least
  about 2 seconds per audible orbit.

`year_seconds_auto = max(20, 2 * 365.25 / P_min_days)`

The slider maximum expands dynamically when necessary. As soon as the user
moves the slider, the setting becomes manual and is no longer automatically
changed by planet selection. Opening another system calculates a new automatic
value. Permalink `year=` values are treated as explicit/manual settings.
