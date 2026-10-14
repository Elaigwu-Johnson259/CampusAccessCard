"""Command-line interface for the campus access-card system."""

from .workflow import approve_request, issue_card, return_card


def run_menu():
    while True:
        print("\n===== CAMPUS ACCESS CARD MANAGEMENT SYSTEM =====")
        print("1. Create a request")
        print("2. View a request")
        print("3. Approve a request")
        print("4. Issue a card")
        print("5. Return a card")
        print("6. List all requests")
        print("7. Save requests")
        print("8. Quit")

        choice = input("Choose an option (1-8): ")

        try:
            if choice == "1":
                print("You selected Create a request.")
                print("Request creation will be connected to the storage functions.")

            elif choice == "2":
                print("You selected View a request.")
                print("Request lookup will be connected to the storage functions.")

            elif choice == "3":
                request_id = input("Enter request ID: ")
                approved_by = input("Enter approver's name: ")

                request = approve_request(request_id, approved_by)

                print(f"Request {request['id']} has been approved.")

            elif choice == "4":
                request_id = input("Enter request ID: ")

                request = issue_card(request_id)

                print(f"Request {request['id']} has been issued.")

            elif choice == "5":
                request_id = input("Enter request ID: ")

                request = return_card(request_id)

                print(f"Request {request['id']} has been returned.")

            elif choice == "6":
                print("You selected List all requests.")
                print("Request listing will be connected to the storage functions.")

            elif choice == "7":
                print("You selected Save requests.")
                print("Saving will be connected to the storage functions.")

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose a number from 1 to 8.")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")
            