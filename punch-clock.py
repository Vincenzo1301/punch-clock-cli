from datetime import datetime
import argparse
import json
import os


class TimeManager:
    """Class to manage time entries and store them in a JSON file."""

    def __init__(self, store_file="store.json"):
        self.store_file = store_file
        self.store = self.load_store()

    def load_store(self):
        """Load the data store from the JSON file."""
        if os.path.exists(self.store_file):
            with open(self.store_file, "r") as f:
                return json.load(f)
        return {}

    def save_store(self):
        """Save the data store to the JSON file."""
        with open(self.store_file, "w") as f:
            json.dump(self.store, f, indent=4)

    def add_work_entry(self, time_type):
        """Add or update a work start or end time for today's date."""
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if time_type == "end" and date_str not in self.store:
            print(f"No start time for {date_str} defined.")
            return

        if date_str not in self.store:
            self.store[date_str] = {}

        self.store[date_str][time_type] = time_value
        self.save_store()
        print(f"Added: {date_str} => {time_type}: {time_value}")

    def add_break_entry(self, time_type):
        """Add or update a break start or end time for today's date."""
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if date_str not in self.store:
            print(f"No start time for {date_str} defined.")
            return

        if "break" not in self.store[date_str]:
            self.store[date_str]["break"] = {}

        if time_type == "end" and not self.store[date_str]["break"].get("start"):
            print(f"No break start time for {date_str} defined.")
            return

        self.store[date_str]["break"][time_type] = time_value
        self.save_store()
        print(f"Added break time for {date_str}: {time_type} => {time_value}")

    def current_work_time(self):
        """Calculate and display the current work duration for today."""
        date_str = datetime.today().strftime("%d.%m.%Y")
        if date_str not in self.store:
            print(f"Current work time for {date_str} is unknown.")
            return

        start_time_str = self.store[date_str].get("start")
        if not start_time_str:
            print(f"Start time for {date_str} is incomplete.")
            return

        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        start_datetime = datetime.combine(datetime.today(), start_time)

        end_time_str = self.store[date_str].get("end")
        if end_time_str:
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            current_datetime = datetime.combine(datetime.today(), end_time)
        else:
            current_datetime = datetime.now()

        work_duration = current_datetime - start_datetime
        hours, minutes = divmod(work_duration.seconds // 60, 60)

        if end_time_str:
            print(f"You worked on {date_str} for {hours} hours and {minutes} minutes.")
        else:
            print(f"Your current work time for {date_str} is {hours} hours and {minutes} minutes.")

    def list_entries(self):
        """List all stored time entries from the data store."""
        if not self.store:
            print("No entries found.")
            return

        print("Stored Entries:")
        for date, times in self.store.items():
            print(f"  {date}:")
            for time_type, time_value in times.items():
                print(f"    {time_type}: {time_value}")


def main():
    """Main function to handle command-line interface commands."""
    time_manager = TimeManager()

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
        time_manager.add_work_entry(args.time_type)
    elif args.command == "break":
        time_manager.add_break_entry(args.time_type)
    elif args.command == "current":
        time_manager.current_work_time()
    elif args.command == "list":
        time_manager.list_entries()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
