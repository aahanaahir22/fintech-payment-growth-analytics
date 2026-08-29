# Case Study: Improving Payment Reliability Without Treating Every Failure the Same

## 1. Problem

A payment platform can lose revenue and customer trust when authorization failures, network timeouts, authentication issues, configuration errors, and bank downtime are handled as one generic "payment failed" problem.

The objective of this case study is to identify the most material failure patterns in a multi-market synthetic portfolio and propose interventions that improve **payment success, customer experience, support demand, and recovered GMV** without creating excessive retry or operational risk.

## 2. Analytical approach

The analysis separates the portfolio by:

- market
- payment method
- merchant segment
- new vs. returning customer
- failure source and reason
- retry eligibility
- support-ticket creation
- latency

The primary KPI is **payment success rate**. Supporting metrics include **failed GMV, support-ticket rate, failure mix, method/market acceptance, and modeled recovered GMV**.

## 3. Findings

Across 4,000 synthetic attempts, the overall success rate is **88.42%** and failed GMV is **$33,003.92**.

- Card: **87.22%** success — lowest-performing payment method.
- India: **86.79%** success — lowest-performing market.
- Issuer declines: **22.25% of failures** — largest failure category.
- 336 failed attempts are flagged retry-eligible under the synthetic rules.

These findings suggest that the operating problem is not simply "too many failures." Different failure types require different treatments: some are potentially recoverable, some need customer action, some require merchant/integration remediation, and some are external downtime events.

## 4. Decision model

Four initiatives are prioritized using a RICE-style framework:

**Priority Score = Reach × Impact × Confidence ÷ Effort**

The framework is not presented as a mathematically perfect ranking. Its purpose is to make assumptions explicit and create a transparent decision conversation across Product, Operations, Engineering, Risk, and Support.

## 5. Recommended interventions

### A. Smart retry + downtime-aware routing
Use retry eligibility and downtime context to avoid treating transient failures the same as permanent customer/merchant failures. Primary KPIs: success-rate lift, recovered GMV, duplicate-payment/error guardrails.

### B. Failure-specific customer messaging
Replace generic failure messaging with actions tailored to authentication, incorrect payment details, or insufficient funds. Primary KPIs: repeat-failure rate and support-ticket rate.

### C. Merchant integration quality checks
Detect configuration issues earlier in onboarding or pre-production validation. Primary KPI: business-source failure rate.

### D. Market/method monitoring
Create acceptance dashboards and alert thresholds for deteriorating success rates or payment-method downtime. Primary KPIs: time to detect and success-rate variance.

## 6. Scenario analysis

A directional scenario assumes **25% of retry-eligible failures** can be recovered. Under that assumption:

- modeled success rate increases from **88.42% to 90.53%**;
- success rate improves by **2.10 percentage points**;
- modeled recovered GMV is approximately **$5,936.49**.

This is an analytical scenario, not a production experiment result. A real rollout would require controlled experimentation, duplicate-payment safeguards, monitoring, and risk review.

## 7. 90-day roadmap

- **Weeks 1–2: Diagnose** — validate taxonomy and baselines.
- **Weeks 3–4: Design** — define intervention requirements and guardrails.
- **Weeks 5–8: Pilot** — run controlled tests on selected segments.
- **Weeks 9–12: Scale** — operationalize dashboards, playbooks, monitoring, and rollout decision.

## 8. Limitations

- Dataset is synthetic and does not represent any specific company's production distribution.
- Failure probabilities and retry eligibility are modeling assumptions.
- The recovery scenario does not model causal uplift, cost, fraud exposure, or duplicate-payment risk.
- Currency is normalized to USD for portfolio analysis.

## 9. What I would do with real production data

1. Validate the event taxonomy and data-quality coverage.
2. Build cohort baselines by market, payment method, merchant segment, issuer, and customer type.
3. Estimate economic impact and support/contact cost by failure reason.
4. Design an experiment for the highest-priority recoverable failure category.
5. Track incremental success, recovered GMV, latency, customer contacts, refunds/duplicates, and risk guardrails.
6. Scale only when the intervention produces durable incremental value.
