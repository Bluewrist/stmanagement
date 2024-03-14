from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('create_product',views.create_product,name='create_product'),
    path('deleteRoom/<int:pk>/',views.deleteRoom,name='deleteRoom'),
    path('product_detail/<str:pk>/',views.product_detail,name='product_detail'),
    path('product_list',views.product_list,name='product_list'),
    path('updateStore/<int:id>/',views.updateStore,name='updateStore'),
    path('all_cat',views.all_cat,name='all_cat'),
    path('add_cat',views.add_cat,name='add_cat'),
    path('all_type',views.all_type,name='all_type'),
    path('add_type',views.add_type,name='add_type'),
    path('all_dist',views.all_dist,name='all_dist'),
    path('add_dist',views.add_dist,name='add_dist'),
    path('sales',views.sales,name='sales'),
    path('dist_detail/<int:pk>/',views.dist_detail,name='dist_detail'),
    path('return_to_wherehouse/<int:pk>/',views.return_to_wherehouse,name='return_to_wherehouse'),
    path('history',views.history,name='history'),
    path('logout_process',views.logout_process,name='logout_process'),
    path('login_process',views.login_process,name='login_process'),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    
]