# Task Helper

A lightweight desktop task manager built with Python, Tkinter, and SQLite. Tasks are stored locally on your computer.

## Features

- Create, view, edit, and delete tasks
- Store a description and optional due date
- Toggle tasks between **Pending** and **Completed**
- Persist data in a local SQLite database
- Use the database module independently of the graphical interface

## Requirements

- Python 3.10 or newer (standard library only)
- Tkinter, usually included with Python; on some Linux distributions install the OS package `python3-tk`

No third-party Python packages are required.

## Run locally

Clone the repository and enter its directory:

```bash
git clone https://github.com/Godson47/Task-Helper.git
cd Task-Helper
python app.py
```

On systems where Python 3 is invoked as `python3`, use `python3 app.py`.

The application creates `tasks.db` on first use. The database is local to the machine and is intentionally excluded from version control. To choose a different database path, set `TASK_HELPER_DB` before launching the app:

```bash
# macOS/Linux
TASK_HELPER_DB="$HOME/.task-helper/tasks.db" python app.py

# PowerShell
$env:TASK_HELPER_DB = "$HOME\.task-helper\tasks.db"
python app.py
```

Ensure the parent directory exists before using a custom database path.

## Run tests

The persistence layer has regression tests and requires no third-party test runner:

```bash
python -m unittest discover -s tests -v
```

Tests use a temporary database and do not modify your personal task data.

## Data and limitations

- This is a **desktop application**, not a web service; it is not deployed to Vercel or another web host.
- The SQLite file contains your task data. Back it up before moving or reinstalling the application.
- Do not commit `tasks.db`, Python bytecode, virtual environments, or secrets.
- Dates are currently stored as text. Enter dates consistently (recommended: `YYYY-MM-DD`).

## Project structure

```text
Task-Helper/
├── app.py              # Tkinter user interface
├── database.py         # SQLite persistence and validation
├── tests/
│   └── test_database.py
├── .gitignore
└── README.md
```

## License

See [LICENSE](LICENSE) if one is added to this repository.
