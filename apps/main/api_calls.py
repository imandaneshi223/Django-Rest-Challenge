from .api_routes import get_route_detail_for
from .constants import API_SECRET, DEFAULT_END_DATE, DEFAULT_START_DATE
from ..utils.exceptions import InSufficientDataProvidedError, PayloadConstructionNotImplementedError
import json
import requests


def construct_payload_for_route(route_name, **kwargs):
    """
    This method return the payload required for given route name
    raises InSufficientDataProvidedError exception when all the data required for the payload are not sent by the
    calling function

    raises PayloadConstructionNotImplementedError exception when the provided route_name has no payload generation logic
    defined
    """
    if route_name == 'invoice_list_api':
        required_fields = ['from_date', 'to_date']
        for required_field in required_fields:
            if required_field not in kwargs:
                raise InSufficientDataProvidedError(required_fields, message=f'{required_field} if not provided')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        return json.dumps({
            "secret": API_SECRET,
            "date_from": f"{from_date} 00:00:00",
            "date_to": f"{to_date} 00:00:00",
            "execute_immediately": True
        })

    raise PayloadConstructionNotImplementedError(route_name)


def get_invoices(from_date=DEFAULT_START_DATE, to_date=DEFAULT_END_DATE):
    route_detail = get_route_detail_for('invoice_list_api')
    payload = construct_payload_for_route('invoice_list_api', from_date=from_date, to_date=to_date)
    url = route_detail.get('api_url')
    headers = route_detail.get('headers')
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json().get('result').get('data')
    return []
