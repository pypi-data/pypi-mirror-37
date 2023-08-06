from __future__ import absolute_import
import json
import logging

from django.conf import settings
from django.utils.translation import get_language

from six.moves.urllib.parse import urljoin

import requests

from . import DarthMailError
from .message import EmailMultiAlternatives
from .serializers import EmailSerializer

API_BASE_URL = 'api/v1/'

logger = logging.getLogger(__name__)


class DarthMailClient(object):
    '''
    This client should only be used via the DarthMailBackend
    '''

    def __init__(self, url=None, token=None, endpoint='emailmsg/'):
        self.api_url = url or settings.EMAIL_DARTHMAIL_URL
        self.token = token or settings.EMAIL_DARTHMAIL_TOKEN
        self.endpoint_url = urljoin(API_BASE_URL, endpoint)

    def _get_headers(self, extra=dict()):
        res = {
            'Authorization': 'Token %s' % self.token,
            'Accept-Language': get_language(),
        }
        res.update(extra)
        return res

    def _post(self, obj, url=None):
        url = urljoin(urljoin(self.api_url, self.endpoint_url), url)
        if isinstance(obj, EmailMultiAlternatives):
            return requests.post(
                url,
                headers=self._get_headers(extra={'Content-Type': 'application/json'}),
                data=json.dumps(obj, cls=EmailSerializer),
            )
        return requests.post(url, headers=self._get_headers(), json=obj)

    def _get(self, url=None, **kwargs):
        url = urljoin(urljoin(self.api_url, self.endpoint_url), url)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                kwargs[k] = ['%s:%s' % (k2, v2) for k2, v2 in v.items()]
        return requests.get(url, headers=self._get_headers(), params=kwargs)

    def submit(self, msg):
        '''
        Submit message to darthmail
        '''

        if not set(msg.metadata.keys()).intersection(settings.EMAIL_DARTHMAIL_REQUIRED_METADATA_FIELDS):
            # we try to avoid sending emails that would be "invisible"
            raise DarthMailError(
                'must include one metadata field of %s' % settings.EMAIL_DARTHMAIL_REQUIRED_METADATA_FIELDS
            )

        res = _process_response(self._post(msg))
        msg.darthmail_id = res['id']  # TODO: used for syncing, can be removed when migration is done (see #104995)
        return res

    def resend(self, pk, to=None, cc=None, bcc=None, reply_to=None, from_email=None):
        '''
        Resend a given email message (identified by PK), optionally overwriting its TO, CC, BCC, REPLY TO and FROM
        fields.
        '''
        url = '%s/resend/' % pk
        overrides = dict()
        if to:
            overrides['to'] = to
        if cc:
            overrides['cc'] = cc
        if bcc:
            overrides['bcc'] = bcc
        if reply_to:
            overrides['reply_to'] = reply_to
        if from_email:
            overrides['from_email'] = from_email
        return _process_response(self._post(overrides, url=url))

    def filter(self, to=[], cc=[], bcc=[], from_email=None, metadata=dict(), any_recipient=[]):
        '''
        Search DarthMail for messages matching the provided criteria.

        All parameters will be joined by AND, including the individual items of parameters that accept lists or dicts.
        '''
        return EmailIterator(
            self,
            to=self._format_list(to),
            cc=self._format_list(cc),
            bcc=self._format_list(bcc),
            from_email=from_email,
            metadata=self._format_dict(metadata),
            any_recipient=self._format_list(any_recipient),
        )

    def _format_list(self, lst):
        return ','.join(lst)

    def _format_dict(self, dct):
        return ','.join(['%s=%s' % (k, v) for k, v in dct.items()])


class EmailIterator(object):
    def __init__(self, client, to=[], cc=[], bcc=[], from_email=None, metadata=dict(), any_recipient=[]):
        self.client = client
        self.response = _process_response(
            client._get(to=to, cc=cc, bcc=bcc, from_email=from_email, metadata=metadata, any_recipient=any_recipient)
        )

    def __len__(self):
        return self.response['count']

    def __iter__(self):
        while True:
            for msg in self.response['results']:
                yield msg
            if self.response['next']:
                self.response = _process_response(
                    requests.get(self.response['next'], headers=self.client._get_headers())
                )
                continue
            else:
                raise StopIteration()


def _process_response(response):
    try:
        response.raise_for_status()
    except Exception as e:
        logger.exception(e.response.content)
        raise DarthMailError(e)
    return response.json()
