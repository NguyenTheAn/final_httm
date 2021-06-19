from django.urls import path
from .views import *


app_name = "ecomapp"
urlpatterns = [

    # Client side pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("review/", SendReview.as_view(), name="review"),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("update-wishlist-<int:pro_id>/", UpdateToWishList.as_view(), name="updateWishList"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("register/",
         CustomerRegistrationView.as_view(), name="customerregistration"),

    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
    path("reviewlist/", ReviewListView.as_view(), name="reviewlist"),
    path("review-success/", ReviewSuccessView.as_view(), name="reviewsuccess"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),

    path("search/", SearchView.as_view(), name="search"),
    path("edit-profile/<int:usr_id>/", EditProfileView.as_view(), name="editprofile"),
    path("shipping-address/<int:cus_id>/", ShippingAddressListView.as_view(), name="shippingaddresslist"),
    path("shipping-address/create/<int:cus_id>/", ShippingAddressCreateView.as_view(), name="shippingaddresscreate"),
    path("shipping-address/edit/<int:cus_id>/<int:addr_id>/", ShippingAddressEditView.as_view(), name="shippingaddressedit"),
    path("shipping-address/delete/<int:cus_id>/<int:addr_id>/", ShippingAddressDeleteView.as_view(), name="shippingaddressdelete"),
    

    path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",
         PasswordResetView.as_view(), name="passwordreset"),
#     # Admin Side pages

    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-review/", AdminReviewListView.as_view(), name="adminreviewlist"),
    path("admin-review/<int:pk>/", AdminReviewDetailView.as_view(),
         name="adminreviewdetail"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-reply/", AdminReplyReviewView.as_view(), name="adminreplyreview"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),
         name="adminorderdetail"),

    path("admin-product-detail/<int:pro_id>/", AdminProductDetailView.as_view(), name="adminproductdetail"),
    path("admin-item-detail/<slug:slug>/", AdminItemDetailView.as_view(), name="adminitemdetail"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),

    path("admin-order-<int:pk>-change/",
         AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),

    path("admin-product/list/", AdminProductListView.as_view(),
         name="adminproductlist"),
     path("admin-item/list/", AdminItemListView.as_view(),
         name="adminitemlist"),
     path("admin-importingrecord/list/", AdminImprotingrecordListView.as_view(),
         name="adminimportingrecordlist"),
     path("admin-product/delete-<int:pro_id>", AdminProductDeleteView.as_view(),
         name="adminproductdelete"),
    path("admin-product/add/", AdminProductCreateView.as_view(),
         name="adminproductcreate"),

    path("admin-product/import/", AdminImportProductView.as_view(),
         name="adminimportproduct"),

]
