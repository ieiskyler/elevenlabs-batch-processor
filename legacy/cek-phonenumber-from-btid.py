import csv
import requests
import time
import logging
import json

API_KEY = "sk_41ac27614ca2a6115b2c2625ed790451bf77d9be1c89c357"
API_BASE = "https://api.elevenlabs.io/v1/convai/batch-calling"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_batch_ids_from_csv(csv_file):
    batch_ids = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'id' in row and row['id']:
                batch_ids.append(row['id'])
    return batch_ids

def fetch_batch(batch_id):
    logger.info(f"Fetching batch {batch_id}...")
    resp = requests.get(f"{API_BASE}/{batch_id}", headers={"xi-api-key": API_KEY})
    if resp.status_code != 200:
        logger.error(f"Failed to fetch batch {batch_id}: {resp.status_code} {resp.text}")
        return None
    return resp.json()

def extract_recipients(batch_data):
    recipients = batch_data.get("recipients", [])
    for r in recipients:
        row = {
            "batch_id": batch_data.get("id"),
            "batch_name": batch_data.get("name"),
            "agent_id": batch_data.get("agent_id"),
            "agent_name": batch_data.get("agent_name"),
            "created_at_unix": batch_data.get("created_at_unix"),
            "scheduled_time_unix": batch_data.get("scheduled_time_unix"),
            "total_calls_dispatched": batch_data.get("total_calls_dispatched"),
            "total_calls_scheduled": batch_data.get("total_calls_scheduled"),
            "last_updated_at_unix": batch_data.get("last_updated_at_unix"),
            "status": batch_data.get("status"),
            "recipient_id": r.get("id"),
            "phone_number": r.get("phone_number"),
            "recipient_status": r.get("status"),
            "recipient_created_at_unix": r.get("created_at_unix"),
            "recipient_updated_at_unix": r.get("updated_at_unix"),
            "conversation_id": r.get("conversation_id"),
            "city": ""
        }
        try:
            row["city"] = r["conversation_initiation_client_data"]["dynamic_variables"].get("city", "")
        except Exception:
            pass
        yield row

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Download all batches listed in a CSV and convert recipients to a single CSV.")
    parser.add_argument("batchlist_csv", help="CSV file with batch IDs in column 'id'")
    parser.add_argument("output_csv", help="Output CSV file for all recipients")
    args = parser.parse_args()

    batch_ids = read_batch_ids_from_csv(args.batchlist_csv)
    logger.info(f"Read {len(batch_ids)} batch IDs from {args.batchlist_csv}")

    all_rows = []
    for batch_id in batch_ids:
        batch_data = fetch_batch(batch_id)
        if not batch_data:
            continue
        for row in extract_recipients(batch_data):
            all_rows.append(row)
        time.sleep(0.2)  # To avoid rate limiting

    if all_rows:
        fieldnames = list(all_rows[0].keys())
        with open(args.output_csv, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        logger.info(f"Wrote {len(all_rows)} recipient rows to {args.output_csv}")
    else:
        logger.warning("No recipient data found to write.")

if __name__ == "__main__":
    main()