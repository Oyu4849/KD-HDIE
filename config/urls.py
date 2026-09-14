from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path("admin/", admin.site.urls),

    path("systems/", include("systems.urls")),

    path("systems/api/", include("systems.api.urls")),

]
