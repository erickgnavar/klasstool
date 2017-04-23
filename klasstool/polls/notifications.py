import json

from channels import Group


def poll_started(poll):
    _send_poll(poll)


def poll_finished(poll):
    _send_poll(poll)


def poll_updated(poll):
    _send_poll(poll)


def _send_poll(poll):
    from klasstool.api_v1.serializers import PollSerializer
    text = json.dumps(PollSerializer(poll).data)
    Group('session-{}'.format(poll.session.id)).send({
        'text': text
    })
