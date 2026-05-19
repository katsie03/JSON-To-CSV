#!/usr/bin/env python3
"""
JSON to CSV Converter

Usage:
    python json_to_csv.py input.json output.csv
    python json_to_csv.py input.json  # outputs to stdout
"""

import json
import csv
import sys
import argparse
from typing import Any


def flatten_json(obj: dict, parent_key: str = '', sep: str = '.') -> dict:
    """Flatten nested JSON objects into a single-level dictionary."""
    items = []
    for key, value in obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep).items())
        elif isinstance(value, list):
            # Convert lists to JSON string representation
            items.append((new_key, json.dumps(value)))
        else:
            items.append((new_key, value))
    return dict(items)


def json_to_csv(json_data: Any) -> tuple[list[str], list[dict]]:
    """Convert JSON data to CSV-ready format."""
    # Handle single object vs array of objects
    if isinstance(json_data, dict):
        records = [json_data]
    elif isinstance(json_data, list):
        records = json_data
    else:
        raise ValueError("JSON must be an object or array of objects")

    # Flatten all records and collect all unique headers
    flattened_records = []
    all_headers = set()
    
    for record in records:
        if isinstance(record, dict):
            flat = flatten_json(record)
            flattened_records.append(flat)
            all_headers.update(flat.keys())
        else:
            # Handle primitive values in array
            flattened_records.append({'value': record})
            all_headers.add('value')

    # Sort headers for consistent output
    headers = sorted(all_headers)
    
    return headers, flattened_records


def convert(input_file: str, output_file: str = None):
    """Read JSON file and write CSV output."""
    # Read JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    headers, records = json_to_csv(json_data)

    # Write CSV
    if output_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        print(f"Converted {len(records)} records to {output_file}")
    else:
        # Write to stdout
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def main():
    parser = argparse.ArgumentParser(description='Convert JSON to CSV')
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('output', nargs='?', help='Output CSV file (optional, defaults to stdout)')
    
    args = parser.parse_args()
    
    try:
        convert(args.input, args.output)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
