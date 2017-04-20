from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^nucleic_acid_types/$', views.get_nucleic_acid_types, name='get_nucleic_acid_types'),
    url(r'^save/$', views.save_sample, name='save_sample'),
    url(r'^delete/$', views.delete_sample, name='delete_sample'),
]
