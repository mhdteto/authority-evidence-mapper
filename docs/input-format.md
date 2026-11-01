# Input format

Both files must be UTF-8 CSV (an optional UTF-8 BOM is accepted). Headers must match the listed names exactly; order may vary. Quote commas and line breaks using standard CSV quoting. Extra/missing columns, duplicate headers and malformed CSV quoting (including unterminated quoted cells) are errors. Parsing is strict; malformed input exits with code 2 before any reports are written. Surrounding whitespace is removed from each cell.

## Claims

| Column | Meaning |
| --- | --- |
| claim_id | Required unique identifier; case-sensitive. |
| entity | Required person or organization name. |
| claim_text | Required precise claim to review. |

## Evidence

| Column | Meaning |
| --- | --- |
| evidence_id | Required unique evidence identifier; case-sensitive. |
| claim_id | Required exact reference to a claim in the claims file. |
| source_url | Required absolute HTTP or HTTPS URL, without credentials or whitespace. No fetching occurs. |
| publisher | Required publisher name. Use stable labels across rows. |
| published_on | Optional publication date, YYYY-MM-DD. |
| accessed_on | Optional last human access date, YYYY-MM-DD; blank means unknown review age. |
| relationship | Required: independent, owned, affiliated or unknown. Human declaration about relation to subject. |
| support_status | Required: supports, partial, contradicts or unreviewed. Human declaration of the review outcome. |
| review_note | Optional human rationale; include reviewer identity or provenance here when needed. |

All headers are required even when some cells are optional. Use `unreviewed` when only collecting a URL; a URL alone does not support a claim. Never label a relationship independent merely because its publisher has a different name.

Dates must be real calendar dates and cannot be after the explicit `--as-of` date. When both dates exist, publication cannot follow access. A blank publication date does not block review-age calculation; a blank access date yields unknown age even if publication is recent. Empty files with correct headers are accepted as empty inventories.

Examples use invented entities and reserved example URLs. Replace them with your own reviewed data before using the tool for decisions.

## Output path protection

The four output targets (`claims.csv`, `evidence.csv`, `report.json`, `report.html`) must not resolve to either input file. Symlink aliases and existing hard links are checked. A collision exits with code 2 before creating or writing reports, preserving source inputs. For example, using `--output-dir examples` with the bundled input paths is rejected. Use `--output-dir reports` instead.
