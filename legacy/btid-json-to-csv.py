"""
if __name__ == "__main__":
    print("Corkage Fee Automation Checker started.")
    # Orchestrate workflow here
"""
import json
import csv

def convert_batches_json_to_csv(json_file, csv_file):
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    batch_calls = data.get("batch_calls", [])
    if not batch_calls:
        print("No batch_calls found in the JSON file.")
        return

    # Define CSV field order
    fieldnames = [
        "id",
        "phone_number_id",
        "phone_provider",
        "name",
        "agent_id",
        "agent_name",
        "created_at_unix",
        "scheduled_time_unix",
        "total_calls_dispatched",
        "total_calls_scheduled",
        "last_updated_at_unix",
        "status"
    ]

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for batch in batch_calls:
            row = {field: batch.get(field, "") for field in fieldnames}
            writer.writerow(row)
    print(f"Converted {json_file} to {csv_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert batch_calls JSON list to CSV.")
    parser.add_argument("input_json", help="Input JSON file (e.g. batch_list.json)")
    parser.add_argument("output_csv", help="Output CSV file (e.g. batch_list.csv)")
    args = parser.parse_args()
    convert_batches_json_to_csv(args.input_json, args.output_csv)