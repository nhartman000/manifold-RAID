# Audit of MG8 3.0 ISR → TCTA harness

**Source:** user-supplied `MG8_3.0.zip`; only the `isr_pipeline/*.py` source and `test_isr_hypothesis.py` were extracted to an isolated scratch folder and executed. The complete MG8 archive was not added to this repository or public package. Python harness exited 0; optional compiled `mg8_core` seal was unavailable in that isolated run and was skipped by the harness.

## Observed result

| Class | Raw guarded schemas | ISR-admitted | Verified on 30 fresh instances | Descriptor checks |
| --- | ---: | ---: | ---: | ---: |
| Sorted search | 343 | 4 | 1 of 4 | 1,624 |
| Prefix accumulation | 36 | 1 | 1 of 1 | 126 |

For sorted search the zero-ISR control admitted all 343 schemas and reported 145 oracle calls, versus 52 for the full-ISR 30-instance run. The ablation ladder admitted more false candidates as rules were removed. The sorted-search winning schema averaged 3.2 steps over the tested instances. These are bounded results from the fixed problem generators, transform vocabulary, seeded samples and rule templates in the archive.

## Interpretation and limits

- The harness discovers guard-to-transform bindings from *predefined* effect descriptors, guarded outcomes, and a fixed archetype library. It does not discover the transform semantics or a general invariant representation from arbitrary programs. In sorted search, `SearchClass.test` computes the midpoint before choosing the guard; that work is supplied by the problem definition.
- The full sorted-search ISR admitted **three candidates that failed verification**. Descriptor admissibility is a pruning filter, not a correctness certificate. Verification remains load-bearing.
- `R = 343/4 = 85.75` is the ratio of raw to admitted schema *counts*. Search still enumerated all 343 schemas and performed 1,624 descriptor checks. It is not an 85.75× runtime or total-compute reduction.
- The 145-versus-52 comparison counts only oracle calls after candidate execution passes earlier checks. It is not a complete cost comparison; failed executions, descriptor checks, rule/template construction, persistence, and verification must be counted.
- The harness has no persistent reconstruction record and no test of storage savings versus trace retention. It supports the possibility of rule-guided schema discovery without stored traces, a related component of Manifold RAID, but does not establish the full persistence methodology.
- `README_ISR_DEMO.md` labels false-admissible candidates as a “false-negative rate”; these are false positives of the descriptor filter. False-negative pruning requires checking whether the filter discards a genuinely valid schema.

## Next gate

Freeze a non-synthetic workload, training/holdout split and descriptor vocabulary. Persist an explicit ISR record and all versioned rules, then compare total bytes and end-to-end compute with a conventional stored-trace baseline. Report valid schemas pruned, invalid schemas admitted, closure failures, and workloads where the method loses. Keep the independent oracle unavailable to search and test on unseen instances and perturbations.
