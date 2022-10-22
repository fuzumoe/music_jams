from django.urls import path, include

from rest_framework import routers, viewsets

from music_jam.jams.views.music_jam_view import MusicJamViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from music_jam.jams.views.user_performer_view import PerformersViewSet
from music_jam.jams.views.user_pofile_view import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'performers', PerformersViewSet)
router.register(r'profiles', ProfileViewSet, )
router.register(r'jams', MusicJamViewSet, )
urlpatterns = [
    path('', include(router.urls)),
    path('schema', SpectacularAPIView.as_view(), name="schema"),
    path('docs',
         SpectacularSwaggerView.as_view(
             template_name='swagger-ui.html', url_name='schema'
         ),
         name="swagger-ui",
         ),
]
