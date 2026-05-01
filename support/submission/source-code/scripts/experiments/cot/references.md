# Chain-of-Thought Experiment References

## Primary Method: Compositional Chain-of-Thought (Single-Prompt Variant)

Our CoT experiment uses a single-prompt CCoT-style approach: the model first describes the visual structure of the figure (chart type, axes, data series, labels, colors, patterns), then reasons step by step to answer questions. This combines visual grounding with chain-of-thought reasoning in one call.

## Key Papers

### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou
- **Venue**: NeurIPS 2022
- **arXiv**: https://arxiv.org/abs/2201.11903
- **Contribution**: Introduced few-shot chain-of-thought prompting — providing examples with intermediate reasoning steps significantly improves LLM performance on arithmetic, commonsense, and symbolic reasoning tasks.

### Large Language Models are Zero-Shot Reasoners
- **Authors**: Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, Yusuke Iwasawa
- **Venue**: NeurIPS 2022
- **arXiv**: https://arxiv.org/abs/2205.11916
- **Contribution**: Showed that simply appending "Let's think step by step." to a prompt (zero-shot CoT) improves reasoning without any examples. Established the standard zero-shot CoT baseline.

### Compositional Chain-of-Thought Prompting for Large Multimodal Models
- **Authors**: Chancharik Mitra, Brandon Huang, Trevor Darrell, Roei Herzig
- **Venue**: CVPR 2024
- **arXiv**: https://arxiv.org/abs/2311.17076
- **GitHub**: https://github.com/chancharikmitra/CCoT
- **Contribution**: Proposed CCoT — a two-step zero-shot method where the model first generates a scene graph (objects, attributes, relationships) from the image, then uses it to answer. Improves compositional visual reasoning without fine-tuning. Our approach adapts this to a single prompt by asking the model to describe the figure structure before answering.

## Self-Reflection / Self-Refine

### Self-Refine: Iterative Refinement with Self-Feedback
- **Authors**: Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, Peter Clark
- **Venue**: NeurIPS 2023
- **arXiv**: https://arxiv.org/abs/2303.17651
- **Contribution**: Introduced iterative self-refinement where the same LLM generates, critiques, and refines its output. Our judge prompt uses a similar single-pass self-critique before finalising error verdicts.

### Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors**: Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
- **Venue**: NeurIPS 2023
- **arXiv**: https://arxiv.org/abs/2303.11366
- **Contribution**: Multi-episode reflection where agents store verbal feedback in memory for subsequent trials. Heavier than our single-pass approach but foundational to the self-reflection paradigm.

### When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs
- **Venue**: TACL 2025
- **URL**: https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713
- **Contribution**: Survey showing self-correction is most effective when initial accuracy is moderate and external verification is available — conditions that match our judge evaluation setting.
