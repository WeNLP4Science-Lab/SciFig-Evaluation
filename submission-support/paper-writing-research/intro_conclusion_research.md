# ACL Paper Writing Research: Introduction, Abstract, Conclusion, Limitations, Ethics

Deep research on how top ACL/NLP papers (2024-2025 best paper winners) structure their key sections, with specific focus on benchmark and evaluation papers.

---

## 1. Abstract Best Practices

### Word Count and Length
- ACL abstracts typically run **150-250 words**
- Best paper examples: Mission: Impossible Language Models (223 words), Aya Model (~226 words), OLMo (~145 words)
- Sweet spot for benchmark papers: **200-230 words** -- enough to convey scope without overwhelming

### Proven Structure (5-Part Framework)
Based on analysis of ACL 2024 best papers and Vered Shwartz's widely-cited NLP writing guide:

1. **Problem/Context** (1-2 sentences): Establish the broad area and why it matters
2. **Gap/Tension** (1-2 sentences): What is missing, broken, or unknown
3. **Our Approach** (2-3 sentences): What we do and at what scale
4. **Key Finding** (1-2 sentences): The headline result, stated concretely
5. **Release/Impact** (1 sentence): What we release and why it matters

### Hook Sentence Patterns from Award Winners

**Pattern A: Bold claim + challenge it**
> "Chomsky and others have very directly claimed that large language models are equally capable of learning languages that are possible and impossible for humans to learn. However, there is very little published experimental evidence to support such a claim."
-- Mission: Impossible Language Models (ACL 2024 Best Paper)

**Pattern B: Rhetorical question**
> "Recent breakthroughs in large language models have centered around a handful of data-rich languages. What does it take to broaden access to breakthroughs beyond first-class citizen languages?"
-- Aya Model (ACL 2024 Best Paper)

**Pattern C: State of the world + problem**
> "Language models have become ubiquitous in both NLP research and in commercial product offerings. As their commercial importance has surged, the most powerful models have become closed off..."
-- OLMo (ACL 2024 Special Topic Award)

**Pattern D: Surprising fact or counterintuitive observation**
Works well for evaluation papers that reveal unexpected gaps or failures in existing systems.

### How to Make Scale Sound Impressive (for our 250-figure paper)
- Lead with the unique dimension, not just raw count: "the first systematic evaluation spanning X dimensions across Y figures"
- Use comparative framing: "N times larger than the closest existing benchmark"
- Emphasize coverage: "spanning 4 languages, 11 models, and 4 evaluation paradigms"
- Qualify scale with depth: "not just more figures, but deeper analysis per figure"

### What NOT to Put in Abstracts
- References or citations
- Undefined acronyms (define on first use or avoid)
- Multiple paragraphs (always single paragraph)
- Sentences reused verbatim from the paper body
- Overly general opening sentences ("AI is transforming the world...")
- Detailed methodology or hyperparameters
- Future work

---

## 2. Introduction Best Practices

### Length and Structure
- Typically **1.5-2 pages** (4-7 paragraphs)
- For benchmark/evaluation papers, 5-6 paragraphs is common
- First person "we" is standard and expected in ACL papers

### Paragraph-by-Paragraph Template

#### Paragraph 1: The Hook and Context (4-6 sentences)
**Purpose**: Establish the broad problem area and why anyone should care.

**Template structure**:
- Sentence 1: Bold, attention-grabbing statement about the state of the field
- Sentence 2-3: Expand on why this matters (practical or scientific importance)
- Sentence 3-4: Narrow from broad to specific area of focus
- Optional: A concrete example that grounds the abstract problem

**Example opening sentences from best papers**:
- Claim + challenge: "X has been widely assumed... but evidence is thin"
- Gap statement: "Despite progress in X, Y remains poorly understood"
- Tension: "X and Y are both important, yet they pull in opposite directions"
- Scale: "N systems now rely on X, yet we lack a principled way to evaluate them"

**AVOID**: "In recent years, [topic] has attracted much attention" -- this is the most common weak opening in NLP papers.

#### Paragraph 2: Prior Work and the Gap (4-6 sentences)
**Purpose**: Acknowledge what exists and precisely identify what is missing.

