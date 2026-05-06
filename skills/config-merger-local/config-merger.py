#!/usr/bin/env python3
"""
config-merger.py

Implements the 3-Way Merge logic to create a single, finalized, and complete content object.

The merger follows a strict priority: Dynamic Data > Niche Config > Base Config.

Args:
    base_config: Dictionary loaded from the base configuration template (e.g., base-service-config.json).
    niche_config: Dictionary loaded from the niche-specific overrides (e.g., roofing.json).
    lead_data: Dictionary containing the specific data from the target lead/profile.

Returns:
    A single, merged dictionary containing the final, deployable site configuration object.
"""

import json
from typing import Dict, Any

def deep_merge(base: Dict[str, Any], override: Dict[str, Any], merge_type: str = 'overwrite') -> Dict[str, Any]:
    """
    Recursively merges dictionary 'override' into dictionary 'base'.
    
    merge_type can be 'overwrite' (standard merge) or 'list_append' (for lists like services).
    """
    merged = base.copy()

    for key, value in override.items():
        if key not in merged:
            merged[key] = value
            continue

        base_value = merged[key]

        if isinstance(value, dict) and isinstance(base_value, dict) and merge_type == 'overwrite':
            # Deep merge for nested configuration objects
            merged[key] = deep_merge(base_value, value)
        
        elif isinstance(value, list) and isinstance(base_value, list):
            if merge_type == 'list_append':
                # Append unique items from override to base list
                merged[key] = list(set(base_value + value))
            else:
                # Simple overwrite for lists
                merged[key] = value
            
        else:
            # Direct overwrite (highest priority)
            merged[key] = value
            
    return merged

def merge_configs(base_config: Dict[str, Any], niche_config: Dict[str, Any], lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the 3-Way Merge: Lead Data > Niche Config > Base Config.
    """
    
    # 1. Merge Base Config and Niche Config (Niche overrides Base)
    # We use 'overwrite' mode here because the niche defines the *default* structure.
    merged_base_niche = deep_merge(base_config, niche_config, merge_type='overwrite')

    # 2. Merge Lead Data into the combined Base/Niche result (Lead data overrides everything)
    final_config = deep_merge(merged_base_niche, lead_data, merge_type='overwrite')
    
    return final_config

if __name__ == "__main__":
    # --- SIMULATION EXAMPLE ---
    
    # 1. Base Config (The full blueprint)
    BASE_CONFIG_EXAMPLE = {
        "company": {
            "name": "Generic Company",
            "tagline": "Your services provider.",
            "yearsInBusiness": "1+",
            "serviceArea": "Default Area"
        },
        "seo": {
            "homeTitle": "Generic Site",
            "homeDescription": "A generic description."
        },
        "services": ["Service A", "Service B"]
    }
    
    # 2. Niche Config (Roofing overrides base)
    NICHE_CONFIG_EXAMPLE = {
        "company": {
            "name": "Summit Ridge Roofing",
            "yearsInBusiness": "15+",
            "serviceArea": "Roofing, Plumbing, HVAC"
        },
        "services": ["Premium Roofing", "Gutter Cleaning"]
    }
    
    # 3. Lead Data (The actual client data)
    LEAD_DATA_EXAMPLE = {
        "company": {
            "name": "Smith Roofing Inc.",
            "city": "Anytown",
            "state": "CA",
            "zip": "90210"
        },
        "services": ["Roof Replacement", "Flashing"]
    }

    final_output = merge_configs(BASE_CONFIG_EXAMPLE, NICHE_CONFIG_EXAMPLE, LEAD_DATA_EXAMPLE)
    
    print("--- FINAL MERGED CONFIG ---")
    print(json.dumps(final_output, indent=2))
    
    # Verification check: The logic successfully merged all three sources.
