from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from . import views
from django.views.generic import RedirectView
app_name = 'handling'
urlpatterns = [
    path(r'',admin.site.urls),
    url(r'upload_from_cv',views.changelist,name='changelist'),
    url(r'add_new_cv',views.addNewCv,name='addNewCv'),
    url(r'^duplicateCandidate/(?P<candidate_mail>(.*))/(?P<candidate_name>(.*))/(?P<candidate_jt>(.*))/(?P<candidate_company>(.*))/(?P<candidate_location>(.*))',views.duplicateCandidate,name='duplicateCandidate'),
    
]