**Template structure**:
- Sentence 1: "Prior work has addressed X through approaches A, B, and C"
- Sentence 2-3: Brief, fair summary of key existing work (cite generously)
- Sentence 4: The pivot -- "However, these approaches share a common limitation..."
- Sentence 5: State the gap crisply and specifically

**Key principle**: The gap must be a real, defensible gap -- not just "nobody did exactly our thing." Frame it as a community need, not a personal interest.

**For benchmark papers specifically**:
- "Existing benchmarks focus on X but neglect Y"
- "Evaluation has been limited to [single dimension], missing [critical aspect]"
- "No systematic study has examined [phenomenon] across [scale/diversity]"

#### Paragraph 3: Our Approach (3-5 sentences)
**Purpose**: Introduce what you did, at a high level, without methodology details.

**Template structure**:
- Sentence 1: "In this work, we present/introduce [NAME], a [brief description]"
- Sentence 2: Scale and scope -- "spanning N figures, M models, K languages"
- Sentence 3: Key methodological innovation -- what makes your approach different
- Sentence 4: What makes this possible or how you enabled this at scale

**For benchmark papers**: Emphasize the design principles, not just the artifact. Why these figures? Why these models? Why this evaluation framework?

#### Paragraph 4: Key Findings Preview (3-5 sentences)
**Purpose**: Give readers a reason to keep reading by previewing the most compelling findings.

**Template structure**:
- Sentence 1: "Our evaluation reveals several key findings"
- Sentence 2-4: State 2-3 headline findings, each in one sentence
- Focus on surprising or counterintuitive results
- Use specific numbers where they are compelling

**Key principle**: Preview findings; do not exhaustively list them. Save detailed results for the results section. The goal is to create curiosity, not to replace the results section.

**AVOID**: "Our results show that our method outperforms baselines" -- this is vague and uninteresting.

#### Paragraph 5: Contributions List (variable length)
**Purpose**: Explicitly enumerate what the paper contributes to the field.

**Standard format**: Numbered list, typically 3-4 items. This is the dominant convention in NLP.

**Template**:
> Our contributions are as follows:
> 1. We introduce [ARTIFACT] -- a [description with scale] (Section N).
> 2. We conduct [ANALYSIS] -- revealing [key insight] (Section N).
> 3. We release [RESOURCE] -- enabling [future use] (Section N).

**Common contribution verbs**: introduce, present, propose, conduct, release, develop, provide, demonstrate

**For benchmark papers, typical contributions**:
1. The benchmark/dataset itself (artifact contribution)
2. A systematic evaluation/analysis (knowledge contribution)
3. Key findings or insights (knowledge contribution)
4. Open-source release of data/code (artifact contribution)

**Rules**:
- 3-4 contributions is the sweet spot; 5+ dilutes impact
- Each contribution should be independently valuable
- Include section references to help reviewers navigate
- The first contribution is your primary one -- make it strongest

#### Optional Paragraph 6: Paper Organization (1-2 sentences)
**Purpose**: Brief roadmap. Some papers include this; others fold it into the contributions list.

Not strictly necessary for ACL papers. If the contributions paragraph includes section references, this is redundant.

### Where Does Figure 1 Go?

**Placement**: Top of the first or second page, ideally visible without scrolling/turning the page. In two-column ACL format, Figure 1 is often placed as a full-width figure spanning both columns at the top of page 1.

**What Figure 1 should show for a benchmark/evaluation paper**:
- **Option A: Overview/architecture diagram** showing the evaluation pipeline
- **Option B: Teaser result** -- one compelling, visually striking finding that draws readers in
- **Option C: Task illustration** -- concrete example of what the benchmark tests
- **Option D: Scale visualization** -- showing the scope/coverage of the benchmark

**Best practice**: Figure 1 should be self-contained and understandable from its caption alone. A reviewer skimming should grasp your paper's key idea from Figure 1 + caption.

**For our paper**: A figure showing example scientific figures with model descriptions side by side, or a matrix showing the evaluation dimensions (models x languages x metrics), would work well.

