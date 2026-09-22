# Lab 01: The Price of One Request
**Student:** Beknazar  
**Date:** September 2026  
**Evaluated Model:** Google Gemini 3.6 Flash  

---

## 1. Prediction vs. Measured Values (Part 1 vs. Part 2)

Before executing the measurement, we predicted the token cost ratios based on UTF-8 byte sizes and the Cyrillic 2-byte representation.

| Metric / Language | English (EN) | Russian (RU) | Kazakh (KK) |
| :--- | :---: | :---: | :---: |
| **Predicted Ratio (Input Tokens)** | 1.00x *(Baseline)* | ~1.50x | ~2.10x |
| **Measured Input Tokens** | 100 | 130 (**1.30x**) | 236 (**2.36x**) |
| **Measured Output Tokens** | 41 | 126 (**3.07x**) | 221 (**5.39x**) |
| **Total Bill Ratio (opus-5)** | 1.00x | **2.49x** | **4.40x** |

**Insight:** While the tokenizer input ratio for Kazakh is moderate (**2.36x**, closely matching our byte-level hypothesis of ~2.10x), the actual financial bill jumps to **4.40x**. This occurs because the model generated an extensive, polite explanation in Kazakh (221 output tokens) compared to a concise reply in English (41 tokens), demonstrating that bill disparity is heavily amplified by output generation length.

---

## 2. Annual Cost Table

**Volume Justification:**  
We model a customer support queue for a mid-sized regional e-commerce service handling an average volume of **2,000 support requests per day** (730,000 requests per year).

| Model | English (USD/year) | Russian (USD/year) | Kazakh (USD/year) | Added Cost for Kazakh vs. English |
| :--- | :---: | :---: | :---: | :---: |
| **haiku-4.5** | $223 | $555 | **$979** | +$756 (+339%) |
| **sonnet-5** | $445 | $1,110 | **$1,958** | +$1,513 (+339%) |
| **opus-5** | $1,113 | $2,774 | **$4,895** | +$3,782 (+339%) |
| **fable-5.1** | $2,226 | $5,548 | **$9,789** | +$7,563 (+339%) |

---

## 3. Production Model Recommendation (Kazakh Support Queue)

**Selected Model:** **`haiku-4.5`**  
**Justification (Cost & Quality):**  
For high-volume customer support in Kazakh, `haiku-4.5` is the superior production choice: it costs only **$979/year** (saving almost **$4,000/year** compared to `opus-5`), while offering minimal latency and fully sufficient natural language comprehension to triage tickets and deliver bank policy explanations.

---

## 4. Cost Reduction Lever Not Used in this Lab

> Implementing **Prompt Caching** on the static system prompt and deposit rules knowledge base, which eliminates up to 80–90% of recurring input token costs across customer inquiries.

---
\pagebreak

## AI Usage Declaration

**Tools Used:**  
- LLM Assistant (for Markdown report structuring, ratio verification, and script adaptation).
- Google Gemini 3.6 Flash API (for live token counting and multilingual text generation).

**Purpose and Extent of AI Assistance:**
1. Adapting `part2_measure.py` to the Google GenAI SDK and configuring the `gemini-3.6-flash` model.
2. Formatting measured empirical token counts into clean Markdown comparative tables.
3. Formulating the volume justification for 2,000 requests/day.

**Independent Work by the Student:**
- Setting up the local Python virtual environment, acquiring Google AI Studio credentials, and configuring secure `.env` storage.
- Executing tokenizer tests across English, Russian, and Kazakh (`part0`, `part1`, and `part2 --call`).
- Analysis of token disparity and the economic impact of output answer lengths.
- Running final annual budget simulations via `part3_cost.py` and committing deliverables to GitHub.