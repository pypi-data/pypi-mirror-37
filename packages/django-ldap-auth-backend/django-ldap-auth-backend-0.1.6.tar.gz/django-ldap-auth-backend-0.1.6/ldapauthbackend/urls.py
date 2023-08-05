from django.conf.urls import url

from . import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^candidate-members$', views.CandidateMembers.as_view(), name='candidate-members'),
		url(r'^import-member$', views.ImportMember.as_view(), name='import-member'),
		url(r'^sync-profile$', views.SyncProfile.as_view(), name='sync-profile'),
]
