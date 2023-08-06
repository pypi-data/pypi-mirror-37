"""
This module exposes EMS Service methods
"""
from dateutil import parser
from ems_client import EMSAPI, EMSAPIException
from ems_client.models import *
from lxml import etree


class Service(EMSAPI):
    def __init__(self):
        super(Service, self).__init__({
            'wsdl': 'Service.asmx?WSDL'
        })
        self._port = 'ServiceSoap'

    @staticmethod
    def _data_from_xml(data_type, xml):
        try:
            tree = etree.fromstring(xml)
        except Exception as ex:
            raise EMSAPIException('xml: %s' % str(ex))
        data = []

        for node in tree.xpath("/%s/Data" % data_type):
            datum = {}
            for element in node.xpath("*"):
                datum[element.tag] = element.text
            data.append(datum)

        return data

    def get_api_version(self):
        xml = self._request('GetAPIVersion')
        tree = etree.fromstring(xml)
        apiversion = {}
        for element in tree.xpath("/API/APIVersion/*"):
            apiversion[element.tag] = element.text

        return apiversion

    def get_statuses(self):
        data = self._data_from_xml("Statuses", self._request(
            'GetStatuses', {}))
        statuses = []
        for item in data:
            status = Status()
            status.description = item['Description']
            status.id = int(item['ID'])
            status.status_type_id = int(item['StatusTypeID'])
            status.display_on_web = (item['DisplayOnWeb'] == 'true')
            statuses.append(status)
        return statuses

    def get_event_types(self):
        data = self._data_from_xml("EventTypes", self._request(
            'GetEventTypes', {}))
        event_types = []
        for item in data:
            event_type = EventType()
            event_type.description = item['Description']
            event_type.id = int(item['ID'])
            event_type.display_on_web = (item['DisplayOnWeb'] == 'true')
            event_types.append(event_types)
        return event_types

    def get_all_rooms(self, building_id=-1):
        data = self._data_from_xml("Rooms", self._request(
            'GetAllRooms', {
                'BuildingID': building_id,
            }))
        rooms = []
        for item in data:
            room = Room()
            room.description = item['Description']
            room.dv_building = item['Building']
            room.building_id = int(item['BuildingID'])
            room.room = item['Room']
            room.id = int(item['ID'])
            room.external_reference = item.get('ExternalReference')
            rooms.append(room)
        return rooms

    def get_buildings(self):
        data = self._data_from_xml("Buildings", self._request(
            'GetBuildings', {}))
        buildings = []
        for item in data:
            building = Building()
            building.description = item['Description']
            building.building_code = item['BuildingCode']
            building.id = int(item['ID'])
            buildings.append(building)
        return buildings

    def get_service_order_details(self, start_date, end_date):
        data = self._data_from_xml("ServiceOrderDetails", self._request(
            'GetServiceOrderDetails', {
                'StartDate': start_date,
                'EndDate': end_date,
            }))
        details = []
        for item in data:
            detail = ServiceOrderDetail()
            detail.booking_date = parser.parse(item['BookingDate']).date()
            detail.service_order_start_time = \
                parser.parse(item['ServiceOrderStartTime']).time() \
                if item.get('ServiceOrderStartTime') else None
            detail.service_order_end_time = \
                parser.parse(item['ServiceOrderEndTime']).time() \
                if item.get('ServiceOrderEndTime') else None
            detail.resource_description = item['ResourceDescription']
            detail.resource_external_reference = \
                item['ResourceExternalReference'] \
                if item['ResourceExternalReference'] is not None else ''
            detail.service_order_id = int(item['ServiceOrderID'])
            detail.booking_id = int(item['BookingID'])
            details.append(detail)
        return details

    def get_booking(self, booking_id):
        data = self._data_from_xml("Booking", self._request(
            'GetBooking', {
                'BookingID': booking_id,
            }))
        item = data.pop()
        booking = Booking()
        booking.booking_date = parser.parse(item['BookingDate']).date()
        booking.room_description = item['RoomDescription']
        booking.time_event_start = parser.parse(item['TimeEventStart']) \
            if item.get('TimeEventStart') else None
        booking.time_event_end = parser.parse(item['TimeEventEnd']) \
            if item.get('TimeEventEnd') else None
        booking.group_name = item['GroupName']
        booking.event_name = item['EventName']
        booking.reservation_id = int(item['ReservationID'])
        booking.event_type_description = item['EventTypeDescription']
        booking.id = int(item['BookingID'])
        booking.building_id = int(item['BuildingID'])
        booking.time_booking_start = \
            parser.parse(item['TimeBookingStart']) \
            if item.get('TimeBookingStart') else None
        booking.time_booking_end = parser.parse(item['TimeBookingEnd']) \
            if item.get('TimeBookingEnd') else None
        booking.building_code = item['BuildingCode']
        booking.dv_building = item['Building']
        booking.room_code = item['RoomCode']
        booking.dv_room = item['Room']
        booking.room_id = int(item['RoomID'])
        booking.status_id = int(item['StatusID'])
        booking.status_type_id = int(item['StatusTypeID'])
        return booking

    def get_bookings(self, start_date, end_date,
                     statuses=None, event_types=None):
        params = {
                'StartDate': start_date,
                'EndDate': end_date,
                'ViewComboRoomComponents': True,
            }
        if statuses is not None:
            params['Statuses'] = {'int': statuses}
        if event_types is not None:
            params['EventTypes'] = {'int': event_types}
        data = self._data_from_xml("Bookings", self._request(
            'GetBookings', params))
        bookings = []
        for item in data:
            booking = Booking()
            booking.booking_date = parser.parse(item['BookingDate']).date()
            booking.room_description = item['RoomDescription']
            booking.time_event_start = parser.parse(item['TimeEventStart']) \
                if item.get('TimeEventStart') else None
            booking.time_event_end = parser.parse(item['TimeEventEnd']) \
                if item.get('TimeEventEnd') else None
            booking.group_name = item['GroupName']
            booking.event_name = item['EventName']
            booking.reservation_id = int(item['ReservationID'])
            booking.event_type_description = item['EventTypeDescription']
            booking.id = int(item['BookingID'])
            booking.building_id = int(item['BuildingID'])
            booking.time_booking_start = \
                parser.parse(item['TimeBookingStart']) \
                if item.get('TimeBookingStart') else None
            booking.time_booking_end = parser.parse(item['TimeBookingEnd']) \
                if item.get('TimeBookingEnd') else None
            booking.building_code = item['BuildingCode']
            booking.dv_building = item['Building']
            booking.room_code = item['RoomCode']
            booking.dv_room = item['Room']
            booking.room_id = int(item['RoomID'])
            booking.status_id = int(item['StatusID'])
            booking.status_type_id = int(item['StatusTypeID'])
            booking.date_added = parser.parse(item['DateAdded'])
            booking.date_changed = parser.parse(item['DateChanged'])
            bookings.append(booking)
        return bookings
