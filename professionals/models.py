from django.db import models


class Professional(models.Model):
    social_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["social_name", "id"]

    def __str__(self):
        return self.social_name