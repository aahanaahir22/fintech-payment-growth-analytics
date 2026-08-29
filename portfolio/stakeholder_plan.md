# Stakeholder Communication Plan

| Stakeholder | Primary question | Information needed | Cadence |
|---|---|---|---|
| Product | Which failure problem should we solve first? | KPI movement, customer friction, prioritization score, experiment results | Weekly |
| Operations | Where is operational leakage happening? | Failure mix, market/method breakdown, downtime patterns, escalation thresholds | Weekly |
| Engineering | What should be implemented and instrumented? | Requirements, failure taxonomy, retry rules, event fields, guardrails | Sprint planning + async |
| Risk | Could recovery logic create unacceptable behavior? | Retry limits, decision gates, auditability, false-positive/duplicate-payment risk | Before pilot + scale gate |
| Support | Which failures drive customer contacts? | Ticket rate, failure-specific messaging, escalation paths | Biweekly |
| Leadership | Is the intervention worth scaling? | Success-rate lift, recovered GMV, support impact, implementation effort, risks | Phase gate |

## Decision principles

1. Prioritize interventions that improve both customer outcomes and economic value.
2. Separate observed metrics from modeled scenario assumptions.
3. Use staged decision gates before scaling recovery logic.
4. Track guardrails alongside the primary success KPI.
5. Tailor communication depth to the stakeholder's decision responsibility.
