from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
