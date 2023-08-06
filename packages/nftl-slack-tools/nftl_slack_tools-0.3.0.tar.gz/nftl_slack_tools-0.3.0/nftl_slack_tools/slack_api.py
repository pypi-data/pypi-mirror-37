# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import json
import requests
import logging as log

from abc import ABC
from typing import Any, Dict, Optional, List
from http.client import responses
from requests import Response, RequestException

STANDARD_DELAY = 1.1
SMALL_DELAY = 0.55
THROTTLING_DELAY = 5.05

OptData = Optional[Dict[str, Any]]
OptStr = Optional[str]
OptInt = Optional[int]
OptAny = Optional[Any]
ListAny = List[Any]


class SlackApi(ABC):
    """
    Slack API abstract handler

    Args:
        slack_token: Slack admin auth token for API calls
        slack_api_url: Slack API base Url
    """

    API_CATEGORY = ""

    def __init__(self, slack_token: str, slack_api_url: OptStr) -> None:
        self.slack_api_url = slack_api_url
        if not slack_api_url:
            self.slack_api_url = 'https://slack.com/api/'
        self.slack_token = slack_token

    def _get_token(self, token: OptStr) -> str:
        """
        Validate token - use provided if available or provide admins one

        Args:
            token: optional users auth token
        Returns:
            Auth token that scan be used
        """
        return token if token else self.slack_token

    @staticmethod
    def _get_data(response) -> OptData:
        """
        Universal Response validator

        Args:
            response - :py:class:`requests.Response` object to be validated
        Returns:
            None if data is invalid or Dict[str, Any] when success
        """
        if response.ok:
            data = response.json()
            if data.get('ok'):
                return response.json()
            error = data.get('error')
            if error:
                log.error(f'Slack API error {error} retrieving {response.url}')
        else:
            status = response.status_code
            name = responses[status]
            error = response.headers.get('x-amzn-errortype')
            msg = 'HTTP error (%s - %s, error: %s) retrieving: %s' % (
                status, name, error, response.url)
            log.error(msg)
        return None

    def _call(self, method: str, data_key: str, data: Dict[str, Any],
              default: Any, token: OptStr = None, http_get: bool = False,
              full_response: bool = False) -> OptAny:
        """
        Wrapper for request builder

        Args:
            method: Slack API method name
            data_key: data key from response json that should be returned
            data: request parameters
            default: object that should be returned when data key
                will not be avilable
            token: optional users auth token
        Returns:
            data structure that is available in json or None
            when error occurred
        """
        req = self._call_slack(
            f'{self.API_CATEGORY}.%s' % method,
            data,
            token,
            http_get
        )

        if req is not None:
            resp_data = self._get_data(req)
            log.debug(
                'API response for method "%s" : "%s"' % (method, req.content)
            )
            if full_response:
                return resp_data
            if resp_data:
                return resp_data.get(data_key, default)
        return None

    def _call_slack(self, method: str, data: Dict[str, Any],
                    token: OptStr = None,
                    http_get: bool = False) -> Optional[Response]:
        """
        Slack POST request builder

        Args:
            method: Slack API method name
            data: request parameters
            token: optional users auth token
        Returns:
            :py:class:`requests.Response` for provided request
        """
        url = f'{self.slack_api_url}{method}'
        msg = 'API %s "%s" with params "%s"'
        try:
            if http_get:
                log.debug(msg % ('GET', url, data))
                return requests.get(
                    url,
                    headers=self.get_headers(token),
                    params=data
                )
            log.debug(msg % ('POST', url, data))
            return requests.post(
                url,
                headers=self.get_headers(token),
                data=bytes(json.dumps(data), 'utf-8')
            )
        except RequestException as e:
            log.error(f'Error handling request "{url}" with an exception: {e}')

        return None

    def get_headers(self, token: OptStr = None):
        return {
            'Authorization': 'Bearer %s' % self._get_token(token),
            'Content-type': 'application/json; charset=utf-8'
        }
