# Scripts

This directory includes all scripts used in the DART generation and evaluation pipeline.

Contents include:
- **Generation scripts** for producing ATT&CK-aligned command samples
    - GenerateScenarios.py
    - GenerateCommands.py
- **Validation tools** for syntax and semantic checks
    - SyntaxChecker.py
    - SimilarityCheck.py
- **Evaluation utilities** for multi-agent scoring and diversity filtering
    - LLMJuryFinal.py
    - SortVerdicts.py
    - CountJson.py
    - CountByShellToolPlatform.py

Each script is modular and is run independently.
