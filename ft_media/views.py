import os
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage


class UploadApiView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FileUploadParser,)

    def put(self, request, filename):
        file_obj = request.data['file']
        if not default_storage.exists(os.path.join('images', filename)):
            path = default_storage.save(os.path.join('images', filename), file_obj)
        else:
            path = default_storage.path(os.path.join('images', filename))
        return Response({"path": path}, status=200)

upload_view = UploadApiView.as_view()