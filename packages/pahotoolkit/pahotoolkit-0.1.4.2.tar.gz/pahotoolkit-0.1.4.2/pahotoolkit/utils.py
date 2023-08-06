import functools
import json

from paho.mqtt.client import MQTTMessage

from pahotoolkit.log import error_logger


def json_message(none_on_failure: bool = True, json_loader=json):
    """Json Message or nothing, maybe.

    This decorator will filter all the non-JSON
    incoming messages. If the :param none_on_failure:
    is set, it will return None, avoiding the call of
    the wrapped function.

    If set to False the function will always get called,
    but the payload argument will be always an empty
    dictionary for non-JSON messages.

    The json_loader argument allows to specify different a
    json module to use for calling the `loads` method.
    This is useful when requiring an alternative to the
    standard `json` module.

    :param none_on_failure:
    :param json_loader:
    :params args:
    :params kwargs:

    :kwarg client, userdata, message: MQTT Paho original
    arguments

    Usage:

    @json_message()
    def handle_message(payload, *args, **kwargs):
        pass
    """
    def decorator(fn):

        @functools.wraps(fn)
        def execute(client, userdata, message: MQTTMessage, *args, **kwargs):
            payload = {}
            try:
                payload = json_loader.loads(message.payload)
            except Exception as e:
                if none_on_failure:
                    err_message = 'Message was not JSON, {e}'.format(e=str(e))
                    error_logger.error(err_message)
                    return None

            return fn(client=client, userdata=userdata, message=message,
                      payload=payload, *args, **kwargs)
        return execute
    return decorator
