
## A project built by Johnson Elaigwu Peter and Victoria Ada Abah

# Campus Access Card Management System

## Overview

The Campus Access Card Management System is a Python-based application designed to manage campus access-card requests. It helps keep track of requests, approvals, card issuance, and card returns in an organized way.

The system uses a command-line interface (CLI) that allows users to interact with the application through a menu.

## Problem Statement

Managing campus access cards manually can lead to misplaced records, duplicate entries, difficulty tracking card status, and delays in approving and issuing cards.

This application provides a structured way to create, validate, track, and store access-card requests.

## Features

- **Create Requests:** Register a new access-card request using a fellow ID and card type.
- **View Requests:** Retrieve the details of a specific request using its request ID.
- **Approve Requests:** Approve requests and record the approver's name.
- **Issue Cards:** Issue cards only after their requests have been approved.
- **Return Cards:** Record the return of cards that have been issued.
- **List Requests:** Display all recorded access-card requests.
- **Validate Inputs:** Reject invalid card types, empty fellow IDs, malformed request IDs, and invalid workflow operations.
- **Save Requests:** Store request records in JSON format.
- **Load Saved Requests:** Load previously saved requests when the application starts.

## Card Types

The system supports three card types:

- `visitor`
- `student`
- `staff`

## Request Workflow

Requests follow this sequence:

`requested → approved → issued → returned`

A card cannot be issued before approval, and a request cannot be marked as returned before the card has been issued.

## Technologies Used

- Python
- JSON for data storage
- Git and GitHub for version control
- Python `unittest` for automated testing

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
└── docs/
    ├── design-decisions.md
    └── ai-learning-log.md
```

The `data/requests.json` file is created or used at runtime to store saved requests.

## Requirements

- Python 3.10 or later recommended.
- Git, if you want to clone the repository.

## How to Run the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/Elaigwu-Johnson259/CampusAccessCard.git
   ```

2. Enter the project directory:

   ```bash
   cd CampusAccessCard
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Follow the menu instructions to create, view, approve, issue, return, and save requests.

## How to Run the Tests

Run the automated test suite from the project root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks application behaviour, including validation, request storage, and workflow operations.

## Data Storage

Requests are stored in JSON format in `data/requests.json`. This allows the application to reload saved requests when it starts again.

The data directory is local runtime data and should not be committed unless the project explicitly requires sample data to be shared.

## Team Contributions

The project is developed collaboratively using Git and GitHub.

- **Request management:** Request creation, input validation, request ID generation, lookup, and data storage.
- **Access workflow and CLI:** Request approval, card issuance, card returns, workflow enforcement, and the command-line interface.

Changes are integrated through feature branches and pull requests.

