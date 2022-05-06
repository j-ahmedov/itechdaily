from django.urls import path
from .views import *
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>', get_category, name='category'),
    path('read/<int:news_id>', read_news, name='read'),
    path('contact', contact_us, name='contact'),
    path('about', about, name='about'),


    # --------------urls for API-----------------------------------
    path('get-api', GetNewsView.as_view(), name='get-api'),
    path('get-api/category/<int:category_id>', get_by_category, name='get-api-category')

]

urlpatterns += doc_urls