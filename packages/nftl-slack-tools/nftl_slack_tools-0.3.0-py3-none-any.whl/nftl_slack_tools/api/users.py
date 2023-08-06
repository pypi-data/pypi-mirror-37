# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
from typing import Optional, Dict, Any

from nftl_slack_tools.slack_api import SlackApi, OptStr


class Users(SlackApi):
    """
    Slack API wrapper that is handling users category
    https://api.slack.com/methods#users
    """
    API_CATEGORY = "users"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def info(self, user, locale=False, token=None):
        # type: (str, bool, Optional[str]) -> Optional[Dict[str, Any]]
        """
        Gets information about the user
        more info https://api.slack.com/methods/users.info

        Args:
            user: Slack user id like UXS65F48
            locale: should response contain locale info
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or user info as :py:class:`typing.Dict`
            when success
        """
        include_locale = 0
        if locale:
            include_locale = 1
        params = {'user': user, 'include_locale': include_locale}
        return super()._call(
            method='info',
            data_key='user',
            data=params,
            default={},
            token=token,
            http_get=True
        )

    def validate_name(self, name, token=None):
        # type: (str, Optional[str]) -> Optional[bool]
        """
        Validate users name field
        This method is not documented in https://api.slack.com/methods/

        Args:
            name: name to be validated
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or boolean validity result
        """
        params = {'field': '', 'text': name}
        resp = super()._call(
            method='validateName',
            data_key='',
            data=params,
            default={},
            token=token,
            full_response
            =True,
            http_get=True
        )

        if resp:
            return resp.get('ok', False)
        return False

    def invite(self, email, firstname=None, lastname=None, channels=None,
               restricted=True, token=None):
        # type: (str, OptStr, OptStr, OptStr, bool, OptStr) -> Optional[bool]
        """
        Invite user to the workspace
        This method is not documented in https://api.slack.com/methods/

        Args:
            email: account email,
            firstname: account first name
            lastname: account last name
            channels: comma separated list of channels (id's) to be invited,
            restricted: restrict to guest that can use multiple channels
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or boolean validity result
        """
        params: Dict[str, Any] = {'email': email, 'resend': True}

        if firstname:
            params.update({'first_name': firstname})
        if lastname:
            params.update({'last_name': lastname})
        if channels:
            params.update({'channels': channels})
        if restricted:
            params.update({'restricted': restricted})

        resp = super()._call(
            method='admin.invite',
            data_key='',
            data=params,
            default={},
            token=token,
            full_response=True,
            http_get=True
        )

        if resp and resp.get('ok', False):
            return True
        return False
