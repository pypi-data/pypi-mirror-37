import json

from django.urls import reverse
from django.views.generic import TemplateView

from kitchensink.conf import settings as app_settings
from kitchensink.models import Sheet
from kitchensink.utils.auth import secure


@secure
class Home(TemplateView):
    template_name = "kitchensink/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["DOMAIN"] = app_settings.PUBLISH_DOMAIN
        context["SECRET"] = app_settings.SECRET_KEY
        context["SHEETS"] = json.dumps(
            [
                {
                    "id": sheet.sheet_id,
                    "title": sheet.title,
                    "publish": reverse("kitchensink-publish", args=[sheet.id]),
                }
                for sheet in Sheet.objects.order_by("title")
            ]
        )
        return context
