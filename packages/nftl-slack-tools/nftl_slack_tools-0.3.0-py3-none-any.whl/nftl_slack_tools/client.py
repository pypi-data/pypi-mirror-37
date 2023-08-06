# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
from typing import Optional

from nftl_slack_tools.api.channels import Channels
from nftl_slack_tools.api.chat import Chat
from nftl_slack_tools.api.groups import Groups
from nftl_slack_tools.api.signup import Signup
from nftl_slack_tools.api.users import Users


class SlackClient:
    """
    Slack API wrapper
    Partial implementation of methods that full documentation
    more info at  https://api.slack.com/methods
    """

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        self._token = slack_token
        self._slack_api_url = slack_api_url
        self._users_api: Optional[Users] = None
        self._channels_api: Optional[Channels] = None
        self._chat_api: Optional[Chat] = None
        self._groups_api: Optional[Groups] = None
        self._signup_api: Optional[Signup] = None

    def get_users_api(self) -> Users:
        """
        Provides Wrapper for methods available in Users category
        more info at https://api.slack.com/methods#users

        """
        if not self._users_api:
            self._users_api = Users(self._token, self._slack_api_url)
        return self._users_api

    def get_channels_api(self) -> Channels:
        """
        Provides Wrapper for methods available in Channels category
        more info at https://api.slack.com/methods#channels

        """
        if not self._channels_api:
            self._channels_api = Channels(self._token, self._slack_api_url)
        return self._channels_api

    def get_chat_api(self) -> Chat:
        """
        Provides Wrapper for methods available in Channels category
        more info at https://api.slack.com/methods#channels

        """
        if not self._chat_api:
            self._chat_api = Chat(self._token, self._slack_api_url)
        return self._chat_api

    def get_groups_api(self) -> Groups:
        """
        Provides Wrapper for methods available in Groups category
        more info at https://api.slack.com/methods#groups

        """
        if not self._groups_api:
            self._groups_api = Groups(self._token, self._slack_api_url)
        return self._groups_api

    def get_signup_api(self) -> Signup:
        """
        Provides Wrapper for methods available in Signup category
        This category is not documented

        """
        if not self._signup_api:
            self._signup_api = Signup(self._token, self._slack_api_url)
        return self._signup_api
