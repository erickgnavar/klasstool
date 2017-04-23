import json

from django.http import JsonResponse
from channels import Group
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from . import serializers
from klasstool.courses.models import Session
from klasstool.polls.models import Poll


class SessionPollListView(APIView):

    serializer_class = serializers.PollSerializer

    def get_queryset(self):
        qs = Poll.objects.all()
        session = get_object_or_404(Session, id=self.kwargs.get('session_id'))
        qs = qs.filter(session=session)
        return qs

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return JsonResponse({
            'data': serializer.data
        })


class PollResponseCreateView(APIView):

    def post(self, request, *args, **kwargs):
        # TODO: check poll and choice belongs to session
        serializer = serializers.ResponseSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            text = json.dumps(serializers.PollSerializer(response.poll).data)
            Group('session-{}'.format(response.poll.session.id)).send({
                'text': text
            })
            return JsonResponse({
                'data': {
                    'id': response.id
                }
            }, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
