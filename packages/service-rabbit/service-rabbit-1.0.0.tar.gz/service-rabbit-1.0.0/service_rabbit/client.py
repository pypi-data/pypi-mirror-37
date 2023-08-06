# -*- coding: utf-8 -*-
import requests
import urllib3

from service_rabbit.conf import settings

from . import models

# Suppress warnings related to the invalid SSL certificate for Rabbit API.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RabbitClient(object):
    def __init__(self):
        self.requests_base_kwargs = dict(
            verify=False,
            auth=(settings.HTTP_AUTH_USERNAME, settings.HTTP_AUTH_PASSWORD),
            timeout=settings.REQUEST_TIMEOUT,
        )

    def get_queue(self, vhost, queue):
        """
        Get info about a queue.
        $ curl -u user:pass http://inspire-prod-broker1.cern.ch:15672/api/queues/inspire/orcid_push | jq '.messages'
        """  # noqa: E501
        endpoint = 'queues/{}/{}'.format(vhost, queue)

        url = '{}/{}'.format(settings.BASE_URL, endpoint)

        response = requests.get(url, **self.requests_base_kwargs)
        return models.GetQueueResponse(response)
