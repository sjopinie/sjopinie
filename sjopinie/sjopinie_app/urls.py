from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'lecturers', views.LecturerViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'tags', views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('opinion/<int:subject_id>/', views.opinion_of_subject),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('subject/<int:id>/', views.subject)
]
