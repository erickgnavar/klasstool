from channels import Group


def _session_group(message):
    _, session_id = message.content['path'].strip('/').split('/')
    return Group('session-{}'.format(session_id))


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    _session_group(message).add(message.reply_channel)


def ws_disconnect(message):
    _session_group(message).discard(message.reply_channel)
