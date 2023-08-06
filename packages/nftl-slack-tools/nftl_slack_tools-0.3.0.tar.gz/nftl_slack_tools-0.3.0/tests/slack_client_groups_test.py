# -*- coding: utf-8 -*-
"""
Automated tests for Ed provisioner.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import json

import pytest
import responses
from requests import HTTPError

from nftl_slack_tools.client import SlackClient


@pytest.fixture()
def delays(monkeypatch, mocker):
    monkeypatch.setattr("nftl_slack_tools.slack_api.STANDARD_DELAY", 0)
    monkeypatch.setattr("nftl_slack_tools.slack_api.SMALL_DELAY", 0)
    monkeypatch.setattr("nftl_slack_tools.slack_api.THROTTLING_DELAY", 0)
    mocker.patch('nftl_slack_tools.api.channels.sleep', return_value=None)
    mocker.patch('nftl_slack_tools.api.groups.sleep', return_value=None)


@pytest.fixture
def slack_client():
    return SlackClient('xoxp-xxxx')


@pytest.fixture
def broken_url_slack_client():
    return SlackClient('xoxp-xxxx', 'https://example.com/api')


@responses.activate
def test_slack_groups_info_list(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.list',
        body='{"ok":true,"groups":[{"some_channel_data":true}]}',
        status=200,
        content_type='application/json'
    )

    # then:
    data = slack_client.get_groups_api().list()
    assert isinstance(data, dict)
    assert isinstance(data.get('groups'), list)


@responses.activate
def test_slack_groups_create(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/groups.create',
        body='{"ok":true,"group":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(slack_client.get_groups_api().create('terefere'), dict)


@responses.activate
def test_slack_groups_invite(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/groups.invite',
        body='{"ok":true,"group":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(
        slack_client.get_groups_api().invite('terefere', 'UXXX'), dict)


@responses.activate
def test_slack_groups_channel_info_by_name_valid(slack_client):
    # given:
    _req_channel_info_by_name()

    # then:
    assert isinstance(
        slack_client.get_groups_api().group_info('cname'), dict)


@responses.activate
def test_slack_groups_channel_info_exception(slack_client):
    # given:
    responses.add(responses.GET, 'https://slack.com/api/groups.list',
                  body=HTTPError('Error'))

    # then:
    assert not slack_client.get_groups_api().list(cursor='irrelevant')


@responses.activate
def test_slack_groups_channel_info_by_name_invalid_req(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.list',
        body='',
        status=404,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_groups_api().list()


@responses.activate
def test_slack_groups_info_method(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.info',
        body='',
        status=404,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_groups_api().info('irrelevant')


@responses.activate
def test_slack_groups_channel_info_by_name_invalid(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.list',
        body='{"ok":false,"error":"boom!"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_groups_api().group_info('cname')


@responses.activate
def test_slack_groups_channel_info_by_name_not_found(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.list',
        body='{"ok":true,"groups":[{"id":"id","name":"boom"}]}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_groups_api().group_info('cname')


@responses.activate
def test_slack_groups_onboard_no_channels(slack_client, mocker, caplog):
    # given:
    mocker.patch('nftl_slack_tools.api.groups.Groups.list', return_value=None)

    # when:
    slack_client.get_groups_api().onboard(['irrelevant'])

    # then:
    assert 'Channels are unavailable' in caplog.text


@responses.activate
def test_slack_groups_onboard(slack_client, mocker, caplog, delays):
    # given:
    ret_present = mocker.patch('nftl_slack_tools.api.groups.Groups.list')
    groups_with_cursor = {
        'groups': [
            {'id': 'irrelevant', 'is_general': False, 'is_open': True},
            {'id': 'irrelevant2', 'is_general': False, 'is_open': True}
        ],
        'cursor': 'next please'
    }
    groups_without_cursor = {
        'groups': [
            {'id': 'irrelevant', 'is_general': False, 'is_open': True},
            {'is_general': False, 'is_open': False}
        ]
    }

    ret_present.side_effect = [
        groups_with_cursor,
        groups_with_cursor,
        groups_with_cursor,
        groups_without_cursor
    ]
    ret_present = {
        'members': [
            'irrelevant'
        ]
    }
    ret_empty = {
        'members': []
    }
    info = mocker.patch('nftl_slack_tools.api.groups.Groups.info')
    info.side_effect = [
        None,
        ret_present,
        ret_empty,
        ret_present,
        ret_empty,
        ret_present
    ]

    invite = mocker.patch('nftl_slack_tools.api.groups.Groups.invite')
    invite.side_effect = [
        None,
        {'ok'}
    ]

    # when:
    onboard = slack_client.get_groups_api().onboard(['irrelevant'])

    # then:
    assert 'throttling break' in caplog.text
    assert onboard


@responses.activate
def test_slack_groups_clear_history(slack_client, delays):
    def _response(has_more: bool = False):
        return {
            'ok': True,
            'has_more': has_more,
            'messages': [{
                'ts': '111',
                'name': channel_name
            }]
        }

    # given:
    channel_name = 'general'
    channel_id = 'xxx'
    api_ = 'https://slack.com/api'
    _req_channel_info_by_name(channel_name)

    responses.add(
        method=responses.GET,
        url='%s/groups.history?channel=%s&count=10'
            % (api_, channel_id),
        body=json.dumps(_response(True)),
        status=200,
        content_type='application/json'
    )

    responses.add(
        method=responses.GET,
        url='%s/groups.history?channel=%s&count=10&latest=%s'
            % (api_, channel_id, '111'),
        body=json.dumps(_response(False)),
        status=200,
        content_type='application/json'
    )

    _req_chat_delete(channel_id)
    _req_chat_delete(channel_id, 'false')
    _req_chat_delete(channel_id)

    # then:
    assert slack_client.get_groups_api().clear_history(
        channel_name,
        slack_client.get_chat_api()
    ) == 2


def _req_channel_info_by_name(name: str = 'cname'):
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/groups.list',
        body='{"ok":true,"groups":[{"id":"xxx","name":"%s"}]}' % name,
        status=200,
        content_type='application/json'
    )


def _req_chat_delete(channel_id: str, ok: str = 'true',
                     base_url: str = 'https://slack.com/api'):
    responses.add(
        method=responses.POST,
        url=('%s/chat.delete' % base_url),
        body='{"ok":%s,"group":"%s"}' % (ok, channel_id),
        status=200,
        content_type='application/json'
    )
