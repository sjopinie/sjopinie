from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'opinions', views.OpinionViewSet, basename='opinions')
router.register(r'lecturers', views.LecturerViewSet, basename='lecturers')
router.register(r'subjects', views.SubjectViewSet, basename="subjects")
router.register(r'tags', views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('subject/<int:id>/', views.subject)
]
