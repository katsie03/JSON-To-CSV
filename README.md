Usage:

Features:
python json_to_csv.py data.json output.csv   # Write to file
python json_to_csv.py data.json              # Print to stdout

Handles both single JSON objects and arrays of objects
Flattens nested objects (e.g., {"user": {"name": "John"}} → user.name)
Converts nested arrays to JSON strings
Consistent column ordering
