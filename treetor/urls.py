from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^',include('treetorapp.urls')),

]
