# ResearchOS — Evaluation & Benchmarking Framework

## 1. Metrics & Quality Dimensions

ResearchOS incorporates multi-dimensional evaluation criteria:

### 1.1 Retrieval Metrics
- **Recall@K & Precision@K**: Proportion of ground-truth relevant literature retrieved.
- **Mean Reciprocal Rank (MRR)** & **NDCG**: Quality of ranking for key evidence chunks.

### 1.2 RAG & Synthesis Quality
- **Context Relevance**: Percentage of retrieved context directly relevant to the research subtask.
- **Faithfulness**: Rate of generated statements mathematically supported by the evidence ledger.
- **Answer Relevance**: Semantic alignment between the synthesized findings and the user's research question.

### 1.3 Deep Research Metrics
- **Source Diversity**: Distribution across peer-reviewed venues, preprints, official docs, and industry benchmarks.
- **Citation Precision**: Proportion of citations linking directly to exact supporting text passages.
- **Contradiction Recall**: Rate of discovered known disagreements in contentious domain topics.
- **Research Completeness**: Percentage of planned research subquestions resolved with high confidence.
