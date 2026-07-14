# Full-Benchmark Scenario Review

Each full-benchmark manifest is a candidate until a human records it as
`approved` in `spec/full-benchmark-candidates.yaml`. Candidate status is an
execution gate, not a label: the preflight refuses to mark the study ready
while any required probe or paired control lacks approval.

## Review checklist

For every individual probe/control pair, verify all of the following:

1. The proposed failure mechanism matches its declared contamination class.
2. The paired control uses the same task but contains a genuinely relevant
   memory; it is not merely an easier prompt.
3. `source`, `age_days`, `domain`, and `fact_class` vary independently where
   the scenario tests provenance or staleness.
4. Retrieval assertions identify the intended inclusion, exclusion, or
   contradiction-pair behavior by stable memory IDs.
5. `forbidden_content` encodes the contamination criterion without treating a
   negated or quoted mention as an asserted error.
6. A deterministic `expected.utility.must_include_patterns` oracle measures
   whether the answer still performs the task.
7. The `rationale` explains why the scenario and its pair are discriminating.

## Approval record

Add one record per reviewed manifest to
`spec/full-benchmark-candidates.yaml`:

```yaml
- scenario_id: CB-FULL-SD-01
  status: approved
  approved_by: human reviewer name or role
  approved_at: 2026-07-14
  rationale: Human-reviewed candidate; paired task, retrieval oracle, and utility criterion verified.
```

AI may assist with an individual candidate, but the approving human must
review the actual manifest against this checklist. Do not add bulk approvals
or treat planning fixtures as accepted evidence.
