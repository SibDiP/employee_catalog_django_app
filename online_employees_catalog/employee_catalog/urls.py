from django.urls import path
from . import views

app_name = 'employee_catalog'
urlpatterns = [
    path('', views.TreeView.as_view(), name='catalog_tree'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail')
]

from django.urls import path




# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]