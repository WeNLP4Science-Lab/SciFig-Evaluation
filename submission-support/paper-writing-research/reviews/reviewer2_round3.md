# ACL Reviewer 2 -- Novelty & Contribution: Round 3 Review

**Paper:** SciFig-Eval: Evaluating Scientific Figure Understanding across Perception, Reasoning, and Behaviour
**Reviewer Role:** Novelty & Contribution (Reviewer 2)
**Review Type:** Revision check -- corpus expansion from 50 to 228/215 figures

---

## Does the Expansion Strengthen the Contribution?

**Yes, substantially.** The move from 50 admittance figures and 48 inductance figures to 228 and 215 respectively transforms A-R-I from a proof-of-concept probe on a convenience sample into a near-population evaluation over the 250-figure corpus. The total evaluation count rising from 23,000 to 34,000+ is meaningful because it brings the behavioural dimensions to the same coverage level as the perception and reasoning dimensions, which already operated on 250 figures. This was an implicit weakness in earlier rounds: the core novelty claim (behaviour diverges from perception) rested on a much smaller sample than the perception claim. That asymmetry is now largely resolved.

Table 4 now reports admittance and inductance on n=228 and n=215 respectively, compared to the full 250 for capability and resistance. The coverage is credible. The stability analysis (split-half rho=0.979, scale convergence at 100 figures) further supports that the expanded set is not just larger but stable.

---

## The Admittance Drop: 90% to 71%

This is the most interesting change in the revision and the paper handles it adequately but could do more.

### What happened
Gemini 3.1 Pro's active admittance dropped from 90% (Round 1, n=50) to 71% (Round 3, n=228). GPT-5.2 moved from 98% fabrication to 96% fabrication. Both shifts are in the same direction: the expanded corpus is harder for admittance detection, which is expected when moving from a curated subset to near-full coverage.

### Is the story still intact?
Yes. The 71% vs 8% gap between Gemini and GPT-5.2 remains enormous (63 percentage points). The "confident fabricator" finding still holds -- GPT-5.2 fabricates in 96% of cases despite leading on description quality. No other model besides Gemini exceeds 19% active admittance. The qualitative conclusion is unchanged: admittance is a separable dimension that perception scores miss entirely.

### What I would like to see acknowledged
The paper should note, even briefly, that the admittance rate is sensitive to which elements are tested. The original 50 figures were presumably easier cases (clearer blur targets, more obvious unrecoverability). The expansion introduced harder or more ambiguous cases where even Gemini sometimes fabricates. A single sentence in the results or limitations acknowledging this sample-sensitivity would be honest and strengthen credibility. The current text presents 71% without noting it was previously 90% on a smaller set, which is fine for a standalone submission but leaves a loose thread for anyone tracking revisions.

---

## Status of Previous Round 2 Issues

### Issue 2 (Inductance depth): STILL PARTIALLY RESOLVED
The quantitative validation is now stronger with n=215 (up from 48). Inductance correctness ranges are reported (14%-66% for inferable, 5%-14% for unrecoverable). The empirical separation between inferable and unrecoverable is convincing at this sample size. However, the deeper question -- what visual features make an element inferable vs. unrecoverable -- remains unaddressed. I no longer consider this a blocker given the expanded empirical base, but it remains the clearest path to a stronger paper. Even a brief error analysis on 20 inductance failures would add insight.

### Issue 4 (Compress basic transform results): RESOLVED
The transform results are now appropriately compressed. The selective blur results get proportionally more space, which is the right editorial trade-off given the expansion.

### Issue 5 (Cross-judge validation): PARTIALLY RESOLVED
The new capability question cross-judge check (Mistral Large scoring 344 questions, rho=1.000) is a welcome addition that directly addresses the seeder-judge circularity concern for reasoning. This is exactly the kind of targeted validation I requested. However, cross-judge validation for the MQM and behavioural dimensions still uses GPT-4o only. The limitation is still acknowledged honestly. I consider this partially resolved because the highest-risk circularity (capability questions) is now checked, even though a full cross-judge sweep remains absent.

### New Issue 1 from Round 2 (Language inconsistency): RESOLVED
The reproducibility appendix now correctly states "250 English-language scientific figures," consistent with the dataset section.

