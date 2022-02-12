"""Functions for getting station"""
from data_model import Station


def get_station(departure_board) -> Station:
    name = departure_board['locationName']
    are_services_available =\
        departure_board['areServicesAvailable'] is not False
    message = get_departure_board_message(departure_board)
    return Station(name, are_services_available, message)


def get_departure_board_message(departure_board) -> str:
    messages = departure_board['nrccMessages']
    return '' if not messages else\
        '\n'.join(m['_value_1'] for m in messages['message'])
