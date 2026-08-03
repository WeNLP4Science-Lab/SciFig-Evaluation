from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "pdf" / "scifig_eval_reviewer_responses.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)


def clean(text):
    return (text.replace("A-R-I", "A-R-I")
                .replace("GPT‑", "GPT-")
                .replace("SciFig-Eval’s", "SciFig-Eval's")
                .replace("reviewer’s", "reviewer's")
                .replace("model’s", "model's")
                .replace("benchmark’s", "benchmark's")
                .replace("doesn’t", "doesn't")
                .replace("cannot", "cannot")
                .replace("–", "-")
                .replace("—", "-")
                .replace("‑", "-")
                .replace("ρ", "rho")
                .replace("α", "alpha")
                .replace("δ", "delta")
                .replace("%", "%"))


reviews = [
    {
        "id": "No6d",
        "date": "30 Jun 2026, 16:14 (modified: 08 Jul 2026, 23:59)",
        "summary": "This paper presents SCIFIG-EVAL, a benchmark for evaluating vision-language models (VLMs) on scientific figures. Built from 250 arXiv figures, it assesses models along three axes: open-ended figure descriptions, targeted reasoning questions, and behavioral stress tests that include visual perturbations, misleading captions, false-premise questions, and selective blur. The authors also propose the Admittance-Resistance-Inductance (A-R-I) framework, which characterizes whether a model admits uncertainty when evidence is missing, resists misleading context, and infers cautiously from partial visual evidence.",
        "strengths": [
            "The paper is clearly written and tackles an important general problem: VLMs may hallucinate or behave unreliably when visual evidence is incomplete or misleading.",
            "The evaluation is broad in scope, combining perception, reasoning, and behavioral probes within a single benchmark.",
            "The results surface interesting differences between models that reach similar description quality but diverge sharply in how they handle uncertainty.",
        ],
        "items": [
            ("Summary Of Weaknesses", "Most of the stress tests build on existing ideas - image perturbation, caption bias, false-premise probing, hallucination evaluation, and uncertainty acknowledgment - rather than introducing new techniques.",
             "Thank you for the feedback. We agree these categories have prior conceptual roots, which we discuss in Section 2 and will make more explicit. Our probe-level contribution lies in two design differences. (1) We apply these perturbations in matched conditions to systematically diagnose how open-ended figure descriptions change under altered visual evidence, using an MQM-adapted rubric that captures error types and severity rather than relying only on binary accuracy, BLEU, or closed-form QA metrics commonly used in prior work. (2) For uncertainty, we decompose visual evidence into inferable and non-inferable elements, operationalised through OCR-driven selective blurring of specific chart targets. This is a controlled visual-uncertainty design that, to our knowledge, prior VLM benchmarks do not implement."),
            (None, "The A-R-I framework largely renames and reorganizes known behavioral dimensions, and it is unclear whether it amounts to a substantially new evaluation method.",
             "We agree that the component behaviours have precedents, although, to our knowledge, inference under recoverable uncertainty is rarely treated as a distinct evaluation axis. Rather than aggregating existing metrics, A-R-I constructs controlled evidence conditions to evaluate model behavioural profiles based on the relationship between a query and its evidence, mapping each response to the behaviour appropriate to that condition. For example, a query about a non-existent element, often classified under uncertainty or unanswerability in prior work, maps to Resistance because the appropriate response is to reject the false premise. If the element exists but is obscured and unrecoverable, Admittance applies. If it remains recoverable from the available context, Inductance applies. These correspond to distinct operational failure modes that accuracy or a single uncertainty score can obscure. Accuracy may reward a lucky guess even when the evidence is unrecoverable, while a single uncertainty score cannot reveal the specific behavioural failure. A-R-I captures these distinctions because a model may infer and resist but fail to admit. GPT-5.2 demonstrates this profile, achieving strong Resistance (0.81) and Inductance (59%) but only 8% active Admittance."),
            (None, "The paper does not explain how often these stress conditions occur in real scientific workflows. It would be more convincing if tied to realistic cases such as OCR errors, PDF parsing failures, and low-resolution screenshots.",
             "We agree that the paper should distinguish the prevalence of these conditions from their consequences. SciFig-Eval does not estimate how frequently each failure occurs in scientific workflows. Instead, it uses controlled conditions to measure model behaviour when such evidence failures occur. We will clarify this scope and connect the probes explicitly to practical settings. Visual perturbations and selective blur represent degraded PDF rendering, OCR loss, cropping, and low-resolution inputs. Caption bias represents incorrect figure-caption retrieval in document processing or multimodal RAG. False-premise probes represent erroneous assumptions introduced by users or propagated between agents. Page-context conditions represent models processing figures within complete scientific documents. We will add this mapping to the benchmark design section."),
            (None, "The benchmark comprises only 250 figures and covers just three chart types (bar, line, and pie). This is modest for a benchmark paper, particularly given that the probe types are themselves not especially novel.",
             "We acknowledge that 250 figures and three chart types limit the benchmark's breadth, as stated in our Limitations. We emphasise three considerations. Diagnostic depth: the 250 authentic figures from 187 papers support more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 reasoning questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets. Probe-level innovations: our OCR-localised and human-confirmed selective-blur pipeline separates unrecoverable from recoverable visual evidence to measure Admittance and Inductance. Our paired in-paper ablation compares an isolated figure, the figure within its original page, and the same page with the target figure blurred, separating direct visual understanding from reliance on surrounding document context. To our knowledge, these controlled designs have not been implemented in prior scientific-figure benchmarks. Reliability within scope: split-half reliability is rho=0.979 across 100 random splits, and resistance scores converge by 100 figures with a maximum deviation of 0.02 from the full set. Broader coverage of scatter plots, heatmaps, and other scientific figures remains important future work, as already stated in our Limitations section."),
            (None, "Although the authors include some human validation, the main evaluation still relies heavily on GPT-4o as the judge. For subtle behaviors such as acknowledgment of uncertainty and resistance to misleading premises, the paper should report direct agreement between GPT-4o and humans, ideally at the item level. This is also a reproducibility concern because GPT-4o has been retired from ChatGPT, so the exact judge version and robustness to a current judge model should be clarified.",
             "Judge validation. Unlike holistic open-ended judging, our behavioural evaluation supplies the judge with the known blurred element, expected answer, false premise, and expected behaviour, and restricts its output to explicit binary or three-level labels. While engineering the judge prompts, we manually inspected output samples across models and probe types and iteratively refined the rubrics, although this was not reported as a separate agreement study. As reported in the paper, we also compared GPT-4o with humans on 120 MQM items and independently judged 344 capability items using Mistral Large 3, obtaining 87.2% item-level agreement and identical model rankings. We will extend this validation using a stratified sample across the behavioural probes and report the missing item-level agreements with human judgements.\n\nModel availability and reproducibility. We clarify that GPT-4o was retired from the ChatGPT interface, whereas our evaluation used Azure OpenAI. GPT-4o remains available through both the OpenAI API and Azure at present, although Azure has scheduled its GPT-4o versions for retirement on October 1, 2026. The paper already reports the Azure region, deployment name, API version, temperature, and seed. We agree that long-term reproducibility additionally requires the underlying model version and inference dates, which we will report alongside the released benchmark data and annotations, prompts, model outputs, and evaluation scripts. The independent Mistral Large 3 validation already tests judge dependence for the 344-item capability evaluation, while the planned stratified behavioural validation will extend this robustness check to the behavioural probes."),
            ("Comments Suggestions And Typos", "The authors should more strongly justify the real-world relevance of the proposed probes, ideally by grounding them in realistic failure cases from scientific workflows - for example, PDF parsing errors, OCR failures, low-resolution screenshots, incorrect figure-caption retrieval, or multimodal RAG pipelines.",
             "Please see our response above. We agree and will revise the benchmark design section to make these real-world correspondences explicit."),
            (None, "It would also help to position A-R-I more modestly, as a diagnostic taxonomy rather than a new evaluation paradigm.",
             "We agree that A-R-I includes a diagnostic taxonomy, but it is not limited to categorising behaviours. Please see our response above. Its taxonomy defines the behavioural axes, while the controlled evidence conditions and corresponding metrics operationalise those axes as a targeted multidimensional evaluation framework based on the relationship between a query and its evidence."),
        ],
        "meta": [
            ("Confidence", "3 = Pretty sure, but there's a chance I missed something."),
            ("Soundness", "2.5"), ("Excitement", "2 = Potentially Interesting"),
            ("Overall Assessment", "2 = Resubmit next cycle"),
            ("Ethical Concerns", "There are no concerns with this submission"),
            ("Needs Ethics Review", "No"), ("Reproducibility", "2"),
            ("Datasets", "2 = Documentary"), ("Software", "2 = Documentary"),
        ],
    },
    {
        "id": "h9tb",
        "date": "06 Jul 2026, 07:03 (modified: 08 Jul 2026, 23:59)",
        "summary": "This paper introduces SCIFIG-EVAL, a diagnostic evaluation benchmark engineered to measure the behavioral reliability of Vision-Language Models (VLMs) under conditions of visual uncertainty and misleading context when processing scientific charts. The benchmark utilizes 250 English-language scientific figures (comprising 99 bar charts, 99 line plots, and 52 pie charts) curated from 187 arXiv papers, with each entry accompanied by high-quality human-annotated expert descriptions.",
        "strengths": [
            "The benchmark pipeline features exceptionally precise data interventions. By combining automatic EasyOCR coordinate mapping with a dual-stage blurring protocol (grey-blending plus heavy Gaussian blur), the authors create distinct Admittance Blur (unrecoverable details) and Inductance Blur (inferable variables) conditions. This elegantly differentiates structured visual deduction from ungrounded data fabrication.",
            "This paper executes exhaustive validation steps to establish the neutrality of its automated metrics.",
        ],
        "items": [
            ("Summary Of Weaknesses", "Despite harvesting charts from authentic arXiv research papers, the dataset is strictly limited to three basic visualization types: bar charts, line plots, and pie charts. Modern scientific literature frequently utilizes far more complex visual assets that carry inherent ambiguity, such as scatter plots, heatmaps etc. This narrow focus limits the benchmark's claim to fully represent genuine open-world scientific figure understanding.",
             "We agree that three chart types do not fully represent the diversity of scientific figures, and we do not intend SciFig-Eval to make that claim. Our present scope prioritises diagnostic depth. The 250 authentic figures from 187 papers support more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 capability questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets. Split-half reliability is high at rho=0.979, indicating stable model rankings within this scope. Broader coverage of scatter plots, heatmaps, schematics, and other scientific figures remains important future work, as already stated in our Limitations section."),
            (None, "Section 5 notes that Inexist probes (which embed false assumptions via definite articles, e.g., asking about non-existent error bars) serve as the most potent deception vectors across all architectures due to a persistent 'must answer' bias. However, the paper fails to isolate whether this failure stems from true visual blindness or from instruction-tuning alignment that pressure the model to comply with user prompts regardless of conflicting visual data.",
             "This is a great point. This distinction is a central motivation for SciFig-Eval's staged design. We first establish visual perception quality through open-ended descriptions of clean figures, then evaluate figure-grounded reasoning, before testing behavioural resistance to misleading queries. Models generally demonstrate substantial visual perception, with MQM scores reaching 91.6, while their Inexist resistance varies substantially and is often much poorer. This variation makes general visual inability unlikely to be the sole explanation. Instead, it shows that models capable of interpreting a figure can still accept a linguistically embedded false premise. We will clarify that the Inexist results identify this perception-behaviour dissociation and are consistent with instruction-tuning or presupposition pressure, without claiming to causally identify the internal training mechanism."),
            ("Comments Suggestions And Typos", "please consistency writing the name of Llama 4",
             "Thank you for catching this. We will standardise the model name as 'Llama 4 Maverick' throughout the paper, tables, and appendices."),
        ],
        "meta": [
            ("Confidence", "3 = Pretty sure, but there's a chance I missed something."),
            ("Soundness", "3 = Acceptable"), ("Excitement", "3.5"),
            ("Overall Assessment", "3 = Findings"),
            ("Ethical Concerns", "There are no concerns with this submission"),
            ("Needs Ethics Review", "No"), ("Reproducibility", "5"),
            ("Datasets", "5 = Enabling"), ("Software", "5 = Enabling"),
        ],
    },
    {
        "id": "LhRb",
        "date": "24 Jun 2026, 06:42 (modified: 08 Jul 2026, 23:59)",
        "summary": "This paper introduces SCIFIG-EVAL, a benchmark for evaluating VLM behavior on scientific figures when visual evidence is missing or misleading. The authors propose the A-R-I framework, Admittance, Resistance, and Inductance, to test whether models admit uncertainty, resist misleading context, and infer cautiously from partial evidence.",
        "strengths": [
            "I think the value of this paper is that it does not reduce scientific figure understanding to description quality or QA accuracy. It directly studies uncertainty behavior, which is important in scientific settings. If a model answers confidently when it cannot actually see the evidence, that can be more problematic than an ordinary mistake. I also appreciate the probe-designer ablation, human agreement check, and split-half stability analysis, which make the benchmark more convincing.",
        ],
        "items": [
            ("Summary Of Weaknesses", "My main reservation is about scale and dependence on automatic evaluation. 250 figures is still limited for the broad space of scientific figures. The validation helps, but I would still have liked to see more diverse figure sources.",
             "We agree that 250 figures cannot represent the broad space of scientific figures. As stated in the Dataset section, Appendix E, and our Limitations, SciFig-Eval contains 250 English-language figures from 187 arXiv papers published between 2023 and 2025, spanning NLP, machine learning, and computational linguistics, with stratified sampling used to preserve the chart-type distribution. This sampling provides authentic and varied content within the selected scope, while naturally biasing coverage towards recent English-language computer-science research and limiting generalisation to other disciplines and figure types. Within this scope, we prioritise diagnostic depth, supporting more than 34,000 evaluations across eight models, including 1,243 transformed or page-context cases, 1,000 capability questions, 750 resistance probes, 100 caption-bias cases, and 443 confirmed selective-blur targets. As also reported, split-half reliability is rho=0.979, and resistance scores converge by 100 figures with a maximum deviation of 0.02 from the full set. Broader and more diverse scientific corpora remain important future work."),
            (None, "GPT-4o is used quite heavily in probe generation and judging. The validation helps, but I would still have liked to see broader human evaluation.",
             "We agree that broader human validation would strengthen the benchmark. GPT-4o did not design the probes without human specification or independent checks. The resistance and caption-bias pipelines use detailed human-designed criteria, constraints, and positive and negative examples. During prompt engineering, we manually inspected generated samples and iteratively refined these specifications. We will document this human-in-the-loop development process more explicitly, while distinguishing it from the independent human-agreement evaluation. As detailed in Section 3 and Appendices B.3 and F, capability questions are independently filtered by Mistral Large 3 using five quality criteria. Every selective-blur target is confirmed or replaced by a human reviewer before inclusion, as described in Appendix B.6. We further regenerated probes with Mistral Large 3 on a matched 50-figure subset, preserving model rankings, as reported in Section 4.5 and Appendix C.\n\nFor judging, Appendix C.1 reports human comparison on 120 MQM items, while Appendix C, Table 9 reports independent Mistral Large 3 judging of 344 capability items, yielding 87.2% item-level agreement and identical model rankings. We will extend this validation using a fresh stratified sample across the behavioural probes and report the missing item-level agreements with human judgements. Broader figure sources remain important future work, as discussed in our response above."),
            (None, "The A-R-I framework is useful, but I am not fully convinced that these three dimensions are sufficient to cover behavioral reliability.",
             "As stated in Section 3.4, A-R-I is not intended to be exhaustive. It provides a targeted decomposition of model behaviour based on the relationship between a query and its supporting evidence. Within the conditions studied by SciFig-Eval, Admittance applies when a target element exists but is obscured and unrecoverable from the remaining evidence. Resistance applies when the query introduces a non-existent, false, or misleading premise. Inductance applies when a target element exists and is obscured but remains recoverable from the surrounding context. These axes cover the benchmark's principal evidence conditions and are empirically separable, but we do not claim that they exhaust every possible query-evidence relationship or model behaviour. We will make this intended scope more prominent."),
            ("Comments Suggestions And Typos", "I would suggest discussing more concretely how arXiv figure sampling affects benchmark coverage.",
             "Please see our response above on dataset scale, sampling, and source diversity."),
            (None, "The paper should also discuss model version drift, especially for API models such as GPT and Gemini.",
             "We agree that version drift is an important limitation of API-based evaluation. As reported in Appendix E, we provide the model identifiers, serving backends, Azure region and API version, inference settings, and experiment period of March to May 2026. Temperature 0 and fixed sampling seeds reduce run-level variability, while our bootstrap, split-half, and scale analyses establish stability across dataset samples. These controls do not, however, prevent providers from updating the underlying model behind an API identifier. We will make this distinction explicit and additionally report the underlying model or deployment versions and exact inference dates where exposed by the providers. We will also release the original prompts and model outputs, allowing future reruns to quantify changes caused by model-version drift."),
            (None, "The A-R-I dimensions could be better justified as a necessary and relatively complete decomposition.",
             "Please see our response above on the intended scope and justification of A-R-I."),
            (None, "I did not notice major typos.", None),
        ],
        "meta": [
            ("Confidence", "4 = Quite sure"), ("Soundness", "3 = Acceptable"),
            ("Excitement", "3 = Interesting"), ("Overall Assessment", "3 = Findings"),
            ("Ethical Concerns", "There are no concerns with this submission"),
            ("Reproducibility", "3"), ("Datasets", "3 = Potentially useful"),
            ("Software", "3 = Potentially useful"),
        ],
    },
]


