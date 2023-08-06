# -*- coding: utf-8 -*-
"""
Automated tests for Ed provisioner.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""

import pytest
import responses

from nftl_slack_tools.client import SlackClient


@pytest.fixture
def slack_client():
    return SlackClient('xoxp-')


@responses.activate
def test_slack_create_user(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/signup.createUser',
        body='{"ok":true, "user_id": "UXX", "api_token": "xoxs-"}',
        status=200,
        content_type='application/json'
    )

    # then:
    data = slack_client.get_signup_api().create_user(
        'irrelevant', 'irrelevant', 'irrelevant'
    )
    assert data


@responses.activate
def test_slack_create_user_invalit(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/signup.createUser',
        body='{"ok":false}',
        status=200,
        content_type='application/json'
    )

    # then:
    data = slack_client.get_signup_api().create_user(
        'irrelevant', 'irrelevant', 'irrelevant'
    )
    assert not data