### New Issue 2 from Round 2 (Qwen family dominance): NOT ADDRESSED
Three of eight models remain Qwen variants. The paper still says "across eight models" without noting that three share architecture and training pipeline. This is minor but should be acknowledged in a sentence.

---

## New Issues in This Round

### New Issue 1: Table 3 caption reports n=228 and n=215 but text says "selectively blurring unrecoverable elements reduces MQM by roughly 8-10 points"
The MQM drop numbers in Section 5.2 (Selective blur paragraph) should be verified against the expanded set. If these numbers were computed on the original 50-figure subset and not updated, they may be inaccurate for the 228/215 sets. If they are updated, no action needed -- but the reader cannot tell.

### New Issue 2: The \todo markers remain in the submitted text
Section 5.2 contains multiple \todo{} markers (e.g., "confidence interval? did we motivate why we need this", "what is completeness penalty in our context?", "how this affects MQM categories?"). These must be resolved before submission. They also suggest that some methodological choices (confidence intervals, MQM category definitions) are not yet fully integrated into the narrative. This is an editorial issue, not a novelty concern, but it undermines readiness.

### New Issue 3: Introduction contribution (ii) has a dangling \todo
The second contribution item references a "controlled stress-test" with a \todo noting this phrase appears nowhere else and should reference a subsection number. This should be fixed to point to Section 3.2 (Behavioural Probes).

---

## Updated Scores

| Criterion | Round 1 | Round 2 | Round 3 | Change (R2->R3) |
|-----------|---------|---------|---------|-----------------|
| Excitement | 3.5/5 | 3.75/5 | 4.0/5 | +0.25 |
| Novelty | 3.5/5 | 3.75/5 | 4.0/5 | +0.25 |
| Positioning | 3/5 | 4/5 | 4/5 | -- |
| Findings significance | 4/5 | 4/5 | 4/5 | -- |
| Impact potential | 3.5/5 | 3.5/5 | 3.75/5 | +0.25 |
| Scope honesty | 3.5/5 | 4/5 | 4/5 | -- |

**Overall: 4.0/5 (up from 3.75/5)**

The expansion to 228/215 figures is the single biggest improvement across all three rounds. It converts the A-R-I framework from a suggestive pilot into a properly powered evaluation. The impact potential rises because the benchmark is now usable as-is by other researchers, rather than requiring them to first expand the selective-blur coverage.

---

## Updated Recommendation

**Accept.** The corpus expansion resolves the most substantive empirical weakness. The admittance drop from 90% to 71% actually strengthens the paper's credibility -- it shows the authors did not cherry-pick easy cases. The core finding (perception-behaviour disconnect, confident fabricator profile, presupposition embedding as strongest deception vector) is stable across the expansion. The cross-judge check on capability questions addresses the most pointed circularity concern.

Remaining items for camera-ready:
1. Remove all \todo markers and resolve the questions they raise.
2. Add one sentence noting that admittance rates vary with element selection and corpus coverage.
3. Acknowledge the Qwen family overlap when claiming "across eight models."
4. Verify that the MQM drop numbers in the selective blur paragraph reflect the expanded n=228/215 sets.

None of these are blockers. The paper makes a clear, now well-powered contribution that existing benchmarks do not provide.

---

## Summary of All Issues Across Three Rounds

| Issue | R1 | R2 | R3 |
|-------|----|----|-----|
| 1. Distinction from CHOCOLATE/ChartHal/CHAOS | Open | RESOLVED | RESOLVED |
| 2. Expand inductance analysis | Open | PARTIAL | PARTIAL (no longer blocking) |
| 3. Connect to calibration literature | Open | RESOLVED | RESOLVED |
| 4. Compress basic transform results | Open | PARTIAL | RESOLVED |
| 5. Cross-judge validation | Open | REMAINING | PARTIAL (capability checked) |
| 6. A-R-I branding too forced | Open | RESOLVED | RESOLVED |
| 7. Resistance not differentiated | Open | RESOLVED | RESOLVED |
| 8. Language inconsistency (R2 new) | -- | Open | RESOLVED |
| 9. Qwen family dominance (R2 new) | -- | Open | NOT ADDRESSED |
| 10. \todo markers in text (R3 new) | -- | -- | Open |
| 11. Verify selective blur MQM numbers (R3 new) | -- | -- | Open |

**Resolved: 6/11. Partially resolved: 2/11. Open/not addressed: 3/11 (all editorial, none blocking).**
