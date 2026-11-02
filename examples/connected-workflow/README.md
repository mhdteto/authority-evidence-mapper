# Connected fictional example

**Entirely fictional teaching data:** Alex Rowan, Cedar Notes, publishers, HTTP responses, reviews, engines and answers are invented. Reserved example domains are placeholders. No client case or live AI measurement is presented.

Run from the repository root:

```sh
python3 map_evidence.py --claims examples/connected-workflow/inputs/claims.csv --evidence examples/connected-workflow/inputs/evidence.csv --as-of 2026-11-01 --output-dir examples/connected-workflow/report
```

Inputs: [claims.csv](inputs/claims.csv) · [evidence.csv](inputs/evidence.csv)

## Expected output

Three claims: the chair claim has support and a contradiction, with 1 independent-support publisher after duplicate normalization; the multilingual-publication claim lacks reviewed independent support; the office claim has missing evidence. All review labels are invented human declarations.

Inspect [the generated HTML](report/report.html) and [JSON](report/report.json). The command replaces the report directory’s output files; keep your own inputs elsewhere.

## Where this fits

[Follow the complete five-tool workflow](https://github.com/mhdteto/authority-architecture-system/tree/main/examples/fictional-workflow) · [Operating method](https://github.com/mhdteto/authority-architecture-system) · [Next: entity-structured-data-kit](https://github.com/mhdteto/entity-structured-data-kit)

These original synthetic inputs and reports use CC BY 4.0; the tool retains its existing code license. Verify reproduction with:

```sh
python3 tools/verify_connected_example.py
```
