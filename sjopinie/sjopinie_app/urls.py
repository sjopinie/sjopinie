from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'api/opinions', views.OpinionViewSet, basename='opinions')
router.register(r'api/lecturers', views.LecturerViewSet, basename='lecturers')
router.register(r'api/subjects', views.SubjectViewSet, basename="subjects")
router.register(r'api/tags', views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('lecturer/<int:id>/', views.lecturer),
    path('subject/<int:id>/', views.subject),
    path('new/lecturer/', views.LecturerCreateView.as_view()),
    path('new/opinion/', views.OpinionCreateView.as_view()),
    path('new/subject/', views.SubjectCreateView.as_view()),
]
