#### NO ASSISTANTS, NO HARDCODED API

#!/usr/bin/env python3
"""
Generate synthetic command samples for a MITRE ATT&CK technique
using targets and constraints from a generated input file.

Usage:
  export OPENROUTER_API_KEY="your-api-key-here"
  python GenerateSamples.py path/to/TXXX_LLM_Input_Ready.txt

  ex: python GenerateCommands.py GeneratedInput/T1601_LLM_Input_Ready.txt --model openai/gpt-5
"""

import openai
import time
import json
import os
import hashlib
import argparse
import re
from datetime import datetime

def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable not set.\n"
            "Please set it using: export OPENROUTER_API_KEY='your-api-key-here'"
        )
    return api_key

def extract_technique_id(filepath: str) -> str:
    """Extract technique ID from filename."""
    basename = os.path.basename(filepath)
    match = re.search(r'(T\d+(?:\.\d+)?)', basename, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    raise ValueError(f"Could not extract technique ID from filename: {filepath}")

def load_targets_and_constraints(filepath: str) -> tuple[list, list]:
    """Load targets and constraints from the generated input file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Execute the Python code to get targets and constraints
    namespace = {}
    try:
        exec(content, namespace)
    except Exception as e:
        raise ValueError(f"Failed to execute input file: {e}")
    
    if "targets" not in namespace:
        raise ValueError("No 'targets' variable found in input file")
    if "constraints" not in namespace:
        raise ValueError("No 'constraints' variable found in input file")
    
    return namespace["targets"], namespace["constraints"]

def format_constraints(constraints: list) -> str:
    """Format constraints list into a readable string for the prompt."""
    return "\n".join(f"- {constraint}" for constraint in constraints)

def call_openrouter(prompt: str, api_key: str, model: str = "openai/gpt-4o") -> str:
    """
    Call OpenRouter API with the given prompt.
    
    Args:
        prompt: The prompt to send
        api_key: OpenRouter API key
        model: Model to use (default: openai/gpt-4o for ChatGPT-4)
    
    Returns:
        The model's response text
    """
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )
    
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(
        description="Show the prompt that would be sent to the LLM."
    )
    parser.add_argument("input_file", help="Path to the TXXX_LLM_Input_Ready.txt file")
    parser.add_argument("--technique-description", default="", 
                       help="Optional technique description (will be used if provided)")
    parser.add_argument("--model", default="openai/gpt-4o",
                       help="OpenRouter model to use (default: openai/gpt-4o)")
    args = parser.parse_args()

    # Extract technique ID from filename
    technique_id = extract_technique_id(args.input_file)
    
    # Load targets and constraints
    targets, constraints = load_targets_and_constraints(args.input_file)
    
    print(f"[*] Extracted Technique ID: {technique_id}")
    print(f"[*] Loaded {len(targets)} targets and {len(constraints)} constraints")
    print(f"[*] Model: {args.model}")
    print("\n" + "="*80)
    print("SAMPLE PROMPT (for first target):")
    print("="*80 + "\n")
    
    # Get first target to show example prompt
    target = targets[0]
    platform = target["platform"]
    privilege = target["privilege"]
    shell = target["shell"]
    tool = target["tool"]

    obfuscation_level = "heavy" if tool.endswith("-obf") else "none"
    base_tool = tool.replace("-obf", "")

    # Build the technique description line
    tech_desc_line = ""
    if args.technique_description:
        tech_desc_line = f' ("{args.technique_description}")'

    # Format constraints for prompt
    constraints_text = format_constraints(constraints)

    prompt = f"""
You are a cybersecurity expert tasked with generating synthetic but realistic malicious command-line examples.

For MITRE ATT&CK technique {technique_id}{tech_desc_line}, generate 10 unique commands aligned strictly with this behavior.

Context:
- Platform: {platform}
- Privilege Level: {privilege}
- Shell: {shell}
- Tool: {base_tool}
- Obfuscation: {"Apply base64, hex, eval, or indirect execution techniques" if obfuscation_level == "heavy" else "None"}

Output exactly 10 distinct JSON entries as a list, following this format:
{{
  "technique_id": "{technique_id}",
  "platform": "{platform}",
  "shell": "{shell}",
  "command": "...",
  "explanation": "...",
  "rationale_steps": ["...", "..."],
  "obfuscation_level": "{obfuscation_level}"
}}

Constraints:
{constraints_text}
"""

    print(prompt)
    print("\n" + "="*80)
    print(f"This prompt would be sent for target 1 of {len(targets)}")
    print("="*80)

if __name__ == "__main__":
    exit(main() or 0)
