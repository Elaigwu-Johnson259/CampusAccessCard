# Design Decisions

## 1. Project Overview

The Campus Access Card Management System is a Python application designed to manage campus access-card requests. It allows users to create requests, view request details, approve requests, issue cards, return cards, and list all requests.

## 2. Programming Language

Python was chosen because it is readable, easy to maintain, and supports modular application development.

## 3. Command-Line Interface

The application uses a command-line interface (CLI). This allows users to interact with the system through a menu in the terminal.

## 4. Request Identification

Each request has a unique ID, such as A001 or A002. This allows users to identify and retrieve individual requests.

## 5. Card Types

The system supports three card types:

- Visitor
- Student
- Staff

Validation is used to reject unsupported card types.

## 6. Request Workflow

Requests follow a controlled sequence:

Requested → Approved → Issued → Returned

A card cannot be issued before approval or returned before it has been issued. An approver must be recorded before a card can be issued.

## 7. Data Storage

Requests are stored in a JSON file so that the application can retain request information between runs. The application loads saved requests when it starts.

## 8. Validation and Error Handling

The system validates inputs such as fellow IDs, request IDs, card types, and approver information. Invalid operations should produce understandable errors rather than silently changing request records.

## 9. Automated Testing

Unit tests are used to check validation, storage, and workflow behavior. The test suite is run using:

`python -m unittest discover -s tests -v`

## 10. Possible Future Improvements

Future versions could include user authentication, a graphical interface, a database, access permissions, and more detailed activity records.