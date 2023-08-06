import uuid

from django.db import models


class Sheet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        "Project title", max_length=250, help_text="A title for this sheet"
    )
    sheet_id = models.SlugField(
        "Google Sheet ID", help_text="Sheet ID from URL"
    )

    def __str__(self):
        return self.title
