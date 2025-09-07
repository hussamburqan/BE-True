"""
URL configuration for true project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include

urlpatterns = [
    path('auth/', include('authentiocation.urls')),
    path('blog/', include('blog.urls')),
    path('courses/', include('courses.urls')),
    path('services/', include('services.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('careers/', include('careers.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('companies/', include('companies.urls')),
    path('partners/', include('partners.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('team/', include('team.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('audit/', include('audit.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)