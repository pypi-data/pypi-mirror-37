from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse

import json
from . import Worker


class SyncData(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        Worker.add_sync(json.loads(request.data))
        return Response({}, status=200)
