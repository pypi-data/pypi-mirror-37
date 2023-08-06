# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""

from nftl_slack_tools.slack_api import SlackApi


class Chat(SlackApi):
    """
    Slack API wrapper that is handling chat category
    more info: https://api.slack.com/methods#chat
    """
    API_CATEGORY = "chat"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def postMessage(self, channel: str, text: str, token: str=None) -> bool:
        '''Post a message with the given text to the given Slack channel.
        See: https://api.slack.com/methods/chat.postMessage

        Args:
            channel: Slack channel id, eg. G99LTLXUK
            text: Message to send
            token: optional auth token that will overwrite SlackApi token
        Returns:
        '''
        params = {'channel': channel, 'text': text}
        call = super()._call(
            method='postMessage',
            data_key='ok',
            data=params,
            default=None,
            token=token
        )
        return bool(call)

    def delete(self, channel: str, ts: str, token: str = None) -> bool:
        """
        Deletes a message
        more info https://api.slack.com/methods/chat.delete

        Args:
            channel: Slack channel id like CXJSD234G
            ts: Message id
            token: optional auth token that will overwrite SlackApi token
        Returns:
            boolean operation status
        """

        params = {'channel': channel, 'ts': ts}
        call = super()._call(
            method='delete',
            data_key='channel',
            data=params,
            default=None,
            token=token,
            full_response=True
        )
        if call and len(call) > 0:
            return True
        return False
