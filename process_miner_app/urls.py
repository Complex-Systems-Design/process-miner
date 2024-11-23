from django.urls import path

from . import views

# definition des namespaces
app_name = 'process_miner_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('loginHandler/', views.login_handler, name='login_handler'),
    path('error/', views.error, name='error_page'),
    path('inputHandler/', views.input_handler, name='input_handler'),
    path('outputHandler/', views.output_handler, name='output_handler'),
    path('logout/', views.logout_handler, name='logout_handler')
]