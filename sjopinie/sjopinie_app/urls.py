from django.urls import include, path
from rest_framework import routers
from . import views

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
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('signup/', views.UserSignUpView.as_view(), name="signup"),
    #App usage
    path('lecturer/<int:id>/', views.lecturer),
    path('subject/<int:id>/', views.subject),
    path('search/<str:query>', views.search),
    path('new/lecturer/', views.LecturerCreateView.as_view()),
    path('new/opinion/', views.OpinionCreateView.as_view()),
    path('new/subject/', views.SubjectCreateView.as_view()),
]
