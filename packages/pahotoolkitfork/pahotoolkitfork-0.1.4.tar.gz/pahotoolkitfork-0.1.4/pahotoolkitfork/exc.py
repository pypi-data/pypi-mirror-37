"""Exceptions."""

# on_connection code descriptions #
OK = 'MQTT client connected'

CONN_INCORRECT_PROTOCOL_VER = 'Connection refused - incorrect protocol version'

CONN_INVALID_CLIENT_ID = 'Connection refused - Invalid client identifier'

SERVER_UNAVAILABLE = 'Connection refused - Server Unavailable'

INVALID_CREDENTIALS = 'Connection refused - Bad username or password'

UNAUTHORIZED = 'Connection refused - Not Authorized'

UNKNOWN = 'Unknown connection code'


class PahoToolKitException(Exception):
    """Base Paho's Toolkit exception."""


class InvalidMqttHost(PahoToolKitException):
    """The given MQTT host is invalid."""
