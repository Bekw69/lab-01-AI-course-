# Lab 01: The Price of One Request
**Student:** Beknazar  
**Date:** September 2026  

---

## 1. Prediction vs. Measured Values (Part 1 vs. Part 2)

Before executing the measurement, we predicted the token cost ratios based on UTF-8 byte sizes and the Cyrillic 2-byte representation.

| Metric / Language | English (EN) | Russian (RU) | Kazakh (KK) |
| :--- | :---: | :---: | :---: |
| **Predicted Ratio (Input Tokens)** | 1.00x *(Baseline)* | ~1.50x | ~2.10x |
| **Measured Input Tokens** | 145 | 209 (**1.44x**) | 317 (**2.19x**) |
| **Measured Output Tokens** | 955 | 1226 | 1337 |
| **Total Bill Ratio (opus-5)** | 1.00x | **1.29x** | **1.42x** |

**Insight:** The tokenizer input prediction was very accurate (predicted 2.10x vs. measured 2.19x for Kazakh). However, the total bill ratio (1.42x) is lower than the input token ratio (2.19x) because the model generates long answers in all languages, and the higher base price of output tokens slightly dilutes the relative gap.

---

## 2. Annual Cost Table

**Volume Justification:**  
We model a customer support queue for a mid-sized regional e-commerce service handling an average volume of **2,000 support requests per day** (730,000 requests per year).

| Model | English (USD/year) | Russian (USD/year) | Kazakh (USD/year) | Added Cost for Kazakh vs. English |
| :--- | :---: | :---: | :---: | :---: |
| **haiku-4.5** | $3,592 | $4,627 | **$5,111** | +$1,519 (+42.3%) |
| **sonnet-5** | $7,183 | $9,255 | **$10,223** | +$3,040 (+42.3%) |
| **opus-5** | $17,958 | $23,137 | **$25,557** | +$7,599 (+42.3%) |
| **fable-5.1** | $35,916 | $46,275 | **$51,115** | +$15,199 (+42.3%) |

---

## 3. Production Model Recommendation (Kazakh Support Queue)

**Selected Model:** **`haiku-4.5`**  
**Justification (Cost & Quality):**  
For high-volume, real-time customer support, `haiku-4.5` offers the optimal trade-off: it costs only **$5,111/year** on Kazakh (saving over **$20,400/year** compared to `opus-5`), while delivering sub-second latency and sufficient language comprehension to resolve FAQs, query account statuses, and route tickets accurately.

---

## 4. Cost Reduction Lever Not Used in this Lab

> Implementing **Prompt Caching** on the static system prompt and knowledge base (FAQ documents), which reduces repetitive input token costs by up to 80–90% across all incoming support tickets.

---
\pagebreak

## AI Usage Declaration

**Tools Used:**  
- LLM Assistant (for editorial review, Markdown formatting, and ratio cross-verification).

**Purpose and Extent of AI Assistance:**
1. Formatting the lab findings into the requested one-page Markdown layout and markdown tables.
2. Formulating the economic justification for the 2,000 requests/day support volume.
3. Checking the arithmetic consistency between raw token costs and annual operational expenses.

**Independent Work by the Student:**
- Local Python virtual environment setup and dependency installation.
- Running offline tokenization benchmarks (`part0_tokenizers.py` and `part1_offline.py`).
- Hypothesis formulation for UTF-8 character and byte-level token fragmentation.
- Execution and analysis of annual cost calculations via `part3_cost.py`.
- Final selection of production architecture and cost-saving recommendations.