styles = getSampleStyleSheet()
title = ParagraphStyle("Title2", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=15,
                       leading=19, textColor=colors.HexColor("#162A46"), alignment=TA_CENTER,
                       spaceAfter=5 * mm)
subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5,
                          leading=11, textColor=colors.HexColor("#566273"), alignment=TA_CENTER,
                          spaceAfter=6 * mm)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5,
                    leading=13, textColor=colors.HexColor("#183B66"), spaceBefore=4 * mm,
                    spaceAfter=2 * mm, keepWithNext=True)
body = ParagraphStyle("Body2", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.1,
                      leading=10.8, textColor=colors.HexColor("#222831"), spaceAfter=2.1 * mm)
answer = ParagraphStyle("Answer", parent=body, fontName="Helvetica", fontSize=7.9, leading=10.7,
                        leftIndent=5 * mm, rightIndent=3 * mm, borderColor=colors.HexColor("#A9C7E8"),
                        borderWidth=0.8, borderPadding=6, backColor=colors.HexColor("#F2F7FC"),
                        textColor=colors.HexColor("#173A5E"), spaceBefore=0.8 * mm, spaceAfter=3 * mm)
meta_style = ParagraphStyle("Meta", parent=body, fontSize=7.7, leading=9.8, spaceAfter=0.8 * mm)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7DEE8"))
    canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#6D7785"))
    canvas.drawString(18 * mm, 9 * mm, "SciFig-Eval - Reviewer Response Report")
    canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=17 * mm, bottomMargin=20 * mm,
                      title="SciFig-Eval Reviewer Responses", author="SciFig-Eval Authors")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="review", frames=frame, onPage=header_footer)])

story = []
for idx, review in enumerate(reviews):
    if idx:
        story.append(PageBreak())
    story.append(Paragraph(clean(f"Official Review of Submission14568 by Reviewer {review['id']}"), title))
    story.append(Paragraph(clean(f"Official Review by Reviewer {review['id']} - {review['date']}"), subtitle))
    story.append(Paragraph("Paper Summary", h2))
    story.append(Paragraph(clean(review["summary"]), body))
    story.append(Paragraph("Summary Of Strengths", h2))
    for strength in review["strengths"]:
        story.append(Paragraph(clean(strength), body))
    last_section = None
    for section, concern, response in review["items"]:
        if section and section != last_section:
            story.append(Paragraph(clean(section), h2))
            last_section = section
        story.append(Paragraph(clean(concern), body))
        if response:
            response_html = clean(response).replace("\n\n", "<br/><br/>")
            story.append(Paragraph(f"<b>A:</b> {response_html}", answer))
    story.append(Paragraph("Review Scores And Metadata", h2))
    for label, value in review["meta"]:
        story.append(Paragraph(clean(f"<b>{label}:</b> {value}"), meta_style))

doc.build(story)
print(OUT)
