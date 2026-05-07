# Tables for RQ1

## MAIN TEXT TABLES (2)

---

### Table 1: Main Leaderboard — 13 Models Across Languages

**Location**: Main text, Page 1
**Purpose**: Hero table. The single most important table in the thesis.

| Column | Description |
|--------|-------------|
| Model | Model name, grouped by family |
| Params | Parameter count |
| Overall | Mean MQM across all figures, with 95% CI |
| English | Mean MQM on english_only subset |
| Bulgarian | Mean MQM on bulgarian_only subset |
| Chinese | Mean MQM on chinese_only subset |
| German | Mean MQM on german_only subset |

**Rows** (grouped by family):
- Proprietary: GPT-5.2, Gemini 3.1 Pro, Claude Opus 4.6
- Qwen3-VL: 235B, 32B, 30B, 8B
- LLaMA-4: Maverick, Scout
- Gemma-3: 27B, 12B, 4B
- Phi-4 Multimodal

**Formatting**:
- Bold best, underline second-best per column
- 95% CI in parentheses: `78.3 (75.1-81.5)`
- Group families with midrules
- Booktabs style, no vertical lines
- Report for both judges (dual columns or average with footnote)

**Data source**: `output/evaluation/atomic_mqm_v2/{judge}/{model}/`

---

### Table 2: Human vs LLM Judge Comparison

**Location**: Main text, Page 3
**Purpose**: Validate LLM judges against human ground truth.

| Column | Description |
|--------|-------------|
| Model | 4 evaluated models |
| Human MQM | Mean human MQM with 95% CI |
| GPT-4o MQM | LLM judge score on same 30 figures |
| Mistral MQM | LLM judge score on same 30 figures |

**Footer rows**:
- Spearman rho (Human-GPT4o, Human-Mistral)
- Kendall tau (Human-GPT4o, Human-Mistral)
- Krippendorff's alpha (inter-annotator)

**Data source**: `HumanEval/human_eval_results.json` + `output/evaluation/atomic_mqm_v2/`

---

## APPENDIX TABLES (10)

---

### Table A.1: Full Leaderboard with Detailed CIs

Same as Table 1 but adds:
- Multi-language column
- Per-judge columns (GPT-4o score | Mistral score)
- Full CI ranges
- Significance markers (* p<0.05) for adjacent-rank pairs

---

### Table A.2: Per-Language EN-X Gap Metrics

| Column | Description |
|--------|-------------|
| Model | 13 models |
| EN | English MQM |
| BG | Bulgarian MQM |
| CN | Chinese MQM |
| DE | German MQM |
| EN-BG Gap % | (EN - BG) / EN * 100 |
| EN-CN Gap % | (EN - CN) / EN * 100 |
| EN-DE Gap % | (EN - DE) / EN * 100 |

---

### Table A.3: Per Chart Type Breakdown

| Column | Description |
|--------|-------------|
| Chart Type | Bar, Line, Pie, Scatter, Heatmap, Box, etc. |
| N | Number of figures |
| Avg Atoms | Complexity proxy |
| Mean MQM | Average across all models |
| Best Model | Highest scoring |
| Worst Model | Lowest scoring |

---

### Table A.4: Pairwise Significance Tests

- All 78 model pairs (or 12 adjacent-rank pairs)
- Columns: Model A, Model B, Delta, p-value (paired bootstrap), Cliff's delta, Significance
- Bonferroni-corrected p-values

---

### Table A.5: Hallucination Rates per Model

| Model | Hallucination Count | Rate (per fig) | % of Total Errors |

---

### Table A.6: Prompt Ablation (C1 / C2 / C2')

| Condition | EN | BG | CN | DE | Avg | Delta vs C1 | p-value |
|-----------|----|----|----|----|-----|-------------|---------|
| C1 (native) | ... | ... | ... | ... | ... | — | — |
| C2 (English) | ... | ... | ... | ... | ... | +/- | ... |
| C2' (EN→native) | ... | ... | ... | ... | ... | +/- | ... |

---

### Table A.7: Chain-of-Thought Ablation

| Model | Direct MQM | CCoT MQM | Delta | p-value |

---

### Table A.8: Cross-Lingual Controlled (13 Parallel Figures)

| Model | EN | BG | CN | DE | EN-BG | EN-CN | EN-DE |

Only the 13 figures with all 4 language annotations — eliminates figure difficulty confound.

---

### Table A.9: Error Sub-type Detailed Counts

| Error Sub-type | GPT-4o Count | Mistral Count | Human Count | % |
|----------------|-------------|---------------|-------------|---|
| Incorrect Numerical Value | ... | ... | ... | ... |
| Incorrect Visual Attribute Mapping | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

---

### Table A.10: Judge Agreement Matrix

|  | Human | GPT-4o | Mistral |
|--|-------|--------|---------|
| Human | — | rho / tau | rho / tau |
| GPT-4o | rho / tau | — | rho / tau |
| Mistral | rho / tau | rho / tau | — |

Plus: ICC, weighted Cohen's kappa for human annotator pairs.

---

## Formatting Standards (All Tables)

- Booktabs style (toprule, midrule, bottomrule)
- No vertical lines
- Bold best, underline second-best per column
- 95% CI in parentheses for key scores
- Significance: * p<0.05, ** p<0.01, *** p<0.001
- All scores to 1 decimal place
- Caption includes judge model and figure count