### First Person "We" Usage
- Standard and expected in ACL papers
- "We" for describing what the authors did: "We introduce...", "We find that..."
- "We" for inclusive statements about the community: "We argue that..."
- Avoid "I" even for single-author papers (ACL convention)
- Do not overuse hedging: "We believe" is weaker than "We find" or "We show"

### Balancing Motivation vs Technical Preview
- Introduction should be ~80% motivation, ~20% technical preview
- Save methodology details for the methods section
- The introduction should be accessible to any NLP researcher regardless of subarea
- Avoid notation, formulas, or detailed algorithms in the introduction
- If you must mention a technical detail, explain it in plain language

---

## 3. Conclusion Best Practices

### Length
- Typically **0.5 pages** (half a column to a full column in ACL two-column format)
- 3-4 paragraphs is common
- Should NOT simply be a summary of the paper

### Structure

#### Paragraph 1: Restate the Problem and What You Did (2-3 sentences)
- Brief, high-level restatement -- different wording from the introduction
- "In this paper, we presented X, which addresses Y"
- This should be shorter than the introduction's version

#### Paragraph 2: Key Takeaways (3-5 sentences)
- Not a repetition of results -- this is the "so what?" paragraph
- What should the community take away from this work?
- What new understanding does this work enable?
- State implications, not just findings

**Good**: "Our findings challenge the assumption that X, suggesting that the field should reconsider Y"
**Bad**: "We found that Model A scored 0.85 and Model B scored 0.72"

#### Paragraph 3: Broader Impact or Implications (2-3 sentences)
- How does this work change how the community should think about evaluation?
- What does this mean for practitioners building real systems?
- What principles emerge from your findings?

#### Paragraph 4: Future Work (2-4 sentences)
- **How much**: Keep it brief and specific -- 2-4 concrete directions
- **How specific**: Name specific extensions, not vague aspirations
- **Tone**: Frame as exciting opportunities, not missing pieces

**Good future work**:
- "Extending to additional modalities (charts, diagrams, photographs)"
- "Investigating whether our findings generalize to domain-specific figures"
- "Developing automated metrics that better correlate with human judgment"

**Bad future work**:
- "More work is needed in this area" (too vague)
- "We plan to improve our method" (undermines current work)

### How to End on a Strong Note
- End with a forward-looking statement about impact
- The last sentence should leave a positive impression
- Options: call to action, vision statement, or statement of what your work enables
- Example: "We hope [RESOURCE] serves as a foundation for more rigorous evaluation of scientific figure understanding"

### What NOT to Do in Conclusions
- Do not introduce new results or analysis
- Do not repeat the abstract
- Do not be defensive about limitations (that goes in the Limitations section)
- Do not add new citations that were not in the main text
- Do not use "In conclusion" as the opening phrase (use "We have presented..." or similar)

---

## 4. Limitations Section (Mandatory for ACL)

### Placement and Format
- Comes after the conclusion, before references
- Titled exactly "Limitations"
- Does NOT count toward the page limit
- Can only include discussion of limitations -- no new experiments, figures, or analysis
- Typically **0.5-1 page** (3-6 paragraphs)

### The Three Approaches (Only One Works)
Based on analysis of published papers:

1. **The Confessional** (too much): Lists every possible flaw, undermining confidence in the work. AVOID.
2. **The Dismissal** (too little): Handwaves limitations with a sentence or two. Reviewers will notice. AVOID.
3. **The Reflection** (right approach): Honest, balanced acknowledgment of scope constraints with explanation of why they do not invalidate the findings. USE THIS.

### How to Handle Limitations Honestly Without Undermining Your Work

**Framework**: For each limitation, use this structure:
1. **State it clearly**: "Our evaluation is limited to [scope]"
2. **Explain the rationale**: "We chose this scope because [principled reason]"
3. **Acknowledge the impact**: "This means our findings may not generalize to [context]"
4. **Point forward**: "Future work should examine [extension]"

### Common Limitations for Benchmark/Evaluation Papers

