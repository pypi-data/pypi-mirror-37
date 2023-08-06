import functools


# Subscriptions map
# Topic -> fn
subscriptions = dict()


def subscribe(topic: str):
    """Relates the topic handler to the specified topic.

    This will automatically subscribe to the topic on reconnects.

    @mqtt.subscribe('/my/topic')
    def handle_topic(client, userdata, message):
        pass
    """
    def decorator(fn):
        subscriptions[topic] = fn

        @functools.wraps(fn)
        def add_subscription(*args, **kwargs):
            return fn(*args, **kwargs)
        return add_subscription
    return decorator
