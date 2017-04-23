import json

from channels import Group

# TODO: Add resource urls


def poll_started(poll):
    Group('session-{}'.format(poll.session.id)).send({
        'text': json.dumps({
            'type': 'POLL_STARTED',
            'resource': ''
        })
    })


def poll_finished(poll):
    Group('session-{}'.format(poll.session.id)).send({
        'text': json.dumps({
            'type': 'POLL_FINISHED',
            'resource': ''
        })
    })