1. **Scale/coverage limitations**
   - "Our benchmark covers N figures, which, while substantial, may not capture the full diversity of scientific figures"
   - "We focus on [4 languages]; extending to additional languages remains future work"

2. **Model selection**
   - "We evaluate N models available at the time of study; the rapidly evolving landscape means newer models may perform differently"
   - Frame as a snapshot in time, not a permanent ranking

3. **Evaluation methodology**
   - "Human evaluation, while gold-standard, is inherently subjective"
   - "Our MQM framework captures specific quality dimensions but may not reflect all aspects of description quality"

4. **Data/domain limitations**
   - "Our figures are drawn from [specific domains/sources]; generalization to other domains is not guaranteed"
   - "Figures vary in complexity; our analysis does not stratify by difficulty"

5. **Annotation limitations**
   - "Inter-annotator agreement, while reasonable, reflects inherent subjectivity in evaluation"
   - "Annotators were [demographics]; different annotator pools might yield different results"

### What to Acknowledge vs What to Defend

**Acknowledge** (be honest):
- Scope choices (language, domain, model selection)
- Annotation subjectivity
- Temporal limitations (models evolve)
- Resource constraints that affected scale

**Defend** (explain your reasoning):
- Design choices you made deliberately (e.g., why MQM over other frameworks)
- Sample size if it is justified by the depth of analysis
- Model selection if it covers a representative range

### Tone
- Matter-of-fact, not apologetic
- Confident, not defensive
- "This is the scope we chose and here is why" -- not "we are sorry we could not do more"

---

## 5. Ethics Statement (Mandatory for ACL)

### Placement and Format
- Comes after Limitations, before references (or after Limitations)
- Titled "Ethical Considerations" (recommended title per ACL guidelines)
- Does NOT count toward the page limit
- Typically **short**: 0.25-0.5 pages (1-3 paragraphs)

### What Benchmark Papers Should Include

1. **Data provenance and licensing** (most important for benchmark papers)
   - Where data comes from
   - Licensing terms and whether use is permitted for research
   - Whether data is publicly available or requires access agreements

2. **No personally identifiable information (PII)**
   - Confirm figures do not contain PII
   - If they do, explain anonymization steps

3. **Annotator welfare**
   - If human evaluation was involved: payment, working conditions, consent
   - Were annotators paid fairly? (ACL reviewers check this)
   - Was the task potentially harmful or distressing?

4. **Potential for misuse**
   - Could the benchmark be used to game or overfit models?
   - Are there dual-use concerns?

5. **Environmental impact** (optional but appreciated)
   - Compute costs for running evaluations
   - Carbon footprint considerations

6. **Evaluation fairness**
   - Were all models evaluated under the same conditions?
   - Are there biases in the evaluation framework?

### Example Structure for Our Paper

> **Ethical Considerations**
>
> All scientific figures used in this study are sourced from [publicly available papers / specific sources] under [license terms]. No personally identifiable information appears in the dataset. Human evaluators were compensated at [rate], above the local minimum wage, and provided informed consent for participation. Our evaluation framework applies identical conditions across all models to ensure fairness. We acknowledge that benchmark results may be used for model comparison; we caution against over-interpreting small score differences and encourage holistic assessment.

### Responsible NLP Checklist Items to Address
Per the ARR checklist, benchmark papers must address:
- A1: Limitations discussion (covered in Limitations section)
- A2: Risk assessment
- B1-B6: Scientific artifacts (citations, licenses, documentation, statistics)
- C1-C4: Computational experiments (resources, setup, statistics)
- D1-D5: Human annotators (if applicable -- instructions, payment, consent, demographics)
- E1: AI assistant disclosure (if used)

---

## 6. The "First Page" Test

### What Must Appear on Page 1

Reviewers form their first impression from the opening page. In ACL two-column format, page 1 contains:
- **Title**: Should be specific, memorable, and contain key terms. For benchmark papers, include the benchmark name.
- **Abstract**: Single paragraph, 200-230 words
- **Start of Introduction**: At least the first 2 paragraphs
- **Ideally Figure 1**: A full-width teaser figure at the top

### How Best Papers Make Page 1 Irresistible

