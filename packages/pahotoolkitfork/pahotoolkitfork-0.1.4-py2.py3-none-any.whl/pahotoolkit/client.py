"""MQTT simplified client module."""
import logging.config

from paho.mqtt.client import Client

from pahotoolkit import exc
from pahotoolkit.log import (
    LOGGING_CONFIG_DEFAULTS,
    logger,
    error_logger,
)
from pahotoolkit.subscriptions import subscriptions
from pahotoolkit.on_connect import on_connects


# singleton client
client = Client()


def start_async(host: str, port: int = 1883,
                username: str = None, password: str = None,
                initialize: bool = True,
                log_config: dict = LOGGING_CONFIG_DEFAULTS,
                mqtt_client: Client = client) -> Client:
    """Start the MQTT Client in async mode."""
    if not host:
        raise exc.InvalidMqttHost('An MQTT host is required')

    if username and password:
        mqtt_client.username_pw_set(username=username,
                                    password=password)

    if initialize:
        init(mqtt_client)

    mqtt_client.connect_async(host=host,
                              port=port)
    mqtt_client.loop_start()

    if log_config:
        logging.config.dictConfig(log_config)

    return mqtt_client


def stop_async(mqtt_client: Client = client):
    """Stops the client's loop."""
    mqtt_client.loop_stop()


def init(mqtt_client: Client = client):
    """Initializes the given Paho's MQTT Client.

    If the given MQTT client is not given then it uses the
    singleton MQTT client.
    """
    mqtt_client.on_connect = _on_connect
    mqtt_client.on_message = _on_message


def _on_connect(client: Client, userdata, flags, result_code):
    """Handle the on-connect event from paho's client."""
    if result_code == 0:
        logger.debug(exc.OK)
        hook(client)
    elif result_code == 1:
        error_logger.error(exc.CONN_INCORRECT_PROTOCOL_VER)
    elif result_code == 2:
        error_logger.error(exc.CONN_INVALID_CLIENT_ID)
    elif result_code == 3:
        error_logger.error(exc.SERVER_UNAVAILABLE)
    elif result_code == 4:
        error_logger.error(exc.INVALID_CREDENTIALS)
    elif result_code == 5:
        error_logger.error(exc.UNAUTHORIZED)
    else:
        error_logger.warning(exc.UNKNOWN)


def hook(mqtt_client: Client):
    """Hook the toolkit to Paho's MQTT Client."""
    mqtt_client.subscribe('$SYS/#')

    logger.debug('Registering annotated subscriptions')
    # register the message callback for the topics
    for topic, fn in subscriptions.items():
        mqtt_client.subscribe(topic)
        mqtt_client.message_callback_add(topic,
                                         callback=fn)

    logger.debug('Registering annotated on_connect hooks')
    # register the on_connect functions
    for fn in on_connects:
        try:
            fn(client=mqtt_client)
        except Exception as e:
            error_logger.error(f'on_connect function failed: '
                               f'{e}')


def _on_message(client: Client, userdata, msg):
    """Unhandled message handler."""
    error_logger.warning(f'Unhandled message, '
                         f'{msg.topic}: '
                         f'{msg.payload}')
