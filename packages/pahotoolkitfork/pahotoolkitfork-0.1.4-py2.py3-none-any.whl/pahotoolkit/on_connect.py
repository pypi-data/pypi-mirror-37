import functools

from paho.mqtt.client import Client


on_connects = list()


def on_connect():
    """Excutes the function while injecting a connected MQTT client.
        This function will always be called when the client raises the
        on_connect function.

        Usage:

        @mqtt.on_connect()
        def init_publish(client, *args, **kwargs):
            client.publish('/here', 'Me!')
    """
    def decorator(fn):
        on_connects.append(fn)

        @functools.wraps(fn)
        def add_on_connect(client: Client, *args, **kwargs):
            return fn(client=client, *args, **kwargs)
        return add_on_connect
    return decorator
