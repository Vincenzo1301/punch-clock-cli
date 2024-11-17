from datetime import datetime
import argparse
import json
import os

# Path to the JSON file for storing data
STORE_FILE = "store.json"


def load_store():
    """Load the data store from the JSON file."""
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def save_store(data):
    """Save the data store to the JSON file."""
    with open(STORE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_time_entry(time_type):
    """Add or update a start or end time for today's date."""
    store = load_store()

    # Get today's date and the current time
    date_str = datetime.today().strftime("%d.%m.%Y")
    time_value = datetime.now().strftime("%H:%M")

    # Ensure the date exists as a dictionary
    if date_str not in store:
        store[date_str] = {}

    # Add or update the time type (start or end)
    store[date_str][time_type] = time_value

    save_store(store)
    print(f"Added: {date_str} => {time_type}: {time_value}")


def current_work_time():
    store = load_store()

    date_str = datetime.today().strftime("%d.%m.%Y")
    if date_str not in store:
        print(f"Current work time for {date_str} is unknown.")
        return

    start_time_str = store[date_str].get("start")
    if not start_time_str:
        print(f"Start time for {date_str} is incomplete.")
        return

    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    start_datetime = datetime.combine(datetime.today(), start_time)

    current_datetime = store[date_str].get("end") if store[date_str].get("end") else datetime.now()
    if current_datetime < start_datetime:
        print(f"Current time is earlier than the start time for {date_str}.")
        return

    work_duration = current_datetime - start_datetime
    if store[date_str].get("end"):
        message = f"You worked for {date_str}: {(work_duration.seconds // 3600)}h {(work_duration.seconds // 60) % 60}m."
    else:
        message = f"Current work time for {date_str}: {(work_duration.seconds // 3600)}h {(work_duration.seconds // 60) % 60}m."

    print(message)


def list_entries():
    """List all stored entries."""
    store = load_store()
    if not store:
        print("No entries found.")
        return

    print("Stored Entries:")
    for date, times in store.items():
        print(f"  {date}:")
        for time_type, time_value in times.items():
            print(f"    {time_type}: {time_value}")


def main():
    """Main function to handle CLI commands."""
    parser = argparse.ArgumentParser(description="CLI Tool to manage time entries.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add or update a time entry")
    add_parser.add_argument("time_type", type=str, choices=["start", "end"], help="Time type: start or end")

    subparsers.add_parser("current", help="Get current work time")

    subparsers.add_parser("list", help="List all time entries")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_time_entry(args.time_type)
    elif args.command == "list":
        list_entries()
    elif args.command == "current":
        current_work_time()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
