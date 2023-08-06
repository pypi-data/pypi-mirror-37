# -*- coding: utf-8 -*-


class BaseRabbitClientResponse(dict):
    exceptions = []

    def __init__(self, response):
        self.raw_response = response
        try:
            data = response.json()
        except ValueError:
            data = dict(content=response.content)
        super(BaseRabbitClientResponse, self).__init__(data)

    @property
    def ok(self):
        return self.raw_response.ok

    @property
    def status_code(self):
        return self.raw_response.status_code

    @property
    def request(self):
        return self.raw_response.request

    def raise_for_result(self):
        """
        Raise one of the known exceptions (in self.exceptions) depending on the
        matching criteria; or raise requests.exceptions.HTTPError.
        In case of no errors no exception is raised.
        """
        for exception_class in self.exceptions:
            if exception_class.match(self):
                exception_object = exception_class(str(self))
                exception_object.raw_response = self.raw_response
                raise exception_object
        # Can raise requests.exceptions.HTTPError.
        return self.raw_response.raise_for_status()


class GetQueueResponse(BaseRabbitClientResponse):
    """
    A dict-like object as:
    {
      "message_stats": {
        "ack": 3812581,
        "ack_details": {
          "rate": 16.6
        },
        "deliver": 3813111,
        "deliver_details": {
          "rate": 16.6
        },
        "deliver_get": 3813111,
        "deliver_get_details": {
          "rate": 16.6
        },
        "publish": 3556812,
        "publish_details": {
          "rate": 0.2
        },
        "redeliver": 500,
        "redeliver_details": {
          "rate": 0
        }
      },
      "messages": 163418,
      "messages_details": {
        "rate": -17.4
      },
      "messages_ready": 163378,
      "messages_ready_details": {
        "rate": -17.4
      },
      "messages_unacknowledged": 40,
      "messages_unacknowledged_details": {
        "rate": 0
      },
      "policy": "",
      "exclusive_consumer_tag": "",
      "consumers": 5,
      "consumer_utilisation": 0.002352723800195745,
      "memory": 635743304,
      "backing_queue_status": {
        "q1": 0,
        "q2": 0,
        "delta": [
          "delta",
          "undefined",
          0,
          "undefined"
        ],
        "q3": 0,
        "q4": 163378,
        "len": 163378,
        "pending_acks": 40,
        "target_ram_count": "infinity",
        "ram_msg_count": 163378,
        "ram_ack_count": 40,
        "next_seq_id": 35653069,
        "persistent_count": 163418,
        "avg_ingress_rate": 1.4113838756734183,
        "avg_egress_rate": 16.06359392257519,
        "avg_ack_ingress_rate": 16.06359392257519,
        "avg_ack_egress_rate": 16.06359392257519
      },
      "state": "running",
      "incoming": [
        {
          "stats": {
            "publish": 3556812,
            "publish_details": {
              "rate": 0.2
            }
          },
          "exchange": {
            "name": "",
            "vhost": "inspire"
          }
        }
      ],
      "deliveries": [
        {
          "stats": {
            "deliver_get": 13706,
            "deliver_get_details": {
              "rate": 2.8
            },
            "deliver": 13706,
            "deliver_details": {
              "rate": 2.8
            },
            "ack": 13698,
            "ack_details": {
              "rate": 2.8
            }
          },
          "channel_details": {
            "name": "137.138.152.255:54568 -> 188.184.65.84:5672 (1)",
            "number": 1,
            "connection_name": "137.138.152.255:54568 -> 188.184.65.84:5672",
            "peer_port": 54568,
            "peer_host": "137.138.152.255"
          }
        },
        ...
      ],
      "consumer_details": [
        {
          "channel_details": {
            "name": "188.184.95.208:58324 -> 188.184.65.84:5672 (1)",
            "number": 1,
            "connection_name": "188.184.95.208:58324 -> 188.184.65.84:5672",
            "peer_port": 58324,
            "peer_host": "188.184.95.208"
          },
          "queue": {
            "name": "orcid_push",
            "vhost": "inspire"
          },
          "consumer_tag": "None7",
          "exclusive": false,
          "ack_required": true,
          "prefetch_count": 0,
          "arguments": {}
        },
        ...
      ],
      "name": "orcid_push",
      "vhost": "inspire",
      "durable": true,
      "auto_delete": false,
      "arguments": {},
      "node": "rabbit@inspire-prod-broker1"
    }
    """  # noqa: E501

    def get_messages_count(self):
        return self.get('messages')

    def get_consumers_count(self):
        return self.get('consumers')
