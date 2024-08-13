from django.urls import path, include
from rest_framework import routers
from . import views

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
]

# {"refresh":
#  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTMyMDMyMCwiaWF0IjoxNzIzNTQ0MzIwLCJqdGkiOiIzNzY3OTBjYzY0ZTY0ZGNkYTQ0MjM2YmE5MTI4NTYwNiIsInVzZXJfaWQiOjMsImVtYWlsIjoic2hlaGFyeWFyQGdtYWlsLmNvbSIsIm5hbWUiOiJTaGVoYXJ5YXIiLCJsZXZlbCI6Mn0.jX0jT7iJE_LYbkajydiBbeoG5k5e-_IX2DYKqF21EjU",
#  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzNTQ3OTIwLCJpYXQiOjE3MjM1NDQzMjAsImp0aSI6IjZiYjIyMmU2N2YyNDQyNThhNTVhYjlmOWY0Y2NjMDdhIiwidXNlcl9pZCI6MywiZW1haWwiOiJzaGVoYXJ5YXJAZ21haWwuY29tIiwibmFtZSI6IlNoZWhhcnlhciIsImxldmVsIjoyfQ.Tm94yYBwMiHbEKvh3OYX3sMGZkBvzUsvZxDsncLopms"}