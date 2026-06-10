from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet

from professionals.models import Professional
from professionals.serializers import ProfessionalSerializer


class PlainTextJSONParser(JSONParser):
    media_type = "text/plain"


class ProfessionalViewSet(ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [PlainTextJSONParser, JSONParser]