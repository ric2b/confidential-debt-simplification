from utils.requests.request import Request


class AcceptUOMeRequest(Request):
    """
    Accept UOMe request sent by a valid user to accept a UOMe issued to him.
    """

    request_address = 'accept-uome'

    # TODO: the client should sign the details of the uome as well, no?
    parameter_types = {
        'group_uuid': str,
        'loaner': str,
        'user': str,
        'amount': int,
        'UOMe_id': int,
    }

    format_to_sign = ['group_uuid', 'loaner', 'user', 'amount', 'UOMe_id']

    formats_to_verify = {
        "signature": format_to_sign,
    }
