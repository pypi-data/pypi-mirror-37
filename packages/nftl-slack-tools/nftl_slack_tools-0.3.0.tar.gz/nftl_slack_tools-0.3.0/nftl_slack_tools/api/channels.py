# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import logging as log
from time import sleep
from typing import List, Dict, Any, Tuple

from nftl_slack_tools.api.chat import Chat
from nftl_slack_tools.slack_api import SlackApi, STANDARD_DELAY, \
    THROTTLING_DELAY, SMALL_DELAY, OptStr, OptData, OptInt, ListAny


class Channels(SlackApi):
    """
    Slack API wrapper that is handling channels category
    more info https://api.slack.com/methods#channels
    """
    API_CATEGORY = "channels"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def list(self, limit=1000, cursor=None, token=None):
        # type: (OptInt,OptStr,OptStr) -> OptData
        """
        Lists all channels in a Slack team.
        Channels depends on token so if you want to list users use user token
        instead of SlackApi admin token
        more info https://api.slack.com/methods/channels.list

        Args:
            limit: optional page length ( default: 1000 )
            cursor: optional message list cursor for pagination
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channels :py:class:`typing.Dict`
            with two keys: channels (list of channels) and cursor for pagination
            when success
        """
        data: Dict[str, Any] = {'limit': limit}
        if cursor:
            data.update({'cursor': cursor})

        response = super()._call(
            method='list',
            data_key='',
            data=data,
            default={},
            token=token,
            http_get=True,
            full_response=True
        )

        if not response or len(response.get('channels', [])) < 1:
            return None

        return {
            'channels': response.get('channels', []),
            'cursor': response.get('response_metadata', {}).get('next_cursor')
        }

    def create(self, channel, token=None):
        # type: (str,OptStr) -> OptData
        """
        Create new channel with desired name
        more info https://api.slack.com/methods/channels.create

        Args:
            channel: channel name, can only contain lowercase letters, numbers,
                hyphens, and underscores, and must be 21 characters or less
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channel info as :py:class:`typing.Dict`
            when success
        """
        params = {
            'name': channel,
            'validate': True
        }
        return super()._call(
            method='create',
            data_key='channel',
            data=params,
            default={},
            token=token
        )

    def onboard(self, users_ids, cursor=None, invite_token=None):
        # type: (List[str], OptStr, OptStr) -> bool
        """
        Invite users to all the channels available in token scope except general

        Args:
            users_ids: :py:class:`typing.List` of slack user ids
            cursor: pagination cursor for retry etc.
            invite_token: optional auth token that will overwrite SlackApi token
                used for channel invitation
        Returns:
            boolean success status
        """
        channels = self.list(
            limit=10,
            cursor=cursor
        )
        if not channels:
            log.error('Channels are unavailable...')
            return False

        data = channels.get('channels', [])
        sleep(STANDARD_DELAY)

        for channel in data:
            channel_id = channel.get('id', None)
            is_archived = channel.get('is_archived', None)
            is_general = channel.get('is_general', None)

            if channel_id and not is_archived and not is_general:
                info = self.info(channel_id)
                sleep(STANDARD_DELAY)
                if not info:
                    log.warning("throttling break...")
                    sleep(THROTTLING_DELAY)
                    return self.onboard(users_ids, cursor, invite_token)

                members = info.get('members', [])
                for uid in users_ids:
                    if uid not in members:
                        log.debug(f'inviting "{uid}" into "{channel_id}"')
                        invite = self.invite(channel_id, uid, invite_token)
                        if not invite:
                            log.warning("throttling break...")
                            sleep(THROTTLING_DELAY)
                            return self.onboard(users_ids, cursor, invite_token)
                        sleep(STANDARD_DELAY)
                    else:
                        log.debug(f'invite aborted: '
                                  f'{uid}" already in "{channel_id}"')
            else:
                log.info(
                    f'channel skipped "{channel_id}": '
                    f'archived: {str(is_archived)}, general: {str(is_general)}'
                )

        if channels.get('cursor'):
            sleep(STANDARD_DELAY)
            return self.onboard(users_ids, channels.get('cursor'), invite_token)

        return True

    def invite(self, channel, user, token=None):
        # type: (str,str,OptStr) -> OptData
        """
        Invite user to the channel
        more info https://api.slack.com/methods/channels.invite

        Args:
            channel: Slack channel id like CXJSD234G
            user: Slack user id like UXS65F48
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channel info as :py:class:`typing.Dict`
            when success
        """
        params = {'channel': channel, 'user': user}
        return super()._call(
            method='invite',
            data_key='channel',
            data=params,
            default={},
            token=token
        )

    def info(self, channel_id, token=None):
        # type: (str,OptStr) -> OptData
        """
        Get channel info by channel id
        more info https://api.slack.com/methods/channels.info

        Args:
            channel_id: Slack channel id
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if channel_id not found or channel info
            as :py:class:`typing.Dict` when success
        """
        params = {'channel': channel_id}
        return super()._call(
            method='info',
            data_key='channel',
            http_get=True,
            data=params,
            default={},
            token=token
        )

    def channel_info(self, channel_name, token=None):
        # type: (str,OptStr) -> OptData
        """
        Find channel info by channel name
        There is no equivalent method in Slack API

        Args:
            channel_name: Slack channel name
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if channel_name is not found or channel info
            as :py:class:`typing.Dict` when success
        """
        channels = self.list(token=token, limit=1000)
        if not channels:
            log.error('Channels are unavailable')
            return None

        channel_id = ''
        channels_list = channels.get('channels', [])
        for channel in channels_list:
            name = channel.get('name')
            if name and name == channel_name and channel.get('id'):
                return channel
        else:
            log.warning(f'Channel "{channel_id}" not found')
            return None

    def history(self, channel, count=100, latest=None, token=None):
        # type: (str,int,OptStr,OptStr) -> OptData
        """
        Fetches history of messages and events from a channel.
        more info https://api.slack.com/methods/channels.history

        Args:
            channel: Slack channel id like CXJSD234G
            count: number of messages per page
            latest: End of time range
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if error occurred or number of removed messages
        """
        params = {'channel': channel, 'count': f'{count}'}

        if latest:
            params['latest'] = latest

        return super()._call(
            method='history',
            data_key='',
            data=params,
            default=[],
            http_get=True,
            token=token,
            full_response=True
        )

    def clear_history(self, channel_name, chat):
        # type: (str,Chat) -> int
        """
        Channel history cleaner
        Reads history and removes messages one by one

        Args:
            channel_name: Slack channel name
            chat: chat api handler
        Returns:
            Number of removed messages
        """
        deleted = 0
        channel = self.channel_info(channel_name)
        if channel:
            channel_id: str = channel.get('id', '')
            has_more = True
            msg_id = None
            log.info(f'channel id: "{channel_id}'"")

            while has_more:
                data = self._history(msg_id, channel_id)
                sleep(SMALL_DELAY)
                messages = data[0]
                has_more = data[1]

                for msg in messages:
                    msg_id = msg.get('ts')
                    log.info(f'deleting ts {msg_id}')
                    delete = chat.delete(channel_id, msg_id)
                    sleep(SMALL_DELAY)
                    if delete:
                        deleted += 1
                    else:
                        log.warning("throttling break...")
                        sleep(THROTTLING_DELAY)
                        return deleted + self.clear_history(channel_name, chat)

        return deleted

    def _history(self, msg_id, channel_id):
        # type: (OptStr,str) -> Tuple[ListAny, bool]
        """
        Channel history retriever
        Args
            msg_id:  message id to start from
            channel_id: channel id for history retrieve
        Returns:
            Tuple with messages data and information about
            availability of next page
        """

        if msg_id:
            history = self.history(channel_id, 10, msg_id)
        else:
            history = self.history(channel_id, 10)

        sleep(STANDARD_DELAY)
        messages: List[Any] = []
        has_more = False

        if history:
            messages = history.get('messages', [])
            has_more = history.get('has_more', False)

        return messages, has_more
