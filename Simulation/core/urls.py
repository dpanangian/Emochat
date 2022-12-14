from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageModelViewSet, ScenarioModeViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
router.register(r'scenario', ScenarioModeViewSet, basename='scenario-api')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', login_required(
        TemplateView.as_view(template_name='core/whatsapp.html')), name='whatsapp'),
    path('simpleui/', login_required(
        TemplateView.as_view(template_name='core/chat.html')), name='simpleui'),
]
