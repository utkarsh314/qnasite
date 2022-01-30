from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('question/<int:pk>', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/answer/', views.NewAnswerView.as_view(), name='new_answer'),
    path('question/new/', views.NewQuestionView.as_view(), name='new_question'),
    path('question/<int:pk>/update/', views.EditView.as_view(), name='edit_question'),
    path('question/<int:pk>/delete/', views.DeleteQView.as_view(), name='delete_question'),
    path('question/<int:question_id>/upvote/', views.upvote, name='upvote'),
    path('question/<int:question_id>/downvote/', views.downvote, name='downvote'),
    path('question/<int:question_id>/removevote/', views.removevote, name='removevote'),
    path('<int:answer_id>/upvote/', views.answerupvote, name='answerupvote'),
    path('<int:answer_id>/downvote/', views.answerdownvote, name='answerdownvote'),
    path('<int:answer_id>/removeanswervote/', views.removeanswervote, name='removeanswervote'),
]