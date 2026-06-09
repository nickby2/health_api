from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from professionals.models import Professional
from professionals.serializers import ProfessionalSerializer


class ProfessionalViewSet(ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]