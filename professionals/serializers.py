import bleach

from rest_framework import serializers

from .models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ["id", "social_name", "profession", "address", "contact", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_social_name(self, value):
        cleaned_value = bleach.clean(value, strip=True)
        if len(cleaned_value) < 3:
            raise serializers.ValidationError("Nome social muito curto.")
        return cleaned_value

    def validate_profession(self, value):
        return bleach.clean(value, strip=True)

    def validate_address(self, value):
        return bleach.clean(value, strip=True)

    def validate_contact(self, value):
        return bleach.clean(value, strip=True)