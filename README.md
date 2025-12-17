# ComfyUI Promptanalyzer – Forensic Node

**Forensic prompt analysis for ComfyUI. Local, deterministic, audit-ready.**

This node provides a **token-level forensic analysis** of text prompts by comparing
their embeddings against a locally loaded SDXL-compatible CLIP text encoder checkpoint.
The result is a **quantified, explainable assessment** of how much a prompt relies on
directly learned tokens versus compositional interpretation.

No cloud. No telemetry. No guesswork.

---

## Why this exists

Prompt engineering today is largely based on experience, intuition, and trial-and-error.
This node replaces parts of that uncertainty with **measurable evidence**.

It allows you to:
- Inspect how prompts are internally tokenized
- Identify composed vs. directly learned tokens
- Quantify interpretability and ambiguity
- Assess prompt risk in a reproducible way

This is **analysis**, not generation — and not training data extraction.

---

## What the node does

- Tokenizes prompts using CLIP tokenizer (ViT-L/14)
- Computes token-level cosine similarity against a reference prompt
- Supports long prompts (up to 420 tokens via chunking)
- Classifies tokens into:
  - `direct_training`
  - `composed_token`
- Calculates:
  - Prompt score
  - Composed token ratio
  - Weighted risk score
  - Risk level (Low / Medium / High)
- Outputs **structured JSON** for logging, audits, or downstream tooling

All computation runs **fully local**.

---

## Typical use cases

- Prompt optimization based on measurable signal
- AI-Act / GDPR technical documentation
- Internal model behavior analysis
- Forensic prompt reviews
- Research and explainability workflows
- Regulated or air-gapped environments

---

## Example output (excerpt)

```json
{
  "prompt_score": 0.99999999,
  "node_properties": {
    "token_count": 166,
    "composed_token_count": 126,
    "composed_ratio": 0.759,
    "risk_level": "High",
    "weighted_risk_score": 0.0000000059
  }
}
```

#Interpretation:

A high composed-token ratio indicates increasing reliance on semantic interpolation
rather than directly learned concepts.


---

#Important clarification

This node does not:

  - Reveal training data

  - Extract memorized samples

  - Claim provenance of individual tokens

  - Inspect datasets

#It performs embedding-space similarity analysis only, which is:

  - Non-reversible

  - Non-extractive

  - Aligned with current AI governance guidance


---

##Privacy & compliance

  - No personal data processed

  - No network access

  - No third-party services

  - Suitable for GDPR- and AI-Act-oriented environments

Designed for traceability, not surveillance.

---

##Requirements

- ComfyUI (local installation)

- Python ≥ 3.10

- torch

- transformers

- safetensors

---

##Status

This project is under active development.
Interfaces and metrics may evolve, but forensic principles remain stable.

Contributions, reviews, and discussions are welcome.

---

##Prompt-ToDo (symbolic example)

Because not every masterpiece prompt behaves like one.


```
TODO:
Write a long and complex prompt in your pipeline.
A masterpiece. Award-winning.
A huge load of incredibly detailed prompt soup.

Add weights like:
(prompt:1.5)

Or maybe:
(((prompt soup)))

Misspell words.
Or write nothing at all.
Maybe like:
,,,,,
or
score_9_up

Now ask yourself:
Will the text encoder interpret your {PROMPTSOUP}
—or hallucinate its meaning?

Run the analysis.
Check the result.
Adjust the tokens.

```

What this actually means (without killing the joke)

 - Complexity ≠ semantic clarity

 - Excessive weighting does not guarantee stronger grounding

 - Misspellings and invented terms increase compositional depth

 - More composed tokens → higher interpretation risk

 - Interpretation risk is now measurable

This node helps you decide what to keep, what to simplify, and
what only feels meaningful but isn’t.

---

### Workflow Example

Tipp:

Just for checking Token´s, you do not need a complete Pipeline. Just the TokenCheckpointAnalyse-Node, a StringNode (modelpath), Stringnode (Multiline) and a DisplayAny Node are working well.


<img width="3144" height="1818" alt="workflow" src="https://github.com/user-attachments/assets/94ef8496-4ea9-4c15-a8ab-1099fc114b3f" />


---


### Installation (easy)

1. Download ZIP from GitHub
2. Unzip
3. Move or copy the folder to `ComfyUI/custom_nodes`
4. Restart ComfyUI
5. Enjoy using the Node!


Developers can also use `git clone https://github.com/solongeran54/ComfyUI-Promptanalyzer-ForensicNode` inside `custom_nodes/`.



