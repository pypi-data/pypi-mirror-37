import os
import json
from  chatqhelper import debug
import paho.mqtt.client as mqtt
import uuid
from chatqhelper import exceptions


logger = debug.logger("chatqhelper.mqtt")


class MqttClient(mqtt.Client):
    def __init__(self):
        super(MqttClient, self).__init__()
        self.ignore_topics = set()
        self.is_log_request = False

    def ignore(self, topic):
        self.ignore_topics.add(topic)

    def log_request(self, is_log=True):
        self.is_log_request = is_log

    def _handle_on_message(self, message):
        try:
            if message.topic.strip() in self.ignore_topics:
                return

            payload = message.payload
            payload = payload.decode('utf-8') if isinstance(payload, bytes) else payload
            message.payload = json.loads(payload)
            if self.is_log_request:
                logger.info("request: " + message.topic.strip() + " -- " + str(message.payload))

            self._custom_call_callback_list(message)
        except Exception as e:
            self.publish_exception(e, message)

    def _custom_call_callback_list(self, message):
        """
            This method is use to replace the default behavior of _handle_on_message
            We need this class to call not one but a list of callback.
            We also do some custom variable as well. Like split topic out of message...
        """
        with self._callback_mutex:
            try:
                iterator = self._on_message_filtered.iter_match(message.topic)
            except Exception:
                logger.info("TOPIC NOT FOUND")
            else:
                for callback_dict in iterator:
                    for callback in list(callback_dict.values()):
                        with self._in_callback:
                            callback(self, message)

            if self.on_message:
                with self._in_callback:
                    self.on_message(self, message)

    def message_callback_add(self, sub, callback):
        """
            To allow multiple callback on a single topic, we need to do a few custom.
            This method will replace _on_message_filtered map from single callback map
            to a list of callback
        """
        if callback is None or sub is None:
            raise ValueError("sub and callback must both be defined.")

        callback_id = str(uuid.uuid4())
        with self._callback_mutex:
            try:
                self._on_message_filtered[sub][callback_id] = callback
            except Exception:
                self._on_message_filtered[sub] = {
                    callback_id: callback
                }

        return callback_id

    def message_callback_remove(self, callback_id_list):
        """
            Because we now allow multiple call back on a single topic. We need a way to remove it
            using a unique id that is generated during callback registration
        """
        for sub, callback_id in callback_id_list:
            with self._callback_mutex:
                try:
                    del self._on_message_filtered[sub][callback_id]
                except KeyError:  # no such subscription
                    pass

    def publish_exception(self, exception, message):
        code = getattr(exception, 'code', 500)
        logger.error(
            'exception from message: {0} {1}'.format(
                message.topic,
                str(message.payload)
            )
        )

        error = json.dumps({
            'exception': str(exception.__class__.__name__),
            'message': str(exception),
            'code': code
        })

        logger.error(error)
        debug.log_traceback(logger)
        try:
            data = message.payload
            correlation_id = data.get('correlation_id', None)
            if correlation_id is not None:
                self.publish(
                    message.topic + '/reply-to/' + str(correlation_id),
                    error
                )
            else:
                self.publish('chat/exception', error)
        except Exception:
            pass

    def reply(self, msg, data, log_response=False):
        topic = msg.topic + "/reply-to/" + str(msg.payload.get('correlation_id'))
        payload = json.dumps(data)
        if log_response:
            logger.info("reply: " + topic + " -- " + payload)

        self.publish(topic, payload)

    def setup_message_callbacks(self, *args):
        for topic, callback in args:
            self.message_callback_add(topic, callback)

    @classmethod
    def create(cls, on_connect, is_log_request=False):
        client = cls()
        client.log_request(is_log_request)
        client.on_connect = on_connect
        client.username_pw_set(
            username=os.environ.get('SOL_USERNAME', ''),
            password=os.environ.get('SOL_PASSWORD', '')
        )

        client.connect_async(
            os.environ.get('SOL_URI', ''),
            int(os.environ.get('SOL_MQTT_PORT', '0')),
            60
        )

        return client
