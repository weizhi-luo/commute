"""Functions for getting services"""
from datetime import datetime
from typing import List

from data_model import Service, ServiceStatus, Status, CallingPoint


def get_services(departure_board_with_details, calling_point_names_included)\
        -> List[Service]:
    services = departure_board_with_details['trainServices']
    return [] if not services else\
        [get_service(s, calling_point_names_included)
         for s in filter(
            lambda s: is_valid_service(s, calling_point_names_included),
            services['service'])]


def get_service(service_item_with_calling_points,
                calling_point_names_included) -> Service:
    id_ = service_item_with_calling_points['serviceID']
    status = get_service_status(service_item_with_calling_points)
    time = get_service_time(service_item_with_calling_points)
    calling_points = get_calling_points(service_item_with_calling_points,
                                        calling_point_names_included)
    service = Service(id_, status, time, calling_points)

    if service_item_with_calling_points['length']:
        service.set_length(service_item_with_calling_points['length'])
    if 'platform' in service_item_with_calling_points \
            and service_item_with_calling_points['platform']:
        service.set_platform(service_item_with_calling_points['platform'])

    return service


def get_service_status(service_item) -> ServiceStatus:
    status = get_status(service_item)
    abnormality_message = get_abnormality_message(service_item)
    return ServiceStatus(status, abnormality_message)


def get_status(service_item) -> Status:
    is_on_time = is_service_on_time(service_item)
    is_cancelled = is_service_cancelled(service_item)
    return Status.Cancelled if is_cancelled \
        else Status.OnTime if is_on_time else Status.NewTime


def is_service_on_time(service_item) -> bool:
    return service_item['etd'].casefold().strip() == 'on time'


def is_service_cancelled(service_item) -> bool:
    return True if service_item['isCancelled'] else False


def get_abnormality_message(service_item) -> str:
    messages = []
    if service_item['cancelReason']:
        messages.append(f'Cancel reason: {service_item["cancelReason"]}')
    if service_item['delayReason']:
        messages.append(f'Delay reason: {service_item["delayReason"]}')
    if service_item['adhocAlerts']:
        alerts = '\n'.join(service_item["adhocAlerts"])
        messages.append(f'Alerts:\n{alerts}')
    return '\n'.join(messages)


def get_service_time(service_item) -> datetime.time:
    scheduled_departure_time = service_item['std']
    estimated_departure_time = service_item['etd']
    return datetime.strptime(scheduled_departure_time, '%H:%M').time()\
        if estimated_departure_time.casefold().strip() == 'on time'\
        else datetime.strptime(estimated_departure_time, '%H:%M').time()


def get_calling_points(service_item_with_calling_points,
                       calling_point_names_included) -> List[CallingPoint]:
    calling_points = service_item_with_calling_points[
        'subsequentCallingPoints']['callingPointList'][0]['callingPoint']
    return list(map(
        get_calling_point,
        filter(lambda c: c['locationName'] in calling_point_names_included,
               calling_points)))


def get_calling_point(calling_point) -> CallingPoint:
    name = calling_point['locationName']
    time = get_calling_point_time(calling_point)
    is_cancelled = is_calling_point_cancelled(calling_point)
    alert = get_calling_point_alert(calling_point)
    return CallingPoint(name, time, is_cancelled, alert)


def get_calling_point_time(calling_point) -> str:
    return calling_point['at']\
        if calling_point['at']\
        else calling_point['st']\
        if calling_point['et'].casefold().strip() == 'on time'\
        else calling_point['et']


def is_calling_point_cancelled(calling_point) -> bool:
    return True if calling_point['isCancelled'] else False


def get_calling_point_alert(calling_point) -> str:
    return '' if not calling_point['adhocAlerts']\
        else '\n'.join(calling_point['adhocAlerts'])


def is_valid_service(service_item_with_calling_points,
                     calling_point_names_included) -> bool:
    service_calling_points = service_item_with_calling_points[
        'subsequentCallingPoints']['callingPointList'][0]['callingPoint']
    return any(
        filter(lambda c: c['locationName'] in calling_point_names_included,
               service_calling_points))
