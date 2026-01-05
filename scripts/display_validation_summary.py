#!/usr/bin/env python3
"""
Helper script to display validation summary from JSON log file.

Usage: python scripts/display_validation_summary.py <json_file>
"""

import json
import sys

def display_summary(json_file):
    """Display a summary of the validation results."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"Total operations: {data['total_operations']}")
        print(f"Time range: {data['start_time']} to {data['end_time']}")
        
        return 0
    except FileNotFoundError:
        print(f"ERROR: File not found: {json_file}")
        return 1
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in file: {json_file}")
        return 1
    except KeyError as e:
        print(f"ERROR: Missing expected key in JSON: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python display_validation_summary.py <json_file>")
        sys.exit(1)
    
    sys.exit(display_summary(sys.argv[1]))
