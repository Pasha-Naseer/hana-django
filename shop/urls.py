from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path("", views.shop_index, name="shop_index"),
    path("products/<int:collection_id>/", views.products_index, name="products_index"),
    path("products/<int:collection_id>/<int:product_id>/", views.products_detail, name="products_detail"),
    path('about/', views.about, name='about'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    # Used2B
    # path('register/', views.user_register, name='register'),
    # is
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),

    path('update/', views.user_update, name='update'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password', views.update_password, name='update_password'),
    path('search/', views.search, name='search'),
    path("blog/", views.blog, name='blog'),
    path('blog/<str:blog_id>/', views.blog_detail, name='blog_detail'),
]
