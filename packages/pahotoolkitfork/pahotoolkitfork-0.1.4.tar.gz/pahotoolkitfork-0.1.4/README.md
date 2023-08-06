# Paho's MQTT toolkit

Welcome to Paho's MQTT Toolkit.

## For who? and why?

This toolkit if for those who have gone through the documentation of the [Paho's MQTT library and its examples](https://www.eclipse.org/paho/clients/python/) and, like me, have felt that the API is somehow off and complicated to onboard applications.

I, personally, like Paho's MQTT library and I don't wish to replace it in anyway. However, I want to write applications that in a way, are familiar to the frameworks I use, e.g., Flask or Sanic.
And therefore, abstracting the underlying implementation by using a solid configuration base with a simplified API.

### What's the base configuration?

The base configuration of this toolkit uses Paho's event loop implementation by using the `start_loop` and `stop_loop` methods and creating a single entrypoint method that accepts different configuration parameters, `start_async`.

## Simple Usage

For more examples refer to the examples directory.


```python
import time

from paho.mqtt.client import Client

from pahotoolkit import (
    init,
    start_async,
    stop_async,
    subscribe,
    json_message,
)

from my_settings import (
    HOST,
    PORT,
    USERNAME,
    PASSWORD,
    LOG_CONFIG
)


@subscribe('/temperature')
def handle_temperature(mqtt_client: Client, userdata, message):
    print(f'Got {message}')


@subscribe('/my/topic')
@json_message()  # by default, non-json messages in the topic are ignored
def listen_my_topic(payload: dict, *args, **kwargs):
    # todo: do something with the payload
    pass


@on_connect()
def client_connected(mqtt_client: Client, *args, **kwargs):
    """Publish something on_connect."""
    mqtt_client.publish('/clients', 'Paho\'s MQTT toolkit message!')


# log_config => https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
# the default MQTT Client uses the default's MQTT Client constructor
# https://github.com/eclipse/paho.mqtt.python#client-1
def main():
    client: Client = start_async(host=HOST, port=PORT,  # port default to 1883 if not given
                                 username=USERNAME, password=PASSWORD,  # optional fields
                                 initialize=False, log_config=LOG_CONFIG)  # optional fields

    init(client)  # only required if initialize=False, else by default is automatically called

    while True:
        time.sleep(1)  # or do something in this thread...


if __name__ == '__main__':
    try:
        main()
    finally:
        stop_async()
```

## Contact

Arnulfo Solis

* arnulfojr94@gmail.com
