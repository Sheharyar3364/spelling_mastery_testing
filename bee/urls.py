from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('puzzle', views.PuzzleView)
router.register('answer', views.AnswerView)


urlpatterns = [
    path('', include(router.urls)),
    path('puzzle/<int:id>/', views.PuzzleView.as_view({'get': 'retrieve'}), name='puzzle-detail'),
    path('answer/by-puzzle/<int:puzzle_id>/', views.AnswerView.as_view({'get': 'by_puzzle'}), name='answer-by-puzzle'),
]