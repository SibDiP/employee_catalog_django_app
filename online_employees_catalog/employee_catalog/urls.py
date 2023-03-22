from django.urls import path
from .views import employee_tree

app_name = 'employee_catalog'
urlpatterns = [
    path('', employee_tree, name='employee_tree'),
    # path('<int:pk>/', specific_employee_tree, name='specific_employee_tree')
]




# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]