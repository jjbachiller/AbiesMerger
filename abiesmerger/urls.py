"""abiesmerger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from fileManager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^merge/$', views.merge, name='merge'),
    url(r'^download/(?P<folder>[\w-]+)/$', views.download, name='download'),
    # url(r'^downloads/(?P<folder>[\w-]+)/' + settings.ABIES_ZIP_FILE + '$', views.downloadFile, name='downloadFile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
