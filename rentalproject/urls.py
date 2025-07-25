"""rentalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import url
from django.urls import path, re_path, include
from django.contrib import admin
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', lambda request: redirect('admin-dashboard'), name='admin-root-redirect'),
    path('admin/', include('dashboard.urls')),
    path("admin/", admin.site.urls),
    path("",include("rentalapp.urls")),
    path("rental_business/", include("rental_business.urls")),
    


    # re_path('admin-interface/', include('admin_interface.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")),)