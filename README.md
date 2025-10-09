# DART: Data Augmentation of Rare ATT&CK Techniques Using LLM Agents

**DART** is a semi-automated system for generating and validating MITRE ATT&CK–grounded malicious command samples. It combines static validation, multi-agent large language model (LLM) evaluation, and diversity filtering to create balanced and representative datasets for cybersecurity research.

---

## Overview
Traditional cybersecurity datasets are often imbalanced, with well-documented attack behaviors dominating while rare or complex techniques remain underrepresented. **DART** addresses this limitation by leveraging LLMs to synthetically generate realistic command samples aligned with specific ATT&CK techniques, then validating them through syntax parsers, semantic checks, and multi-model scoring.

---

## Features
- **Scenario-driven generation** for targeted ATT&CK techniques  
- **Syntactic validation** via parsers and compilers  
- **Multi-agent evaluation** for semantic alignment and quality scoring  
- **Diversity filtering** using embedding-based cosine similarity  

---

## Results
DART demonstrates that LLM-based generation can produce operationally realistic, diverse, and semantically consistent attack commands across multiple ATT&CK categories. The system helps reduce dataset imbalance and enhances representation of underexplored adversarial behaviors.
