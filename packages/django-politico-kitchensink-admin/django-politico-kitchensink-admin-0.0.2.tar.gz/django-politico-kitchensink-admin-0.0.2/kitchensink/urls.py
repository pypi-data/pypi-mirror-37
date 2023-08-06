from django.urls import path

from .views import Home, PublishSheet

urlpatterns = [
    path("", Home.as_view(), name="kitchensink-home"),
    path(
        "publish/<str:pk>/", PublishSheet.as_view(), name="kitchensink-publish"
    ),
]
