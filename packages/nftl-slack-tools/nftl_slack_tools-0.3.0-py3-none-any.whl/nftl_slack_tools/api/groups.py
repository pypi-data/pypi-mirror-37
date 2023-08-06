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
    THROTTLING_DELAY, SMALL_DELAY, OptData, OptInt, OptStr, ListAny


class Groups(SlackApi):
    """
    Slack API wrapper that is handling groups category
    more info https://api.slack.com/methods#groups
    """
    API_CATEGORY = "groups"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def list(self, limit=1000, cursor=None, token=None):
        # type: (OptInt,OptStr,OptStr) -> OptData
        """
        Lists all groups aka private channel in a Slack team.
        Groups depends on token so if you want to list users use user token
        instead of SlackApi admin token
        more info https://api.slack.com/methods/groups.list

        Args:
            limit: optional page length ( default: 1000 )
            cursor: optional message list cursor for pagination
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channels :py:class:`typing.Dict`
            with two keys: groups (list of groups) and cursor for pagination
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

        if not response or len(response.get('groups', [])) < 1:
            return None

        return {
            'groups': response.get('groups', []),
            'cursor': response.get('response_metadata', {}).get('next_cursor')
        }

    def create(self, group, token=None):
        # type: (str,OptStr) -> OptData
        """
        Create new group with desired name
        more info https://api.slack.com/methods/groups.create

        Args:
            group: group name, can only contain lowercase letters, numbers,
                hyphens, and underscores, and must be 21 characters or less
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or group info as :py:class:`typing.Dict`
            when success
        """
        params = {
            'name': group,
            'validate': True
        }
        return super()._call(
            method='create',
            data_key='group',
            data=params,
            default={},
            token=token
        )

    def onboard(self, users_ids, cursor=None, invite_token=None):
        # type: (List[str], OptStr, OptStr) -> bool
        """
        Invite users to all the groups available in token scope except general

        Args:
            users_ids: :py:class:`typing.List` of slack user ids
            cursor: pagination cursor for retry etc.
            invite_token: optional auth token that will overwrite SlackApi token
                used for group invitation
        Returns:
            boolean success status
        """
        groups = self.list(
            limit=10,
            cursor=cursor
        )
        if not groups:
            log.error('Channels are unavailable...')
            return False

        data = groups.get('groups', [])
        sleep(STANDARD_DELAY)

        for group in data:
            group_id = group.get('id', None)
            is_archived = group.get('is_archived', None)
            is_open = group.get('is_open', None)

            if group_id and not is_archived:
                info = self.info(group_id)
                sleep(STANDARD_DELAY)
                log.debug(f'-------------------- info {info}')
                if not info:
                    log.warning("throttling break...")
                    sleep(THROTTLING_DELAY)
                    return self.onboard(users_ids, cursor, invite_token)

                members = info.get('members', [])
                for uid in users_ids:
                    if uid not in members:
                        log.debug(f'inviting "{uid}" into "{group_id}"')
                        invite = self.invite(group_id, uid, invite_token)
                        if not invite:
                            log.warning("throttling break...")
                            sleep(THROTTLING_DELAY)
                            return self.onboard(users_ids, cursor, invite_token)
                        sleep(STANDARD_DELAY)
                    else:
                        log.debug(f'invite aborted: '
                                  f'{uid}" already in "{group_id}"')
            else:
                log.info(
                    f'group skipped "{group_id}": '
                    f'archived: {str(is_archived)}, general: {str(is_open)}'
                )

        if groups.get('cursor'):
            sleep(STANDARD_DELAY)
            return self.onboard(users_ids, groups.get('cursor'), invite_token)

        return True

    def invite(self, group, user, token=None):
        # type: (str,str,OptStr) -> OptData
        """
        Invite user to the group
        more info https://api.slack.com/methods/group.invite

        Args:
            group: Slack group id like GXJSD234G
            user: Slack user id like UXS65F48
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or group info as :py:class:`typing.Dict`
            when success
        """
        params = {'channel': group, 'user': user}
        return super()._call(
            method='invite',
            data_key='group',
            data=params,
            default={},
            token=token
        )

    def info(self, group_id, token=None):
        # type: (str,OptStr) -> OptData
        """
        Get group info by group id
        more info https://api.slack.com/methods/groups.info

        Args:
            group_id: Slack group id
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if group_id not found or group info
            as :py:class:`typing.Dict` when success
        """
        params = {'channel': group_id}
        return super()._call(
            method='info',
            data_key='group',
            http_get=True,
            data=params,
            default={},
            token=token
        )

    def group_info(self, group_name, token=None):
        # type: (str,OptStr) -> OptData
        """
        Find group info by group name
        There is no equivalent method in Slack API

        Args:
            group_name: Slack channel name
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if group_name is not found or channel info
            as :py:class:`typing.Dict` when success
        """
        groups = self.list(token=token, limit=1000)
        if not groups:
            log.error('Groups are unavailable')
            return None

        group_id = ''
        groups_list = groups.get('groups', [])
        for channel in groups_list:
            name = channel.get('name')
            if name and name == group_name and channel.get('id'):
                return channel
        else:
            log.warning(f'Group "{group_id}" not found')
            return None

    def history(self, group, count=100, latest=None, token=None):
        # type: (str,int,OptStr,OptStr) -> OptData
        """
        Fetches history of messages and events from a group.
        more info https://api.slack.com/methods/groups.history

        Args:
            group: Slack group id like GXJSD234G
            count: number of messages per page
            latest: End of time range
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if error occurred or number of removed messages
        """
        params = {'channel': group, 'count': f'{count}'}

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

    def clear_history(self, group_name, chat):
        # type: (str,Chat) -> int
        """
        Group history cleaner
        Reads history and removes messages one by one

        Args:
            group_name: Slack group name
            chat: chat api handler
        Returns:
            Number of removed messages
        """
        deleted = 0
        group = self.group_info(group_name)
        if group:
            group_id: str = group.get('id', '')
            has_more = True
            msg_id = None
            log.info(f'group id: "{group_id}'"")

            while has_more:
                data = self._history(msg_id, group_id)
                sleep(SMALL_DELAY)
                messages = data[0]
                has_more = data[1]

                for msg in messages:
                    msg_id = msg.get('ts')
                    log.info(f'deleting ts {msg_id}')
                    delete = chat.delete(group_id, msg_id)
                    sleep(SMALL_DELAY)
                    if delete:
                        deleted += 1
                    else:
                        log.warning("throttling break...")
                        sleep(THROTTLING_DELAY)
                        return deleted + self.clear_history(group_name, chat)

        return deleted

    def _history(self, msg_id, group_id):
        # type: (OptStr,str) -> Tuple[ListAny, bool]
        """
        Group history retriever
        Args
            msg_id:  message id to start from
            group_id: group id for history retrieve
        Returns:
            Tuple with messages data and information about
            availability of next page
        """

        if msg_id:
            history = self.history(group_id, 10, msg_id)
        else:
            history = self.history(group_id, 10)

        sleep(STANDARD_DELAY)
        messages: List[Any] = []
        has_more = False

        if history:
            messages = history.get('messages', [])
            has_more = history.get('has_more', False)

        return messages, has_more
