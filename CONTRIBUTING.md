# Contributing

Use Python 3.10+ and the standard library. Keep the CLI offline and the outputs explainable. Include regression tests for behavior changes, especially any change to missing/contrary evidence, date semantics or exported text safety.

Run `python3 -m unittest discover -s tests -v` and regenerate the example using the command in README before submitting a change. Explain the user-visible behavior and validation results. Use fictional or explicitly licensed sample data; never contribute private customer records or source credentials. Code contributions use MIT; documentation and original artwork use CC BY 4.0. No contribution should imply that the tool verifies truth or predicts ranking.

## Choose a contribution route

- [Bug or documentation error](https://github.com/mhdteto/authority-evidence-mapper/issues/new?template=bug_report.yml): include a release tag or commit and a minimal public/fictional reproducer.
- [Feature request](https://github.com/mhdteto/authority-evidence-mapper/issues/new?template=feature_request.yml): state the task, example and proposed behavior.
- [Source or methodology proposal](https://github.com/mhdteto/authority-evidence-mapper/issues/new?template=source_proposal.yml): provide the specific claim, publisher, dates, market, relationship and limits.

Run the documented validation and preserve the distinction between observed, supplied, inferred and unknown. See the [connected fictional workflow](https://github.com/mhdteto/authority-architecture-system/tree/main/examples/fictional-workflow) for an example.
