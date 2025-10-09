#!/usr/bin/env python3
"""
Sort JSON files based on their llm_verdict field.
- likely_match: Keep in place
- uncertain: Move to 'uncertain' subfolder
- likely_mismatch: Move to 'likely_mismatch' subfolder

Usage:
  python SortVerdicts.py
"""

import os
import json
import shutil

# Configuration
source_folder = "../../Desktop/SyntheticCommandGen/Data/Samples/T1601/LLM Jury/T1601_THRESH_4_4"

def sort_files_by_verdict():
    """Sort files into subfolders based on their llm_verdict."""
    
    if not os.path.exists(source_folder):
        print(f"Error: Source folder not found: {source_folder}")
        return
    
    # Create verdict subfolders if they don't exist
    uncertain_folder = os.path.join(source_folder, "uncertain")
    mismatch_folder = os.path.join(source_folder, "likely_mismatch")
    
    os.makedirs(uncertain_folder, exist_ok=True)
    os.makedirs(mismatch_folder, exist_ok=True)
    
    # Statistics
    stats = {
        "total_files": 0,
        "likely_match": 0,
        "uncertain": 0,
        "likely_mismatch": 0,
        "no_verdict": 0,
        "errors": 0
    }
    
    # Process all JSON files in the source folder
    for fname in os.listdir(source_folder):
        if not fname.endswith(".json"):
            continue
        
        filepath = os.path.join(source_folder, fname)
        
        # Skip if it's a directory
        if os.path.isdir(filepath):
            continue
        
        stats["total_files"] += 1
        
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            
            # Get the verdict
            verdict = data.get("validation", {}).get("llm_verdict")
            
            if verdict == "likely_match":
                # Keep in place
                stats["likely_match"] += 1
                print(f"[✓] {fname} - likely_match (keeping in place)")
                
            elif verdict == "uncertain":
                # Move to uncertain folder
                dest_path = os.path.join(uncertain_folder, fname)
                shutil.move(filepath, dest_path)
                stats["uncertain"] += 1
                print(f"[→] {fname} - moved to uncertain/")
                
            elif verdict == "likely_mismatch":
                # Move to likely_mismatch folder
                dest_path = os.path.join(mismatch_folder, fname)
                shutil.move(filepath, dest_path)
                stats["likely_mismatch"] += 1
                print(f"[→] {fname} - moved to likely_mismatch/")
                
            else:
                # No verdict found
                stats["no_verdict"] += 1
                print(f"[!] {fname} - no verdict found (keeping in place)")
                
        except Exception as e:
            stats["errors"] += 1
            print(f"[✗] {fname} - Error: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("SORTING SUMMARY")
    print("="*60)
    print(f"Total files processed: {stats['total_files']}")
    print(f"  likely_match (kept in place): {stats['likely_match']}")
    print(f"  uncertain (moved): {stats['uncertain']}")
    print(f"  likely_mismatch (moved): {stats['likely_mismatch']}")
    print(f"  no verdict (kept in place): {stats['no_verdict']}")
    print(f"  errors: {stats['errors']}")
    print("="*60)

if __name__ == "__main__":
    sort_files_by_verdict()