from django.urls import path
from . import shopviews


urlpatterns = [
    path('shop_home',shopviews.home,name='shop_home'),
    path('shop_products',shopviews.product_list,name='shop_products'),
    path('shop_sales',shopviews.sales,name='shop_sales'),
    path('make_sale/<int:id>/',shopviews.make_sale,name='make_sale'),

    
]