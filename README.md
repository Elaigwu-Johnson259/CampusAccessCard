# Campus Access Card Management System

## Overview

The Campus Access Card Management System is a Python command-line application designed to manage campus access-card requests.

It allows users to create requests, view request details, approve requests, issue cards, return cards, list all requests, and save request records to a JSON file.

The system helps organize access-card records and ensures that requests follow the correct approval and issuing process.

## Features

- **Create requests:** Register a request using a fellow ID and card type.
- **View requests:** Find a request using its unique request ID.
- **Approve requests:** Record the name of the person approving a request.
- **Issue cards:** Issue cards only after the request has been approved.
- **Return cards:** Mark an issued card as returned.
- **List requests:** Display all requests currently stored in memory.
- **Save requests:** Store request records in a JSON file.
- **Input validation:** Reject invalid request IDs, unsupported card types, and empty required values.
- **Workflow validation:** Prevent invalid operations, such as issuing an unapproved request or returning a card that has not been issued.
- **Automated tests:** Use Python's `unittest` framework to test validation, storage, workflow, and CLI behavior.

## Technologies Used

- Python
- JSON for data storage
- `pathlib` for file path management
- `unittest` for automated testing
- Git and GitHub for version control and collaboration

## Supported Card Types

The system supports three card types:

- `visitor`
- `student`
- `staff`

## Request Workflow

Requests follow this sequence:

`requested → approved → issued → returned`

A request must be approved before a card can be issued. A card must be issued before it can be returned. Returned requests cannot be returned again.

## Request Record

Each request contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique request ID, such as `A001` |
| `fellow_id` | ID of the person requesting the card |
| `card_type` | Type of card requested |
| `status` | Current workflow status |
| `approved_by` | Name of the person who approved the request, or `null` before approval |

## Project Structure

```text
CampusAccessCard/
├── main.py
├── README.md
├── .gitignore
├── campus_access/
│   ├── __init__.py
│   ├── validation.py
│   ├── storage.py
│   ├── workflow.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_storage.py
│   ├── test_workflow.py
│   └── test_cli.py
├── docs/
│   ├── ai-learning-log.md
│   └── design-decisions.md
└── data/
    └── requests.json
```

The `data/requests.json` file is created when requests are saved. The `docs/` and `tests/` directories should contain the corresponding project documentation and test files.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Enter the project directory

```bash
cd CampusAccessCard
```

### 3. Run the application

```bash
python main.py
```

If your environment uses `python3`, run:

```bash
python3 main.py
```

## How to Use the Application

When the application starts, select an option from the menu.

| Option | Action |
|---|---|
| 1 | Create a request |
| 2 | View a request |
| 3 | Approve a request |
| 4 | Issue a card |
| 5 | Return a card |
| 6 | List all requests |
| 7 | Save requests |
| 8 | Quit |

### Example

To create a student access-card request:

1. Choose option `1`.
2. Enter a fellow ID, such as `F001`.
3. Enter `student` as the card type.
4. Record the generated request ID, such as `A001`.
5. Use the request ID to view, approve, issue, or return the request as permitted by its status.

## Running the Tests

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover request validation, storage operations, workflow rules, and basic CLI behavior.

## Data Persistence

Request records can be saved to `data/requests.json` using the save option. The storage module also provides a function for loading and validating saved request records.

**Note:** Automatic loading of saved requests when the application starts must be connected and verified separately.

## Project Goals

The goals of the project are to:

- Apply Python functions, dictionaries, modules, and validation.
- Implement a controlled request workflow.
- Store and retrieve records using JSON.
- Practice automated testing.
- Build a collaborative Python project using Git and GitHub.

## Current Status

The current implementation includes request validation, storage operations, approval and issuing workflows, a command-line interface, and automated tests.

Further integration and verification are needed before considering the complete application ready for release.

