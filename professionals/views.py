from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet

from professionals.models import Professional
from professionals.serializers import ProfessionalSerializer


class PlainTextJSONParser(JSONParser):
    media_type = "text/plain"


class ProfessionalViewSet(ModelViewSet):
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [PlainTextJSONParser, JSONParser]

    def get_queryset(self):
        queryset = Professional.objects.all()

        specialty = self.request.query_params.get("specialty")

        if specialty:
            queryset = queryset.filter(
                specialty__icontains=specialty
            )
        return queryset