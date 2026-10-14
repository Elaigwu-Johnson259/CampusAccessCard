
"""Command-line interface for the campus access-card system."""

from .storage import create_request, get_request, list_requests, save_requests
from .workflow import approve_request, issue_card, return_card


def show_welcome():
    print("\n" + "=" * 55)
    print("       CAMPUS ACCESS CARD MANAGEMENT SYSTEM")
    print("=" * 55)
    print("Welcome!")
    print("Manage campus access-card requests quickly and easily.")
    print("Create, approve, issue, and track access cards.")
    print("=" * 55)


def run_menu():
    show_welcome()

    while True:
        print("\n--------------- MAIN MENU ---------------")
        print("1. Create a request  (e.g. fellow ID: F001)")
        print("2. View a request    (e.g. request ID: A001)")
        print("3. Approve a request (e.g. approver: M001)")
        print("4. Issue a card      (approved requests only)")
        print("5. Return a card     (issued cards only)")
        print("6. List all requests (view every request)")
        print("7. Save requests     (save to JSON file)")
        print("8. Quit              (exit the application)")
        print("-----------------------------------------")

        choice = input("Choose an option (1-8): ").strip()

        try:
            if choice == "1":
                print("\n--- CREATE A NEW REQUEST ---")
                print("Example card types: visitor, student, staff")

                fellow_id = input(
                    "Enter fellow ID (e.g. F001): "
                ).strip()

                card_type = input(
                    "Enter card type (visitor/student/staff): "
                ).strip().lower()

                request = create_request(fellow_id, card_type)

                print("\n[SUCCESS] Request created!")
                print(f"Request ID : {request['id']}")
                print(f"Fellow ID  : {request['fellow_id']}")
                print(f"Card type  : {request['card_type']}")
                print(f"Status     : [{request['status'].upper()}]")
                print("Keep the request ID for future operations.")

            elif choice == "2":
                print("\n--- VIEW A REQUEST ---")
                request_id = input(
                    "Enter request ID (e.g. A001): "
                ).strip()

                request = get_request(request_id)

                if request is None:
                    print(
                        f"[NOT FOUND] No request exists with ID "
                        f"{request_id}."
                    )
                    print("Example of a valid request ID: A001")
                else:
                    print("\n========== REQUEST DETAILS ==========")
                    print(f"Request ID : {request['id']}")
                    print(f"Fellow ID  : {request['fellow_id']}")
                    print(f"Card type  : {request['card_type']}")
                    print(f"Status     : [{request['status'].upper()}]")
                    print(f"Approved by: {request['approved_by']}")
                    print("=====================================")

            elif choice == "3":
                print("\n--- APPROVE A REQUEST ---")
                request_id = input(
                    "Enter request ID (e.g. A001): "
                ).strip()
                approved_by = input(
                    "Enter approver's name (e.g mr kingsley):"
                    ).strip()

                request = approve_request(request_id, approved_by)

                print(
                    f"\n[SUCCESS] Request {request['id']} "
                    "has been approved."
                )

            elif choice == "4":
                print("\n--- ISSUE A CARD ---")
                print("Note: The request must already be approved.")

                request_id = input(
                    "Enter request ID (e.g. A001): "
                ).strip()

                request = issue_card(request_id)

                print(
                    f"\n[SUCCESS] Card for request {request['id']} "
                    "has been issued."
                )

            elif choice == "5":
                print("\n--- RETURN A CARD ---")
                print("Note: The card must already have been issued.")

                request_id = input(
                    "Enter request ID (e.g. A001): "
                ).strip()

                request = return_card(request_id)

                print(
                    f"\n[SUCCESS] Card for request {request['id']} "
                    "has been returned."
                )

            elif choice == "6":
                print("\n--- ALL ACCESS-CARD REQUESTS ---")
                requests = list_requests()

                if not requests:
                    print("No requests found yet.")
                    print("Choose option 1 to create your first request.")
                else:
                    for request in requests:
                        print("\n" + "-" * 40)
                        print(f"Request ID : {request['id']}")
                        print(f"Fellow ID  : {request['fellow_id']}")
                        print(f"Card type  : {request['card_type']}")
                        print(f"Status     : [{request['status'].upper()}]")
                        print(f"Approved by: {request['approved_by']}")

                    print("\n" + "-" * 40)
                    print(f"Total requests: {len(requests)}")

            elif choice == "7":
                print("\n--- SAVE REQUESTS ---")
                save_requests()
                print("[SUCCESS] All requests saved to the JSON file.")

            elif choice == "8":
                print("\nThank you for using the Campus Access Card")
                print("Management System. Goodbye!")
                break

            else:
                print("\n[INVALID OPTION] Please choose a number from 1 to 8.")

        except (ValueError, KeyError) as error:
            print(f"\n[ERROR] {error}")

            if "card type" in str(error).lower():
                print("Please choose one of: visitor, student, staff.")
            elif "request id" in str(error).lower():
                print("Example of a valid request ID: A001")
