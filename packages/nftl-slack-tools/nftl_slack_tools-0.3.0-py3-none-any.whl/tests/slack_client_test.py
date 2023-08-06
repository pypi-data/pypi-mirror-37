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
from nftl_slack_tools.slack_api import SlackApi


@pytest.fixture(autouse=True)
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


def test_slack_users(broken_url_slack_client):
    # given:
    api1 = broken_url_slack_client.get_users_api()
    api2 = broken_url_slack_client.get_users_api()

    # then:
    assert api1 == api2


@responses.activate
def test_slack_users_info(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='{"ok":true,"user":{"test":"test"}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert slack_client.get_users_api().info('UXXX', locale=True)


@responses.activate
def test_slack_users_info_invalid(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='{"ok":false, "error":"error_key"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().info('UXXX', locale=True)


@responses.activate
def test_slack_users_info_invalid_network(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='',
        status=500,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().info('UXXX', locale=True)


def test_slack_channels(slack_client):
    # given:
    api1 = slack_client.get_channels_api()
    api2 = slack_client.get_channels_api()

    # then:
    assert api1 == api2


@responses.activate
def test_slack_channels_info(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[{"some_channel_data":true}]}',
        status=200,
        content_type='application/json'
    )

    # then:
    data = slack_client.get_channels_api().list()
    assert isinstance(data, dict)
    assert isinstance(data.get('channels'), list)


@responses.activate
def test_slack_channels_create(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/channels.create',
        body='{"ok":true,"channel":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(slack_client.get_channels_api().create('terefere'), dict)


@responses.activate
def test_slack_channels_invite(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/channels.invite',
        body='{"ok":true,"channel":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(
        slack_client.get_channels_api().invite('terefere', 'UXXX'), dict)


@responses.activate
def test_slack_channels_channel_info_by_name_valid(slack_client):
    # given:
    _req_channel_info_by_name()

    # then:
    assert isinstance(
        slack_client.get_channels_api().channel_info('cname'), dict)


@responses.activate
def test_slack_channels_channel_info_exception(slack_client):
    # given:
    responses.add(responses.GET, 'https://slack.com/api/channels.list',
                  body=HTTPError('Error'))

    # then:
    assert not slack_client.get_channels_api().list(cursor='irrelevant')


@responses.activate
def test_slack_channels_channel_info_by_name_invalid_req(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='',
        status=404,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().list()


@responses.activate
def test_slack_channels_info_method(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.info',
        body='',
        status=404,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().info('irrelevant')


@responses.activate
def test_slack_channels_channel_info_by_name_invalid(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":false,"error":"boom!"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().channel_info('cname')


@responses.activate
def test_slack_channels_channel_info_by_name_not_found(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[{"id":"id","name":"boom"}]}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().channel_info('cname')


@responses.activate
def test_slack_channels_onboard_no_channels(slack_client, mocker, caplog):
    # given:
    mocker.patch(
        'nftl_slack_tools.api.channels.Channels.list').return_value = None

    # when:
    slack_client.get_channels_api().onboard(['irrelevant'])

    # then:
    assert 'Channels are unavailable' in caplog.text


@responses.activate
def test_slack_channels_onboard(slack_client, mocker, caplog):
    # given:
    ret_present = mocker.patch('nftl_slack_tools.api.channels.Channels.list')
    channels_with_cursor = {'channels': [
        {'id': 'irrelevant', 'is_general': False, 'is_archived': False},
        {'id': 'irrelevant2', 'is_general': False, 'is_archived': False}],
        'cursor': 'next please'}
    channels_without_cursor = {'channels': [
        {'id': 'irrelevant', 'is_general': False, 'is_archived': False},
        {'id': 'irrelevant2', 'is_general': False, 'is_archived': True}]}

    ret_present.side_effect = [
        channels_with_cursor,
        channels_with_cursor,
        channels_with_cursor,
        channels_without_cursor
    ]
    ret_present = {
        'members': [
            'irrelevant'
        ]
    }
    ret_empty = {
        'members': []
    }
    info = mocker.patch('nftl_slack_tools.api.channels.Channels.info')
    info.side_effect = [None, ret_present, ret_empty, ret_present, ret_empty,
                        ret_present]

    invite = mocker.patch('nftl_slack_tools.api.channels.Channels.invite')
    invite.side_effect = [None, {'ok'}]

    # when:
    onboard = slack_client.get_channels_api().onboard(['irrelevant'])

    # then:
    assert 'throttling break' in caplog.text
    assert onboard


@responses.activate
def test_slack_users_validate_name(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.validateName',
        body='{"ok":true}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert slack_client.get_users_api().validate_name('irrelevant')


@responses.activate
def test_slack_users_validate_name_error(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.validateName',
        body='{"ok":false}',
        status=500,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().validate_name('irrelevant')


@responses.activate
def test_slack_users_invite(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.admin.invite',
        body='{"ok":true}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert slack_client.get_users_api().invite(
        'johnny@example.com', 'John', 'Bravo', 'CXX', True
    )


@responses.activate
def test_slack_users_invite_error(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.admin.invite',
        body='{"ok":false}',
        status=500,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().invite(
        'johnny@example.com', 'John', 'Bravo', 'CXX', True
    )


@responses.activate
def test_slack_channels_clear_history(slack_client):
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
        url='%s/channels.history?channel=%s&count=10'
            % (api_, channel_id),
        body=json.dumps(_response(True)),
        status=200,
        content_type='application/json'
    )

    responses.add(
        method=responses.GET,
        url='%s/channels.history?channel=%s&count=10&latest=%s'
            % (api_, channel_id, '111'),
        body=json.dumps(_response(False)),
        status=200,
        content_type='application/json'
    )

    _req_chat_delete(channel_id)
    _req_chat_delete(channel_id, 'false')
    _req_chat_delete(channel_id)

    # then:
    assert slack_client.get_channels_api().clear_history(
        channel_name,
        slack_client.get_chat_api()
    ) == 2


def test_slack_chat_postMessage(mocker, slack_client):
    # when:
    api_call = mocker.patch.object(SlackApi, '_call')
    slack_client.get_chat_api().postMessage('channel', 'message')

    # then:
    api_call.assert_called_once_with(
        method='postMessage',
        data_key='ok',
        data={'channel': 'channel', 'text': 'message'},
        default=None,
        token=None
    )


def _req_channel_info_by_name(name: str = 'cname'):
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[{"id":"xxx","name":"%s"}]}' % name,
        status=200,
        content_type='application/json'
    )


def _req_chat_postMessage(
        channel_id: str,
        ok: str='true',
        base_url: str='https://slack.com/api'
) -> None:
    responses.add(
        method=responses.POST,
        url=('%s/chat.postMessage' % base_url),
        body='{"ok":%s,"channel":"%s"}' % (ok, channel_id),
        status=200,
        content_type='application/json'
    )


def _req_chat_delete(channel_id: str, ok: str = 'true',
                     base_url: str = 'https://slack.com/api'):
    responses.add(
        method=responses.POST,
        url=('%s/chat.delete' % base_url),
        body='{"ok":%s,"channel":"%s"}' % (ok, channel_id),
        status=200,
        content_type='application/json'
    )
