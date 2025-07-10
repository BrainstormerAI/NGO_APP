from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ProjectManagement
from .serializers import ProjectManagementSerializer

class ProjectManagementViewSet(viewsets.ModelViewSet):
    queryset = ProjectManagement.objects.all().order_by('-modified_date')
    serializer_class = ProjectManagementSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)