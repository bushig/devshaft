from django.conf.urls import url

from .views import (
    # TutorialList,
    TutorialLikesCreateView
)

urlpatterns = [
        # url(r'^$', TutorialList.as_view(), name='tutorials-list'),
        url(r'^(?P<id>[\d]+)/likes/$', TutorialLikesCreateView.as_view(), name='tutorials-likes'),

]