1. **Title is specific and evocative**: "Mission: Impossible Language Models" is memorable. "Aya Model" names the artifact. "OLMo: Accelerating the Science of Language Models" states the mission.

2. **Abstract has a clear hook in sentence 1-2**: Not generic, not throat-clearing. Immediately identifies what is at stake.

3. **Introduction paragraph 1 grabs attention**: Best papers open with bold claims, surprising facts, or compelling questions -- never with "In recent years, X has gained attention."

4. **Figure 1 is visually compelling**: Clean, informative, and self-contained. A reviewer should understand the paper's core idea from Figure 1 + its caption alone.

### Hook Strategies That Work

| Strategy | Example | Best For |
|----------|---------|----------|
| Challenge conventional wisdom | "X is widely believed, but we show Y" | Papers that overturn assumptions |
| Rhetorical question | "What does it take to...?" | Papers proposing new solutions |
| Concrete problem illustration | "Consider this figure... Can a model describe it?" | Benchmark/evaluation papers |
| Scale framing | "N models, M tasks, K languages -- yet no systematic..." | Large-scale evaluation papers |
| Surprising statistic | "Models fail on X% of cases that humans find trivial" | Papers revealing gaps |

### Hook Strategies That Feel Forced
- Name-dropping ("As Chomsky once said...") -- unless directly relevant as in Mission: Impossible
- Excessive hype ("Revolutionary breakthrough in...")
- Starting with a dictionary definition
- "Imagine a world where..." scenarios
- Meta-commentary about the field ("AI is experiencing unprecedented growth")

---

## 7. Common Mistakes

### Introduction Mistakes
1. **Too long**: More than 2 pages signals unfocused motivation. Cut to essentials.
2. **Too vague**: "We study scientific figure understanding" -- specify what about it, why now, what is new
3. **Too much related work in the intro**: Save detailed comparisons for the Related Work section. The intro should mention prior work only to establish the gap.
4. **Contributions that are not contributions**: "We survey the literature" is not a contribution. "We provide a framework" is only a contribution if the framework is novel.
5. **Too many contributions**: More than 4 contributions dilutes perceived impact. Consolidate.
6. **No findings preview**: Reviewers want to know what you found before investing 8 pages.
7. **Burying the lead**: If your most interesting finding is in paragraph 5, move it up.
8. **Generic opening**: "Recently, large language models have achieved remarkable performance..." -- every other paper starts this way.

### Abstract Mistakes
1. **Too technical**: Abstract should be accessible to any NLP researcher
2. **No hook**: Starting with generic background instead of a specific claim or question
3. **Too long**: Over 250 words for an ACL paper is excessive
4. **No concrete results**: Vague claims without numbers or specific findings
5. **Including citations**: Abstracts should be self-contained

### Conclusion Mistakes
1. **Just summarizing**: "In Section 2, we described... In Section 3, we showed..." -- this adds no value
2. **Introducing new results**: The conclusion should synthesize, not present new findings
3. **Being too short**: A 2-sentence conclusion suggests you ran out of steam
4. **Vague future work**: "We plan to explore more" is not useful
5. **Ending weakly**: Last sentence should resonate, not trail off

### Limitations Mistakes
1. **Too brief**: A single sentence looks dismissive. Reviewers will hold this against you.
2. **Too defensive**: "Our work has no significant limitations" is a red flag
3. **Disguised bragging**: "A limitation is that we only evaluated 11 models, which is more than any prior work" -- this is transparent
4. **Including new analysis**: The Limitations section must contain only discussion, no new experiments or figures
5. **Ignoring obvious limitations**: If a limitation is obvious and you do not mention it, reviewers will assume you are unaware

### Ethics Statement Mistakes
1. **Missing entirely**: It is mandatory for ACL submissions
2. **Boilerplate**: Generic statements that could apply to any paper
3. **Not addressing annotator compensation**: If you used crowdworkers, reviewers will check

### Overclaiming in Contributions
- Do not claim "state-of-the-art" unless you have comprehensive comparisons
- Do not claim "first" unless you have thoroughly checked
- Do not claim "comprehensive" unless your coverage is genuinely exhaustive
- Hedge appropriately: "To our knowledge" is useful when claiming firsts
- Let results speak for themselves rather than using superlatives

