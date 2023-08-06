import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import View
from django.conf import settings


import json
from . import Worker


class SyncData(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        Worker.add_sync(json.loads(request.data))
        return Response({}, status=200)


class GetKarat(View):

    def get(self, request):
        if not hasattr(settings, 'AGENT_URL'):
            return JsonResponse({"message": "missing AGENT_URL"}, status=409)
        url = "{}{}".format(settings.AGENT_URL, '/ping-sync/')
        requests.get(url)
        r = requests.get(url)
        return JsonResponse(r.text, status=200, safe=False)
