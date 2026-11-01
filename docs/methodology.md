# Methodology and limits

The CLI reads local CSV files, validates the complete dataset, groups rows by exact claim ID, and exports the supplied declarations. It imports only the Python standard library and makes no network requests. It cannot confirm source existence, content, publisher identity, independence, reviewer qualifications or claim truth.

## Status rules

A claim with zero evidence rows is `missing evidence`. Otherwise each support label contributes a visible status: `unreviewed` becomes unreviewed; `partial` becomes partial; `supports` becomes supporting sources; `contradicts` becomes conflicting sources. Statuses coexist. A contradiction always remains visible when supporting rows also exist. There is no majority vote, confidence percentage or automatic resolution.

## Publisher counts

Publisher labels are normalized with Unicode NFKC, case folding, trimming and collapsing whitespace. Distinct publishers count every evidence row's normalized label, irrespective of relationship or support status. Independent support counts only normalized publishers with at least one row marked both `independent` and `supports`. Repeated articles from one publisher count once.

Normalization does not resolve corporate ownership, subsidiaries, syndication, publisher aliases, coordinated sources or fabricated publisher names. Maintain an explicit, consistent publisher naming convention. One publisher can have contradictory rows; its support count remains visible alongside the conflicting status. The count is an inventory metric, never credibility verification.

## Review age

Age is the calendar-day difference between `--as-of` and `accessed_on`. It is `stale` only when strictly greater than `--stale-days` (default 180); otherwise `within threshold`. A missing access date produces `unknown` and no numeric age. Age does not remove supporting or contradictory rows or alter publisher counts. It flags review work, not evidence invalidity, recency of the underlying event or a fact's expiration.

## Export safety and reproducibility

JSON preserves input text as data. HTML escapes all supplied text and URL attributes and accepts only HTTP(S) links. CSV prefixes formula-like cells with an apostrophe for spreadsheet safety; exported CSV may therefore differ from original cell values. This safety prefix is intentional and not a change to the evidence declaration. Reports contain supplied data, so choose output locations and sharing permissions accordingly.

The explicit reference date and threshold are recorded in JSON/HTML. Output order follows input claim and evidence order. No random values, current-clock dates, hidden models or external services affect the output. Validation completes before report writing, but filesystem failures can interrupt writes; use a new output directory when preserving an earlier report matters.
