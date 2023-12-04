from django.urls import path
from . import views
from .views import CustomLogin, RegisterPage, TaskUpdate, TaskCreate, TaskDelete
from django.contrib.auth.views import LogoutView



urlpatterns=[
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('task-details/<int:pk>', views.task_details, name='task-details' ),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update' ),
    path('task-create/', TaskCreate.as_view(), name='task-create' ),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete' ),
    
]