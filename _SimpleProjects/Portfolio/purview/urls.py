from django.urls import path
from purview import views

urlpatterns = [
    path('', views.purview_index, name='home'),
    path('blog/', views.purview_blog, name='blog')
]
