from datetime import datetime, timedelta
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

    def add_work_start(self):
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if date_str not in self.store:
            self.store[date_str] = {}

        self.store[date_str]["start"] = time_value
        self.save_store()
        print(f"Added: {date_str} => start: {time_value}")

    def add_work_end(self):
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if date_str not in self.store or "start" not in self.store[date_str]:
            print(f"No start time for {date_str} defined. Cannot add end time.")
            return

        self.store[date_str]["end"] = time_value
        self.save_store()
        print(f"Added: {date_str} => end: {time_value}")

    def add_break_start(self):
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if date_str not in self.store or "start" not in self.store[date_str]:
            print(f"No work start time for {date_str} defined. Cannot add break start.")
            return

        if "break" not in self.store[date_str]:
            self.store[date_str]["break"] = []

        for break_entry in self.store[date_str]["break"]:
            if "start" in break_entry and "end" not in break_entry:
                print(f"An incomplete break entry already exists for {date_str}.")
                return

        # Check for incomplete break slots or create a new one
        for break_entry in self.store[date_str]["break"]:
            if "start" not in break_entry:
                break_entry["start"] = time_value
                self.save_store()
                print(f"Added break start time for {date_str}: start => {time_value}")
                return

        # If no incomplete break exists, add a new break
        new_break = {"start": time_value}
        self.store[date_str]["break"].append(new_break)
        self.save_store()
        print(f"Added new break start time for {date_str}: start => {time_value}")

    def add_break_end(self):
        date_str = datetime.today().strftime("%d.%m.%Y")
        time_value = datetime.now().strftime("%H:%M")

        if date_str not in self.store or "start" not in self.store[date_str]:
            print(f"No work start time for {date_str} defined. Cannot add break end.")
            return

        if "break" not in self.store[date_str] or not self.store[date_str]["break"]:
            print(f"No break entries found for {date_str}. Cannot add break end.")
            return

        # Find the last incomplete break
        for break_entry in reversed(self.store[date_str]["break"]):
            if "end" not in break_entry:
                break_entry["end"] = time_value
                self.save_store()
                print(f"Added break end time for {date_str}: end => {time_value}")
                return

        # If no incomplete break is found
        print(f"All breaks for {date_str} already have an end time. Cannot add break end.")

    def current_work_time(self):
        """Calculate and display the current work duration for today, excluding breaks."""
        date_str = datetime.today().strftime("%d.%m.%Y")
        if date_str not in self.store:
            print(f"Current work time for {date_str} is unknown.")
            return

        # Get start time
        start_time_str = self.store[date_str].get("start")
        if not start_time_str:
            print(f"Start time for {date_str} is incomplete.")
            return

        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        start_datetime = datetime.combine(datetime.today(), start_time)

        # Get end time or use the current time
        end_time_str = self.store[date_str].get("end")
        if end_time_str:
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            current_datetime = datetime.combine(datetime.today(), end_time)
        else:
            current_datetime = datetime.now()

        # Calculate total work duration
        work_duration = current_datetime - start_datetime

        # Subtract break durations
        break_duration = timedelta()
        if "break" in self.store[date_str]:
            for break_entry in self.store[date_str]["break"]:
                break_start_str = break_entry.get("start")
                break_end_str = break_entry.get("end")

                if break_start_str and break_end_str:
                    break_start = datetime.strptime(break_start_str, "%H:%M").time()
                    break_end = datetime.strptime(break_end_str, "%H:%M").time()
                    break_start_datetime = datetime.combine(datetime.today(), break_start)
                    break_end_datetime = datetime.combine(datetime.today(), break_end)
                    break_duration += break_end_datetime - break_start_datetime

        # Adjust work duration by subtracting break durations
        effective_work_duration = work_duration - break_duration
        hours, minutes = divmod(effective_work_duration.seconds // 60, 60)

        if end_time_str:
            print(f"You worked on {date_str} for {hours} hours and {minutes} minutes (excluding breaks).")
        else:
            print(f"Your current work time for {date_str} is {hours} hours and {minutes} minutes (excluding breaks).")

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

    subparsers.add_parser("start", help="Start work time entry")
    subparsers.add_parser("end", help="End a work time entry")

    subparsers.add_parser("break", help="Add break time entry")
    subparsers.add_parser("continue", help="Add or update a break time entry")

    subparsers.add_parser("current", help="Get current work time")
    subparsers.add_parser("list", help="List all time entries")

    args = parser.parse_args()
    if args.command == "start":
        time_manager.add_work_start()
    elif args.command == "end":
        time_manager.add_work_end()
    elif args.command == "break":
        time_manager.add_break_start()
    elif args.command == "continue":
        time_manager.add_break_end()
    elif args.command == "current":
        time_manager.current_work_time()
    elif args.command == "list":
        time_manager.list_entries()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
