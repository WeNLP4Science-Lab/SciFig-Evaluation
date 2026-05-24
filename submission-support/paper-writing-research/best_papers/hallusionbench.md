# HallusionBench: An Advanced Diagnostic Suite for Entangled Language Hallucination and Visual Illusion in Large Vision-Language Models

**Authors:** Tianrui Guan, Fuxiao Liu, Xiyang Wu, Ruiqi Xian, Zongxia Li, Xiaoyu Liu, Xijun Wang, Lichang Chen, Furong Huang, Yaser Yacoob, Dinesh Manocha, Tianyi Zhou
**Venue:** CVPR 2024 Best Paper (relevant to our multimodal figure evaluation work)
**ArXiv:** https://arxiv.org/abs/2310.14566

---

## Introduction

In recent years, Large Language Models (LLMs) have revolutionized the field of machine learning with the ability of language understanding and content generation, offering unprecedented capabilities and potentials across a multitude of applications. The integration of LLMs with computer vision systems has given rise to Large Vision-Language Models (LVLMs). These models have demonstrated profound capabilities in various applications and significantly enhance the performance in image reasoning tasks. However, the hallucination issue of LLMs is regarded as a challenging and unsolved problem, which leads to many issues when we integrate LLMs with vision techniques.

While LVLMs like GPT-4V(ision) and LLaVA-1.5 excel in various applications, they are hindered by a pronounced language bias. This bias stems from instances where knowledge priors conflict with the visual context. Similarly, models such as LLaVA-1.5 and mPLUG-Owl are prone to giving affirmative answers regardless of the actual content of questions. The distinct failure modes of different VLMs highlight the need for specific improvements. Recognizing and understanding these limitations and failure types is imperative for advancing these models and striking a delicate balance between knowledge priors and contextual understanding.

When exploring those LVLMs, we observe that their strong language bias often overshadows visual information, leading to an overreliance on language priors rather than the visual context. To study this phenomenon, we use the term "Language Hallucination," which refers to conclusions drawn without visual input. On the other hand, the vision components within the limited ability in LVLMs can give rise to "Visual Illusion", where visual inputs can be misinterpreted, leading to overconfident yet erroneous assertions by the model.

Main Contributions: Recognizing the need to comprehend why an LVLM fails and address these issues, we present HallusionBench, a carefully crafted benchmark designed to explore the complexities of image-context reasoning in depth and expose various problems with respect to current LVLMs. Our design of the visual-question (VQ) pairs, unique in format, facilitates a quantitative analysis of the models' failures, enabling a more thorough evaluation. This investigation sheds light on existing limitations and lays the groundwork for future improvements, aiming to make the next generation of LVLMs more robust, balanced, and precise. The novelties of our work include:

1. We introduce HallusionBench, the first advanced diagnostic suite tailored to systematically dissect and analyze the diverse failure modes of LVLMs. HallusionBench consists of approximately 1129 handcrafted visual question-answer (VQA) pairs, featuring 165 original images and 181 images expertly modified by human professionals. Moving beyond the traditional metrics of correctness and accuracy, our VQA pairs are thoughtfully formulated with an innovative structure. This approach enables us to quantitatively analyze specific dimensions and aspects where current models falter.

2. We evaluate 15 most recent methods on HallusionBench. Our benchmark presents formidable challenges to existing methods. Notably, the SoTA GPT-4V achieves merely a 31.42% Question Pair Accuracy, while the performance of all other methods falls below 16%.

3. We explore HallusionBench and provide an in-depth analysis of examples on which the SoTA LVLMs, such as GPT-4V and LLaVA-1.5 fail. We also provide insights on different issues that existing LVLMs are facing based on the quantitative analysis enabled by HallusionBench.

---

## Results (First Paragraphs)

We compare the performance of several models, including both closed-source models and open-sourced models. Results are given in Tables 2 and 3 and Figure 4. Additionally, we established a human expert evaluation to assess the effectiveness of text-only GPT4-assisted evaluation.

**Correctness Evaluation.** As shown in Table 2, GPT-4V outperforms all the open-sourced LVLMs by a large margin except the Hard Accuracy. Hard Accuracy measures the models' ability to understand human-edited images from HallusionBench. The poor accuracy demonstrates the challenges of our image manipulations for GPT-4V and other open-source LVLMs. In the open-sourced models, we investigate if expanding the size (0.8B to 13B) of the LLM backbone can mitigate object existence hallucination. As detailed in Table 2, there is a noticeable reduction in hallucination as the model size increases, like LLaVA-1.5 and BLIP2-T5. Among models with a size of less than 10B, InstructBLIP and mPLUG-Owl-v2 are the best-performing ones. InstructBLIP, leveraging the BLIP-2 architecture and enhanced through instruction fine-tuning across 26 diverse datasets, demonstrates that a broader and more extensive training set can substantially enhance performance.

**Yes/No Bias.** Another observation is that GPT-4V, BLIP2-T5, and mPLUG-Owl-v2 outperform Random Choice in both question pair accuracy, figure pair accuracy, and question level accuracy. Other models, such as Qwen-VL and MiniGPT4, perform even worse than Random Choice. This indicates their visual reasoning abilities are still limited. However, LLaVA-1.5 outperforms Random Choice while achieving poor results in both question pair accuracy and figure pair accuracy. We attribute this phenomenon to the fact that LLaVA-1.5 tends to answer Yes. This assumption is supported by the low Yes Percentage Difference and False Positive Ratio of LLaVA-1.5 in Yes/No Bias Test from Table 3.

---

## Conclusion

In this work, we introduce HallusionBench, the first advanced diagnostic suite to analyze the failure cases of 15 current LVLMs. HallusionBench presents significant challenges to existing LVLMs like GPT-4V(ision), by emphasizing nuanced understanding and interpretation of visual data. Moreover, our unique design of the visual-question pairs facilitates a quantitative analysis of the models' failures, enabling a more thorough evaluation. We share our observations and key insights for future studies:

1. When GPT-4V, LLaVA-1.5, and other LVLMs have prior knowledge of questions in HallusionBench, they usually suffer from Language Hallucination as they tend to prioritize their prior knowledge which leads to incorrect answers. The model should handle the trade-off between parametric memory and context.

2. When LVLMs have not had parametric memory or prior knowledge regarding the questions in HallusionBench, they can still be prone to Visual Illusion and prefer to produce wrong answers about the given figure. The visual capability of existing LVLMs is still limited.

3. GPT-4V and other LVLMs can be easily misled by simple image manipulations in HallusionBench, including image flipping, order reversing, masking, optical character editing, object editing, and color editing.

4. GPT-4V and other LVLMs are unable to capture the temporal relations of multiple images and fail to answer temporal reasoning questions in HallusionBench. The existing LVLMs lack true temporal reasoning ability.

We plan to expand this benchmark and figure out other ways to diagnose issues within LVLMs. We hope that HallusionBench can be used to identify and provide insights on the weakness of different LVLMs, to facilitate finetuning and improvement of those models based on the diagnoses.

---

## Notable Writing Observations

- Introduces novel terminology ("Language Hallucination" vs "Visual Illusion") to taxonomize failure modes
- The conclusion is structured as numbered key insights rather than prose, making takeaways scannable
- Strong use of concrete shock-value numbers: "GPT-4V achieves merely a 31.42%"
- The word "merely" does a lot of rhetorical work -- framing SOTA performance as inadequate
- Directly relevant to our work: their methodology of manipulating images (flipping, masking, editing) parallels our adversarial blur transforms
