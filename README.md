<p align="center"><img src=".github/readme-assets/banner.svg" width="100%" alt="Authority Evidence Mapper" /></p>

# Authority Evidence Mapper

An offline, installation-free Python CLI for mapping claims to supplied evidence reviews. See supporting and contrary evidence together, identify review gaps, and count distinct publishers without counting repeat articles as additional publishers.

**A source URL is never verification.** Relationships and support labels are declarations supplied by a human reviewer. This tool neither reads the sources nor decides whether a claim is true. It produces no authority score or ranking prediction.

<!-- shared-nav -->
<p>
  <a href="https://mohammedteto.com"><img src=".github/readme-assets/website.svg" width="148" height="36" alt="Website" /></a>
  <a href="https://mohammedteto.com/method/"><img src=".github/readme-assets/method.svg" width="148" height="36" alt="The method" /></a>
  <a href="https://mohammedteto.com/research/"><img src=".github/readme-assets/research.svg" width="148" height="36" alt="Research" /></a>
</p>

## Quick start

Requires Python 3.10 or newer. No packages, API keys, account or network connection are needed. Download the repository, open a terminal in its directory, and run:

```sh
python3 map_evidence.py --claims examples/claims.csv --evidence examples/evidence.csv --as-of 2026-11-01 --output-dir reports
```

Open `reports/report.html` in your browser. The same run creates `report.json`, `claims.csv` and `evidence.csv`. The date is explicit so review-age calculations are reproducible. Set `--stale-days 90` to change the default 180-day review threshold; exactly 180 days is within threshold.

The [fictional worked example](examples/claims.csv) covers an international person and an organization. All names, claims, reviews and publisher labels are invented; reserved example domains are illustrative URLs. The [generated HTML report](examples/output/report.html) is actual CLI output from these inputs, not a screenshot or a claim about real people.

## What the report shows

- Per-claim statuses: missing evidence, unreviewed, partial, supporting sources, conflicting sources. Several statuses can coexist.
- Distinct normalized publisher labels, and distinct publishers with a human-reviewed `supports` declaration and an `independent` relationship declaration.
- Every evidence row, including contrary evidence, its relationship, dates, review age and reviewer note.

Owned, affiliated, unknown and partial rows never increase the independent support count. Unknown access dates never appear fresh. Stale means the recorded access date is older than the configured review threshold; it does not mean the source is invalid. Rows marked `supports` are human-reviewed by input convention, not independently checked by this software.

## Prepare your inputs

Read the [input format](docs/input-format.md), [methodology](docs/methodology.md) and [interpretation guide](docs/interpretation.md). The CLI validates the whole dataset before writing outputs and exits with code 2 and a useful error for invalid input. Reports overwrite files of the same names in the selected output directory. Before writing any report, the CLI rejects output paths that resolve to either input file, including symlink aliases and existing hard links; choose a separate output directory. Keep source files and exported reports under your own access controls.

For the broader public approach, see [Mohammed Teto's method](https://mohammedteto.com/method/), [leaders](https://mohammedteto.com/leaders/), [organizations](https://mohammedteto.com/organizations/) and [research](https://mohammedteto.com/research/).

## Development

```sh
python3 -m unittest discover -s tests -v
python3 map_evidence.py --claims examples/claims.csv --evidence examples/evidence.csv --as-of 2026-11-01 --output-dir examples/output
```

Tests cover missing data, contradictory reviews, duplicate publishers and IDs, invalid dates and enums, unsafe URLs, HTML escaping and spreadsheet formula injection. CI runs tests and checks that the documented example regenerates committed outputs on Python 3.10 and 3.13.

Code is [MIT licensed](LICENSE). Documentation and original artwork are [CC BY 4.0](LICENSE-DOCS.md); see that notice for attribution. [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md).

## Companion resources

Created by **Mohammed Teto — AI Reputation & Authority Strategist** for international leaders and organizations.

- [Authority Architecture System](https://github.com/mhdteto/authority-architecture-system)
- [Entity Consistency Auditor](https://github.com/mhdteto/entity-consistency-auditor)
