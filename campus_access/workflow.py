"""Access-card approval, issuing, and return workflow."""

from .storage import get_request

def approve_request(request_id, approved_by):
    request = get_request(request_id)

    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver name cannot be empty.")

    if request["status"] != "requested":
        raise ValueError("Only requested cards can be approved.")

    request["approved_by"] = approved_by.strip()
    request["status"] = "approved"

    return request

def issue_card(request_id):
    request = get_request(request_id)

    if request["status"] != "approved":
        raise ValueError("Only approved cards can be issued.")

    if not request["approved_by"].strip():
        raise ValueError("The request must have an approver before issuing.")

    request["status"] = "issued"
    save_requests(DATA_FILE)

    return request

def return_card(request_id):
    request = get_request(request_id)

    if request["status"] != "issued":
        raise ValueError("Only issued cards can be returned.")

    request["status"] = "returned"
    save_requests(DATA_FILE)

    return request