Official Review of Submission97 by Reviewer pYWm
Official Reviewby Reviewer pYWm03 Jan 2026, 17:51 (modified: 02 Feb 2026, 18:53)Program Chairs, Area Chairs, Reviewers Submitted, Reviewer pYWm, AuthorsRevisions
Paper Summary:
The paper studies how lexical senses correlate between spoken and sign languages in German. The correspondence can have the following types:
Type 1 (one-to-many), where a single spoken word corresponds to multiple signs;
Type 2 (many-to-one), where multiple spoken words correspond to a single sign;
Type 3 (one-to-one), where a spoken word and a sign have parallel sense(s). There are also No Match cases in which no correspondence exists. The authors manually annotated words and their sign correspondence based on two linguistic resources: (i) the German Word Usage Graph (D-WUG), providing word uses, and (ii) the Digital Dictionary of German Sign Language (DW-DGS), containing signs through video recordings with unique identifier labels, German translations, and the dictionary definitions. The resulted annotations contain 1,404 word–sign ID mappings covering 32 polysemous/homonymous German words. The experiments with automated mappings were performed.
Summary Of Strengths:
The correspondences between spoken and sign languages are not well-studied.
An interesting dataset of correspondences between spoken and sign senses has been created.
Summary Of Weaknesses:
Only 32 words were considered.
A: Thank you for the feedback. This is due to a general constraint of sign language data that we acknowledge. However, it is important to note that the unit of analysis isn't really the 32 headwords. It's the 1,404 individual word-use-to-sign mappings. Each headword has many contextualized uses from the WUG sentences, and each use gets mapped to sign IDs. Although this relatively small scale when looking at just 21 words for the main analysis, the almost-balanced typology distribution on word-level (6/6/7 words T1/T2/T3) supports the idea that our work is meaningful despite the scale.
It is not well-described how annotators established correspondences between spoken and sign senses.
A: Thank you for the feedback. We will add a step-by-step description of the annotation process with (a) running example(s) to clarify.
It is not clear how so many mappings (1,404) were found, how this number was calculated: mappings for each sentence were summed up?
A: Thank you for the feedback. Each connection linking video ids to each context (word + sentence pair) was summed. The result (1,404 links) is the total connections made. It’s important to note that contexts can hold more than one link, if the given sense of the word is covered by the sense territories of multiple different signs.
It is not clear why condition "if |Vw| = 1 AND sim < τ" corresponds to Type 2.
A: Thank you for asking this. This constitutes the main difference between Type 2 and Type 3. If similarity of all meanings under a sign are above τ (0.7 in our case), then the sense territory of these meanings is also covered by the word. However, if the opposite is the case, meaning the similarity score is below τ (below 0.7) this shows that the additional meanings a sign holds might indeed not be covered by the word at hand, and one must connect these senses to other words which may score higher similarity. This naturally leads us to Type 2, where multiple words converge under a single ambiguous sign.
A created dataset was not promised to do publicly available
A: Thank you for the concern. Our data, code, and all resources are publicly available on github. For anonymity purposes, we did not mention our link here. However, for the final copy, we will add it.
Comments Suggestions And Typos:
Some explanations on the annotation process should be provided,
The authors should promise to publish the created dataset.
Reviewer Confidence: 4 = Quite sure. I tried to check the important points carefully. It’s unlikely, though conceivable, that I missed something that should affect my ratings.
Soundness: 3 = Acceptable: This study provides sufficient support for its main claims. Some minor points may need extra support or details.
Overall Assessment: 3 = Neutral: I think this paper could be accepted to the EACL 2026 SRW if the feedback gets incorporated into the camera ready version.
Ethical Concerns:
There are no concerns with this submission
Needs Ethics Review: No
Reproducibility: 4 = They could mostly reproduce the results, but there may be some variation because of sample variance or minor variations in their interpretation of the protocol or method.
Datasets: 1 = No usable datasets submitted.
Software: 1 = No usable software released.
Knowledge Of Or Educated Guess At Author Identity: No
Impact Of Knowledge Of Paper: N/A, I do not know anything about the paper from outside sources

