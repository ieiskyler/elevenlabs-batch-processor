import json
import csv

def json_to_csv(json_file, csv_file):
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract the list of recipients
    recipients = data.get("recipients", [])

    # Define CSV header fields
    fieldnames = [
        "batch_id",
        "batch_name",
        "agent_id",
        "agent_name",
        "created_at_unix",
        "scheduled_time_unix",
        "total_calls_dispatched",
        "total_calls_scheduled",
        "last_updated_at_unix",
        "status",
        "recipient_id",
        "phone_number",
        "recipient_status",
        "recipient_created_at_unix",
        "recipient_updated_at_unix",
        "conversation_id",
        "city"
    ]

    # Prepare rows for CSV
    rows = []
    for r in recipients:
        # Extract dynamic variables if present
        city = ""
        try:
            city = r["conversation_initiation_client_data"]["dynamic_variables"].get("city", "")
        except Exception:
            pass

        row = {
            "batch_id": data.get("id"),
            "batch_name": data.get("name"),
            "agent_id": data.get("agent_id"),
            "agent_name": data.get("agent_name"),
            "created_at_unix": data.get("created_at_unix"),
            "scheduled_time_unix": data.get("scheduled_time_unix"),
            "total_calls_dispatched": data.get("total_calls_dispatched"),
            "total_calls_scheduled": data.get("total_calls_scheduled"),
            "last_updated_at_unix": data.get("last_updated_at_unix"),
            "status": data.get("status"),
            "recipient_id": r.get("id"),
            "phone_number": r.get("phone_number"),
            "recipient_status": r.get("status"),
            "recipient_created_at_unix": r.get("created_at_unix"),
            "recipient_updated_at_unix": r.get("updated_at_unix"),
            "conversation_id": r.get("conversation_id"),
            "city": city
        }
        rows.append(row)

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert historybt.json to CSV.")
    parser.add_argument("input_json", help="Input JSON file (e.g. historybt.json)")
    parser.add_argument("output_csv", help="Output CSV file (e.g. historybt.csv)")
    args = parser.parse_args()

    json_to_csv(args.input_json, args.output_csv)
    print(f"Converted {args.input_json} to {args.output_csv}")