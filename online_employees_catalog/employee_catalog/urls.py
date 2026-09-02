from django.urls import path
from .views import (employee_catalog_with_pagination, simple,show_employee, 
show_employee_full)

app_name = 'employee_catalog'
urlpatterns = [
    #path('', company_tree, name='company_tree'),
    #path('<int:pk>/', specific_employee_tree, name='specific_employee_tree'),
    path('', employee_catalog_with_pagination, name='employee_catalog_with_pagination'),
    path('<int:employee_id>', employee_catalog_with_pagination, name='employee_catalog_with_pagination'),
    # Учебные пути
    path('simple/', simple, name='simple'),
    path('show_employee/<int:pk>', show_employee, name='show_employee'),
    path('employee_full/<int:pk>', show_employee_full, name='show_employee_full')
]




# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]