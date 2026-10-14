
CARD_TYPES = ("visitor", "student", "staff")

STATUSES = ("requested", "approved", "issued", "returned")


def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str):
        raise ValueError("Fellow ID must be a string.")

    if not fellow_id:
        raise ValueError("Fellow ID must not be empty.")

    if (
        len(fellow_id) != 4
        or fellow_id[0] != "F"
        or not all("0" <= char <= "9" for char in fellow_id[1:])
    ):
        raise ValueError("Fellow ID must be in the format F001.")

    return fellow_id


def validate_card_type(card_type):
    if card_type not in CARD_TYPES:
        raise ValueError("Invalid card type.")
    return card_type


def validate_request_id(request_id):
    if (
        not isinstance(request_id, str)
        or len(request_id) != 4
        or request_id[0] != "A"
        or not all(char in "0123456789" for char in request_id[1:])
    ):
        raise ValueError("Request ID must follow the format A001.")
    return request_id


def validate_approver(approved_by):
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver ID must be a non-empty string.")
    return approved_by


def validate_request_record(record):
    required = {"id", "fellow_id", "card_type", "status", "approved_by"}

    if not isinstance(record, dict) or set(record) != required:
        raise ValueError("Invalid request record fields.")

    validate_request_id(record["id"])
    validate_fellow_id(record["fellow_id"])
    validate_card_type(record["card_type"])

    if record["status"] not in STATUSES:
        raise ValueError("Invalid request status.")

    if record["status"] == "requested":
        if record["approved_by"] is not None:
            raise ValueError("A requested record cannot have an approver.")
    else:
        validate_approver(record["approved_by"])

    return record
