import json
import asyncio

import aiohttp
import async_timeout

from .errors import (FCMInvalidDataError, FCMAuthenticationError, FCMInternalPackageError,
                     FCMServerError)

__all__ = ('FCM', 'FCMMessage')

FCM_END_POINT = "https://fcm.googleapis.com/fcm/send"


class FCMMessage:
    """ Base message class. """
    # recognized options, read FCM manual for more info.
    OPTIONS = {
        'collapse_key': str,
        'time_to_live': int,
        # 'delay_while_idle': bool,
        # 'restricted_package_name': str,
        'dry_run': bool,
    }

    def __init__(self, registration_ids, data=None, message_title=None, message_body=None,
                 payload=None, **options):
        """
        Multicast message.
        :param list,str registration_ids: FCM device registration IDs.
        :param dict data: key-value pairs, payload of this message.
        :param str message_title: a title for the notification.
        :param str message_body: the message body of the alert.
        :param payload:
        :param **options: FCM options.
        """
        if not registration_ids:
            raise FCMInvalidDataError("Empty registration_ids list")
        if not isinstance(registration_ids, (list, tuple)):
            registration_ids = list(registration_ids)
        if payload is None:
            payload = {}

        if data:
            if isinstance(data, dict):
                payload['data'] = data
            else:
                raise FCMInvalidDataError("Provided data_message is in the wrong format")

        for opt, flt in self.OPTIONS.items():
            val = options.get(opt, None)
            if val is not None:
                try:
                    val = flt(val)
                except ValueError:
                    raise FCMInvalidDataError('Invalid type: %s' % opt)
            if val or isinstance(val, int):
                payload[opt] = val

        priority = options.get('priority', None)
        if priority is not None:
            payload.setdefault('android', {})
            payload['android']['priority'] = 'high' if priority else 'normal'

        if message_title is not None or message_body is not None:
            payload['notification'] = {}
            if message_title is not None:
                payload['notification']['title'] = message_title
            if message_body is not None:
                payload['notification']['body'] = message_body

        if len(registration_ids) > 1:
            payload['registration_ids'] = registration_ids
        else:
            payload['to'] = registration_ids[0]
        self.payload = payload

    @property
    def registration_ids(self):
        """Target registration ID's."""
        return self.payload.get('registration_ids') or [self.payload.get('to')]

    @property
    def data(self):
        return self.payload.get('data', None)

    @property
    def notification(self):
        return self.payload.get('notification', None)


class FCM:
    """A class for communicating with firebase."""

    def __init__(self, api_key: str):
        """
        Create new connection.
        :param str api_key: Google API key
        """
        self.api_key = api_key

    async def send(self, message: FCMMessage):
        """Send message."""
        sleep_time = 1  # 1, 2, 4, 8, 16, 32, 64, 128, 526, 1024
        while True:
            response, data = await self._do_request(FCM_END_POINT, message.payload)
            if 'Retry-After' in response.headers:
                sleep_time = int(response.headers['Retry-After'])

            else:
                if response.status == 200:
                    return self._parse_response(data)

                elif response.status == 401:
                    raise FCMAuthenticationError(
                        "There was an error authenticating the sender account")
                elif response.status == 400:
                    raise FCMInternalPackageError(data)
                else:
                    sleep_time *= 2
                    if sleep_time > 128:
                        raise FCMServerError("FCM server is temporarily unavailable")

            await asyncio.sleep(sleep_time)

    @staticmethod
    def _parse_response(data):
        response_dict = {
            'multicast_ids': [],
            'success': 0,
            'failure': 0,
            'canonical_ids': 0,
            'results': [],
            'topic_message_id': None
        }
        data = json.loads(data)
        multicast_id = data.get('multicast_id', None)
        success = data.get('success', 0)
        failure = data.get('failure', 0)
        canonical_ids = data.get('canonical_ids', 0)
        results = data.get('results', [])
        message_id = data.get('message_id', None)  # for topic messages
        if message_id:
            success = 1
        if multicast_id:
            response_dict['multicast_ids'].append(multicast_id)
        response_dict['success'] += success
        response_dict['failure'] += failure
        response_dict['canonical_ids'] += canonical_ids
        response_dict['results'].extend(results)
        response_dict['topic_message_id'] = message_id
        return response_dict

    async def _do_request(self, url, data):
        h = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + self.api_key,
        }
        with async_timeout.timeout(15):
            async with aiohttp.ClientSession(headers=h) as session:
                async with session.request('POST', url, json=data) as response:
                    data = await response.text()
                    return response, data
