from django.conf.urls import url

from .views import ModelExportView, PageExportView

app_name = 'export-page'

urlpatterns = [
    url(r'^(?P<page_pk>\d+)/(?P<file_format>\w+)/$', PageExportView.as_view(), name='cms_page'),
    url(r'^(?P<app>\w+):(?P<model>\w+)/(?P<pk>\d+)/(?P<file_format>\w+)/$', ModelExportView.as_view(), name='model'),
]
