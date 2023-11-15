from django.urls import path
from askinside import views

urlpatterns = [
    path('hot/', views.hot, name="hot_questions"),
    path('ask/', views.new_question, name="new_question"),
    path('settings/', views.settings, name="settings"),
    path('question/<int:question_id>', views.question_page, name="question"),
    path('tag/<str:title>', views.tag, name="uniq_tag")
]
