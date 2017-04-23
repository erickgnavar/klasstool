from rest_framework import serializers

from klasstool.polls.models import Choice, Poll, Response


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = (
            'id', 'value'
        )


class PollSerializer(serializers.ModelSerializer):

    finished = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True, read_only=True)
    results = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = (
            'id', 'title', 'finished', 'choices', 'results'
        )

    def get_finished(self, poll):
        return not poll.is_active

    def get_results(self, poll):
        poll_responses_quantity = poll.responses.all().count()
        counter = {}
        # TODO: impprove this
        for response in poll.responses.all():
            counter.setdefault(response.choice.id, 0)
            counter[response.choice.id] += 1
        winner = None
        if counter:
            winner = max(counter.items(), key=lambda x: x[1])

        res = []
        for choice in poll.choices.all():
            res.append(self._compute_result(choice, poll_responses_quantity, winner[0] if winner is not None else 0))
        return res

    def _compute_result(self, choice, poll_responses_quantity, winner_choice_id):
        responses_quanitty = choice.responses.all().count()
        percentage = round(responses_quanitty / poll_responses_quantity * 100, 2) if poll_responses_quantity else 0
        return {
            'value': choice.value,
            'votes': responses_quanitty,
            'percentage': percentage,
            'winner': choice.id == winner_choice_id
        }


class ResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Response
        fields = (
            'poll',
            'choice'
        )
