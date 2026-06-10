from django.contrib import admin

from professionals.models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
	list_display = ("id", "social_name", "profession", "contact", "created_at")
	search_fields = ("social_name", "profession", "contact")
