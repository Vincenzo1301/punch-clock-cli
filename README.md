# Punch Clock CLI

Welcome to **Punch Clock CLI**, a simple yet effective command-line tool for managing your work and break times. This
tool allows you to log start and end times for your workdays and breaks, calculate your total working hours, and review
all your logged entries. Perfect for tracking your productivity!

---

## Features

- **Add Work Entries**: Log start and end times for your workday.
- **Add Break Entries**: Track the start and end times of your breaks.
- **Calculate Current Work Time**: View the total time worked so far today.
- **List All Entries**: Review all stored work and break records.
- **Persistent Storage**: Saves all data in a JSON file (`store.json`).

---

## How It Works

The tool uses a simple JSON structure for data storage. Here's an example of how your entries are saved in `store.json`:

```json
{
  "17.11.2024": {
    "start": "09:00",
    "break": [
      {
        "start": "12:00",
        "end": "12:30"
      },
      {
        "start": "14:00",
        "end": "14:30"
      }
    ],
    "end": "17:00"
  }
}
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/time-manager-cli.git
cd time-manager-cli
```

2. Ensure Python 3.6 or higher is installed.

## Usage

Run the script using the following commands:

### Add Work Entry

Log the start or end time of your workday:

```bash
python punch_clock.py start
python punch_clock.py end
```

### Add Break Entry

Log the start or end time of your break:

```bash
python punch_clock.py break
python punch_clock.py continue
```

### Calculate Current Work Time

View your total work time so far today:

```bash
python punch_clock.py current
```

### List All Entries

Review all stored entries:

```bash
python punch_clock.py list
```

### Example Output

```text
      Date Start Time End Time Break Time Work Duration
21.11.2024      09:00    17:00     0h 45m        7h 15m
22.11.2024      17:58    18:01      0h 1m         0h 2m
23.11.2024      08:00    16:00     0h 45m        7h 15m

```

## Contribution

Feel free to contribute to this project by:

- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is licensed under the MIT License.
