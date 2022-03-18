from django.urls import include, path, re_path
from rest_framework import routers
from . import views

from allauth.account import views as auth_views

router = routers.DefaultRouter()
router.register(r'api/opinions', views.OpinionViewSet, basename='opinions')
router.register(r'api/lecturers', views.LecturerViewSet, basename='lecturers')
router.register(r'api/subjects', views.SubjectViewSet, basename="subjects")
router.register(r'api/tags', views.TagViewSet)
router.register(r'api/vote', views.VoteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.home_page, name='home'),
    #REST API
    path('', include(router.urls)),
    #Accounts and Authentication
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path("login/", auth_views.login, name="account_login"),
    path('signup/', auth_views.signup, name="account_signup"),
    path("inactive/", auth_views.account_inactive, name="account_inactive"),
    # E-mail
    path(
        "confirm-email/",
        auth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        auth_views.confirm_email,
        name="account_confirm_email",
    ),
    #App usage
    path('lecturer/<int:id>/', views.lecturer),
    path('subject/<int:id>/', views.subject),
    path('search/<str:query>', views.search),
    path('new/lecturer/', views.LecturerCreateView.as_view()),
    path('new/opinion/', views.OpinionCreateView.as_view()),
    path('new/subject/', views.SubjectCreateView.as_view()),
]
