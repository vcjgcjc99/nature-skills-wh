# Science Bench V2 architecture figure

This example turns the Science Bench V2 evaluation report into an editable
Nature-style architecture diagram using the `nature-figure` design rules.

## Figure contract

- **Core conclusion:** Science Bench V2 evaluates scientific discovery as a
  gated, multi-layer loop: experiment, infer a Python law, validate on hidden
  hold-out points, and advance only when cross-layer constraints hold.
- **Archetype:** schematic-led composite.
- **Output:** editable SVG, with text preserved as SVG text nodes.
- **Panel map:**
  - **a:** end-to-end benchmark pipeline from domain catalogs to scoring reports.
  - **b:** 60-domain discipline layout and I/U/R/C relation vocabulary.
  - **c:** single-layer agent interaction loop and advance/stop gate.
  - **d:** conformance, composite scoring, and headline seed-0 execution results.

## Files

- `science_bench_v2_architecture.svg` - generated architecture diagram.
- `generate_science_bench_v2_architecture.py` - reproducible generator.

Regenerate the SVG with:

```bash
python3 examples/science_bench_v2_architecture/generate_science_bench_v2_architecture.py
```

The generator uses only the Python standard library so it can run in lightweight
agent environments without installing plotting dependencies.
