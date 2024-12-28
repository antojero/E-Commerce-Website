from django.urls import path
from shop import views
urlpatterns = [
    path("",views.display,name="display"),
    path("register/",views.register,name="register"),
    path("login/",views.login_page,name="login"),
    path("logout/",views.logout_page,name="logout"),
    path("cart_page/",views.cart_page,name="cart_page"),
    path("remove_from_cart/<id>",views.remove_from_cart,name="remove_from_cart"),
    path("collections/",views.collections,name="collections"),
    path("collectionsview/<str:name>",views.collectionsview,name="collectionsview"),
    path("productview/<str:cname>/<str:pname>",views.productview,name="productview"),
    path("addtocart/",views.add_to_cart,name="addtocart"),
]
