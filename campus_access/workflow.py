"""Access-card approval, issuing, and return workflow."""

from .storage import get_request, update_request, save_requests


def approve_request(request_id, approved_by):
    request = get_request(request_id)

    if request is None:
        raise ValueError("Request not found.")

    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver name cannot be empty.")

    if request["status"] != "requested":
        raise ValueError("Only requested cards can be approved.")

    updated_request = update_request(
        request_id,
        status="approved",
        approved_by=approved_by.strip(),
    )

    save_requests()

    return updated_request


def issue_card(request_id):
    request = get_request(request_id)

    if request is None:
        raise ValueError("Request not found.")

    if request["status"] != "approved":
        raise ValueError("Only approved cards can be issued.")

    if (
        not isinstance(request["approved_by"], str)
        or not request["approved_by"].strip()
    ):
        raise ValueError("The request must have an approver before issuing.")

    updated_request = update_request(
        request_id,
        status="issued",
        approved_by=request["approved_by"],
    )

    save_requests()

    return updated_request


def return_card(request_id):
    request = get_request(request_id)

    if request is None:
        raise ValueError("Request not found.")

    if request["status"] != "issued":
        raise ValueError("Only issued cards can be returned.")

    updated_request = update_request(
        request_id,
        status="returned",
        approved_by=request["approved_by"],
    )

    save_requests()

    return updated_request
    