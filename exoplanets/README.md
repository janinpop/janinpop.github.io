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
