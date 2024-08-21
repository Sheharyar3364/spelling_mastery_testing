from django.urls import path, include
from rest_framework import routers
from . import views
from .views import UserGameView

router = routers.DefaultRouter()
router.register('puzzle', views.PuzzleView)
router.register('answer', views.AnswerView)
router.register('user-game', views.UserGameView)


urlpatterns = [
    path('', include(router.urls)),
    path('puzzle/<int:id>/', views.PuzzleView.as_view({'get': 'retrieve'}), name='puzzle-detail'),
    path('unplayed_puzzle/', views.PuzzleView.as_view({'get': 'unplayed'}), name="unplayed-puzzles"),
    path('answer/by-puzzle/<int:puzzle_id>/', views.AnswerView.as_view({'get': 'by_puzzle'}), name='answer-by-puzzle'),
    path('start_game/', views.UserGameView.as_view({'post': 'start_game'}), name='start-game'),
    path('complete_puzzle/', views.UserGameView.as_view({'post': 'complete_puzzle'}), name='complete-puzzle'),
    path('skip_puzzle/', views.UserGameView.as_view({'post': 'skip_puzzle'}), name='skip-puzzle'),
    path('add_word/', views.UserGameView.as_view({'post': 'add_word'}), name='add-word'),
    path('fetch_found_words/<int:gameid>/', UserGameView.as_view({'get': 'fetch_found_words'}), name='fetch-found-words'),
]