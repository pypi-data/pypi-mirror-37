# Library: nftl-slack-tools

This is a tool for Slack API handling.

Source documentation of api is available [here](https://api.slack.com/)

[PyPI project page](https://pypi.org/project/nftl-slack-tools/)


# Installation

```sh
pip install nftl-slack-tools
```

# Usage

```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    channel = slack.get_channels_api().create('new_order')

    if channel:
        print('Yupi!')
```

# Interface

## Channels

Slack API wrapper that is handling channels category

[API reference](https://api.slack.com/methods#channels)

### Usage 
```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    channels_api = slack.get_channels_api()
```
### Available methods
#### list()
Lists all channels in a Slack team.
Channels depends on token so if you want to list users use user token
instead of SlackApi admin token

Slack API : [channels.list](https://api.slack.com/methods/channels.list)
 
```
Args:
    limit: optional page length ( default: 1000 )
    cursor: optional message list cursor for pagination
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or channels :py:class:`typing.Dict`
    with two keys: channels (list of channels) and cursor for pagination
    when success
```

#### create()
Create new channel with desired name

Slack API : [channels.create](https://api.slack.com/methods/channels.create)
```
Args:
    channel: channel name, can only contain lowercase letters, numbers,
        hyphens, and underscores, and must be 21 characters or less
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or channel info as :py:class:`typing.Dict`
    when success
```            

#### onboard()
Invite users to all the channels available in token scope except general

Slack API : Not available
```
Args:
    users_ids: :py:class:`typing.List` of slack user ids
    cursor: pagination cursor for retry etc.
    invite_token: optional auth token that will overwrite SlackApi token
        used for channel invitation
Returns:
    boolean success status
```

#### invite()
Invite user to the channel

Slack API : [channels.invite](https://api.slack.com/methods/channels.invite)
```
Args:
    channel: Slack channel id like CXJSD234G
    user: Slack user id like UXS65F48
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or channel info as :py:class:`typing.Dict`
    when success
```

#### info()
Get channel info by channel id

Slack API : [channels.info](https://api.slack.com/methods/channels.info)
```
Args:
    channel_id: Slack channel id
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if channel_id not found or channel info
    as :py:class:`typing.Dict` when success
```

#### channel_info()
Find channel info by channel name

Slack API : Not available
```
Args:
    channel_name: Slack channel name
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if channel_name is not found or channel info
    as :py:class:`typing.Dict` when success
```

#### history()
Fetches history of messages and events from a channel.

Slack API : [channels.history](https://api.slack.com/methods/channels.history)
```
Args:
    channel: Slack channel id like CXJSF234X
    count: number of messages per page
    latest: End of time range
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if error occurred or number of removed messages
```

#### clear_history()
Channel history cleaner
Reads history and removes messages one by one

Slack API : Not available
```
Args:
    channel_name: Slack channel name
    chat: Chat api handler
Returns:
    Number of removed messages
```

## Groups

Slack API wrapper that is handling groups category

[API reference](https://api.slack.com/methods#groups)

### Usage 
```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    channels_api = slack.get_groups_api()
```
### Available methods
#### list()
Lists all groups aka private channel in a Slack team.
Groups depends on token so if you want to list users use user token
instead of SlackApi admin token

Slack API : [groups.list](https://api.slack.com/methods/groups.list)
 
```
Args:
    limit: optional page length ( default: 1000 )
    cursor: optional message list cursor for pagination
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or channels :py:class:`typing.Dict`
    with two keys: groups (list of groups) and cursor for pagination
    when success
```

#### create()
Create new group with desired name

Slack API : [groups.create](https://api.slack.com/methods/groups.create)
```
Args:
    group: group name, can only contain lowercase letters, numbers,
        hyphens, and underscores, and must be 21 characters or less
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or group info as :py:class:`typing.Dict`
    when success
```            

#### onboard()
Invite users to all the groups available in token scope except general

Slack API : Not available
```
Args:
    users_ids: :py:class:`typing.List` of slack user ids
    cursor: pagination cursor for retry etc.
    invite_token: optional auth token that will overwrite SlackApi token
        used for group invitation
Returns:
    boolean success status
```

#### invite()
Invite user to the group

Slack API : [groups.invite](https://api.slack.com/methods/groups.invite)
```
Args:
    group: Slack group id like GXJSD234G
    user: Slack user id like UXS65F48
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or group info as :py:class:`typing.Dict`
    when success
```

#### info()
Get group info by group id

Slack API : [groups.info](https://api.slack.com/methods/groups.info)
```
Args:
    group_id: Slack group id
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if group_id not found or group info
    as :py:class:`typing.Dict` when success
```

#### group_info()
Find group info by group name

Slack API : Not available
```
Args:
    group_name: Slack channel name
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if group_name is not found or channel info
    as :py:class:`typing.Dict` when success
```

#### history()
Fetches history of messages and events from a group.

Slack API : [groups.history](https://api.slack.com/methods/groups.history)
```
Args:
    group: Slack group id like GXJSD234G
    count: number of messages per page
    latest: End of time range
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if error occurred or number of removed messages
```

#### clear_history()
Group history cleaner
Reads history and removes messages one by one

Slack API : Not available
```
Args:
    group_name: Slack group name
    chat: chat api handler
Returns:
    Number of removed messages
```

## Users

Slack API wrapper that is handling users category

[API reference](https://api.slack.com/methods#users)

### Usage 
```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    users_api = slack.get_users_api()
```
### Available methods

#### info()
Gets information about the user

Slack API : [users.info](https://api.slack.com/methods/users.info)
```
Args:
    user: Slack user id like UXS65F48
    locale: should response contain locale info
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or user info as :py:class:`typing.Dict`
    when success
```

#### validate_name()
Validate users name field

Slack API : This method is not documented
```
Args:
    name: name to be validated
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or boolean validity result
```

#### invite()
Invite user to the workspace

Slack API : This method is not documented
```
Args:
    email: account email,
    firstname: account first name
    lastname: account last name
    channels: comma separated list of channels (id's) to be invited,
    restricted: restrict to guest that can use multiple channels
    token: optional auth token that will overwrite SlackApi token
Returns:
    None if data is invalid or boolean validity result
```

## Chat

Slack API wrapper that is handling chat category

[API reference](https://api.slack.com/methods#chat)

### Usage 
```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    chat_api = slack.get_chat_api()
```
### Available methods

#### delete()
Deletes a message

Slack API : [chat.delete](https://api.slack.com/methods/chat.delete)
```
Args:
    channel: Slack channel id like CXJSD234G
    ts: Message id
    token: optional auth token that will overwrite SlackApi token
Returns:
    boolean operation status
```

## Signup

Slack API wrapper that is handling signup category

This category is not documented in Slack doc 

### Usage 
```python
    from nftl_slack_tools.client import SlackClient

    slack = SlackClient(slack_token='xoxp-...')
    chat_api = slack.get_signup_api()
```
### Available methods

#### create_user()
Create a user with invitation code

This method is not documented in Slack doc

```
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
```

# Deployment how to

Available [here](https://packaging.python.org/tutorials/packaging-projects/)