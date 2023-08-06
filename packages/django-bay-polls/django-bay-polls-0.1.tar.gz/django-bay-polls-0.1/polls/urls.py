from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # i.e: polls/index
    path('', views.IndexView.as_view(), name='index'),
    # i.e: polls/views
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # i.e: polls/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # i.e: polls/question
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
