from django.urls import path
from app_post import views
from django.contrib.auth import views as auth_views

app_name = "app_post"


urlpatterns = [
    path('', views.home, name='home'),
    path('my_post', views.my_post, name='my_post'),
    path('post_details/<int:id>', views.post_details, name='post_details'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:id>/', views.update_post, name='update_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),

    # authentication url patterns
    path('signup/', views.sign_up, name='signup'),

    path('login/', auth_views.LoginView.as_view(template_name='registrations/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]