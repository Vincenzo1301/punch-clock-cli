from datetime import datetime
import argparse
import json
import os

STORE_FILE = "store.json"


def load_store():
    """
    Load the data store from the JSON file.
    Returns:
        dict: The data store, or an empty dictionary if the file doesn't exist.
    """
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r") as f:
            return json.load(f)
    else:
        return {}


def save_store(data):
    """
    Save the data store to the JSON file.
    Args:
        data (dict): The data to save.
    """
    with open(STORE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_work_entry(time_type):
    """
    Add or update a work start or end time for today's date.
    Args:
        time_type (str): Either 'start' or 'end'.
    """
    store = load_store()

    date_str = datetime.today().strftime("%d.%m.%Y")
    time_value = datetime.now().strftime("%H:%M")

    if time_type == "end" and date_str not in store:
        print(f"No start time for {date_str} defined.")
        return

    if date_str not in store:
        store[date_str] = {}

    store[date_str][time_type] = time_value

    save_store(store)
    print(f"Added: {date_str} => {time_type}: {time_value}")


def add_break_entry(time_type):
    """
    Add or update a break start or end time for today's date.
    Args:
        time_type (str): Either 'start' or 'end'.
    """
    store = load_store()

    date_str = datetime.today().strftime("%d.%m.%Y")
    time_value = datetime.now().strftime("%H:%M")

    if date_str not in store:
        print(f"No start time for {date_str} defined.")
        return

    if "break" not in store[date_str]:
        store[date_str]["break"] = {}

    if time_type == "end" and not store[date_str]["break"].get("start"):
        print(f"No break start time for {date_str} defined.")
        return

    store[date_str]["break"][time_type] = time_value

    save_store(store)
    print(f"Added break time for {date_str}: {time_type} => {time_value}")


def current_work_time():
    """
    Calculate and display the current work duration for today.
    If an end time is set, calculate based on that; otherwise, use the current time.
    """
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

    end_time_str = store[date_str].get("end")
    if end_time_str:
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
        current_datetime = datetime.combine(datetime.today(), end_time)
    else:
        current_datetime = datetime.now()

    work_duration = current_datetime - start_datetime

    if end_time_str:
        message = f"You worked on {date_str} for {(work_duration.seconds // 3600)} hours and {(work_duration.seconds // 60) % 60} minutes."
    else:
        message = f"Your current work time for {date_str} is {(work_duration.seconds // 3600)} hours and {(work_duration.seconds // 60) % 60} minutes."
    print(message)


def list_entries():
    """
    List all stored time entries from the data store.
    """
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
    """
    Main function to handle command-line interface commands.
    """
    parser = argparse.ArgumentParser(description="CLI Tool to manage time entries.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("work", help="Add or update a work time entry")
    add_parser.add_argument("time_type", type=str, choices=["start", "end"], help="Time type: start or end")

    add_parser = subparsers.add_parser("break", help="Add or update a break time entry")
    add_parser.add_argument("time_type", type=str, choices=["start", "end"], help="Time type: start or end")

    subparsers.add_parser("current", help="Get current work time")

    subparsers.add_parser("list", help="List all time entries")

    args = parser.parse_args()
    if args.command == "work":
        add_work_entry(args.time_type)
    elif args.command == "break":
        add_break_entry(args.time_type)
    elif args.command == "list":
        list_entries()
    elif args.command == "current":
        current_work_time()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
