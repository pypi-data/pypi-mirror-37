# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""

from nftl_slack_tools.slack_api import SlackApi, OptData, OptStr


class Signup(SlackApi):
    """
    Slack API wrapper that is handling Signup category
    This category is not documented
    """
    API_CATEGORY = "signup"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def create_user(self, code, username, passwd, locale='en_US',
                    tos='tos_oct2016', token=None):
        # type: (str, str, str, str, str, OptStr) -> OptData
        """
        Create a user with invitation code
        This method is not documented

        Args:
            code: invitation code
            username: user name that wil be used fo real and display name
            passwd: user password to be set
            locale: locale for user
            tos: TOS key to be accepted
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or user info as :py:class:`typing.Dict`
            when success
        """

        params = {
            'code': code,
            'password': passwd,
            'emailok': True,
            'real_name': username,
            'display_name': username,
            'locale': locale,
            'last_tos_acknowledged': tos
        }

        user = super()._call(
            method='createUser',
            data_key='',
            data=params,
            default=None,
            token=token,
            full_response=True,
            http_get=False
        )
        if user and all((
            user.get('ok', False),
            'user_id' in user,
            'api_token' in user
        )):
            return {
                'user_id': user['user_id'],
                'user_token': user['api_token']
            }
        return None