---

## 8. ACL Reviewer Scoring (Know Your Audience)

As of 2025, ACL Rolling Review reviewers score on three main dimensions:

### Soundness (1-5)
- Are claims supported by evidence?
- Is the methodology correct?
- Are experiments reproducible?
- **For benchmark papers**: Is the evaluation design principled? Are the metrics appropriate?

### Excitement (1-5)
- Is this novel and interesting?
- Would you tell colleagues about this paper?
- **For benchmark papers**: Does this fill a real gap? Will the community use this?

### Overall Assessment (1-5)
- 5: Consider for Award
- 4: Conference acceptance
- 3: Findings acceptance
- 2: Substantial revisions needed
- 1: Do not resubmit

**Key insight**: A benchmark paper can score high on soundness and overall even without breakthrough novelty, if it fills a genuine need and is executed with rigor. The reviewer guidelines explicitly note that "creating a high-quality resource for a language/domain that does not yet have resources of that type may not sound very novel or exciting, but you may still consider it a significant contribution due to its potential impact."

---

## 9. Template: Complete Introduction Structure for SciFig Evaluation Paper

Below is a concrete paragraph-by-paragraph template for our paper.

### Paragraph 1: Hook and Motivation (5-6 sentences)
> [Bold opening about scientific figures being critical knowledge artifacts.]
> [Expand: millions of figures in scientific literature; they encode findings that text alone cannot capture.]
> [Narrow: vision-language models are increasingly used to interpret these figures.]
> [Tension: but how well do they actually perform? On what dimensions do they succeed or fail?]
> [Optional concrete example: a model confidently describing a chart while missing key data points.]

### Paragraph 2: Prior Work and the Gap (4-5 sentences)
> [Existing benchmarks for figure understanding: ChartQA, FigureQA, SciGraphQA, etc.]
> [What they cover and what they miss.]
> [Key gap: no benchmark systematically evaluates free-form scientific figure descriptions across multiple models, languages, and quality dimensions.]
> [No existing work examines model behavior under adversarial conditions (blurred elements, etc.).]

### Paragraph 3: Our Approach (4-5 sentences)
> [Introduce SciFig-Eval: what it is, its scale (250 figures, 11 models, 4 judges, 4 languages).]
> [Evaluation framework: MQM-based multi-dimensional quality assessment.]
> [What makes it different: systematic, multi-judge, multilingual, adversarial.]
> [Reference Figure 1 here.]

### Paragraph 4: Key Findings Preview (3-4 sentences)
> [Finding 1: Most surprising result -- e.g., caption bias, hallucination patterns.]
> [Finding 2: Cross-model comparison insight.]
> [Finding 3: Adversarial robustness finding.]
> [Frame as "revealing previously undocumented phenomena."]

### Paragraph 5: Contributions (numbered list, 3-4 items)
> Our contributions are as follows:
> 1. **SciFig-Eval benchmark**: [description with scale] (Section N).
> 2. **Multi-dimensional evaluation**: [MQM framework across N dimensions] (Section N).
> 3. **Systematic analysis**: [key findings across models/languages] (Section N).
> 4. **Open release**: [data, annotations, evaluation code] (Section N).

---

## 10. Sources and References

This research draws from analysis of the following ACL 2024-2025 best papers and writing guides:

- **Mission: Impossible Language Models** -- Kallini et al. (ACL 2024 Best Paper)
- **Aya Model** -- Ustun et al. (ACL 2024 Best Paper)
- **OLMo** -- Groeneveld et al. (ACL 2024 Special Topic Award)
- **HELM** -- Liang et al. (Stanford CRFM benchmark paper)
- **Tips for Writing NLP Papers** -- Vered Shwartz (widely-cited writing guide)
- **ACL Rolling Review Guidelines** -- Official reviewer form and responsible NLP checklist
- **ARR Author Checklist** -- Common submission problems
- **The Nature of NLP: Analyzing Contributions in NLP Papers** -- Meta-analysis of contribution patterns
