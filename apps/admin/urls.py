from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("panel/", views.DashboardView.as_view(), name="admin_dashboard"),
    # Products
    path("products/", views.AdminProductsView.as_view(), name="admin_products"),
    path("products/create/", views.CreateProductView.as_view(), name="create_product"),
    path(
        "products/<int:pk>/edit/",
        views.UpdateProductView.as_view(),
        name="edit_product",
    ),
    path(
        "products/<int:pk>/delete/",
        views.DeleteProductView.as_view(),
        name="delete_product",
    ),
    # Users
    path("users/", views.AdminUsersView.as_view(), name="admin_users"),
    path("users/create/", views.CreateUserView.as_view(), name="create_user"),
    path(
        "users/<int:pk>/edit/",
        views.UpdateUserView.as_view(),
        name="edit_user",
    ),
    path(
        "users/<int:pk>/delete/",
        views.DeleteUserView.as_view(),
        name="delete_user",
    ),
    # Orders
    path("orders/", views.AdminOrdersView.as_view(), name="admin_orders"),
    path(
        "orders/<int:pk>/edit/",
        views.UpdateOrderView.as_view(),
        name="edit_order",
    ),
    path(
        "orders/<int:pk>/detail/",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "orders/<int:pk>/delete/",
        views.DeleteOrderView.as_view(),
        name="delete_order",
    ),
    path(
        "orders/<int:pk>/status/<str:status>/",
        views.UpdateOrderStatusView.as_view(),
        name="update_order_status",
    ),
    # Banners
    path("banners/", views.AdminBannersView.as_view(), name="admin_banners"),
    path("banners/create/", views.CreateBannerView.as_view(), name="create_banner"),
    path(
        "banners/<int:pk>/edit/",
        views.UpdateBannerView.as_view(),
        name="edit_banner",
    ),
    path(
        "banners/<int:pk>/delete/",
        views.DeleteBannerView.as_view(),
        name="delete_banner",
    ),
    # Media
    path("media/", views.AdminMediaView.as_view(), name="admin_media"),
    path("media/create/", views.CreateMediaView.as_view(), name="create_media"),
    path(
        "media/<int:pk>/edit/",
        views.UpdateMediaView.as_view(),
        name="edit_media",
    ),
    path(
        "media/<int:pk>/delete/",
        views.DeleteMediaView.as_view(),
        name="delete_media",
    ),
    # Categories
    path("categories/", views.AdminCategoriesView.as_view(), name="admin_categories"),
    path(
        "categories/create/", views.CreateCategoryView.as_view(), name="create_category"
    ),
    path(
        "categories/<int:pk>/edit/",
        views.UpdateCategoryView.as_view(),
        name="edit_category",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.DeleteCategoryView.as_view(),
        name="delete_category",
    ),
    # About
    path("about/", views.AdminAboutView.as_view(), name="admin_about"),
    path("about/create/", views.CreateAboutView.as_view(), name="create_about"),
    path("about/<int:pk>/edit/", views.UpdateAboutView.as_view(), name="edit_about"),
    path(
        "about/<int:pk>/delete/", views.DeleteAboutView.as_view(), name="delete_about"
    ),
    # Testimonials
    path(
        "testimonials/",
        views.AdminTestimonialsView.as_view(),
        name="admin_testimonials",
    ),
    path(
        "testimonials/create/",
        views.CreateTestimonialView.as_view(),
        name="create_testimonial",
    ),
    path(
        "testimonials/<int:pk>/edit/",
        views.UpdateTestimonialView.as_view(),
        name="edit_testimonial",
    ),
    path(
        "testimonials/<int:pk>/delete/",
        views.DeleteTestimonialView.as_view(),
        name="delete_testimonial",
    ),
    # Social Media
    path("social/", views.AdminSocialView.as_view(), name="admin_social"),
    path("social/create/", views.CreateSocialMediaView.as_view(), name="create_social"),
    path(
        "social/<int:pk>/edit/",
        views.UpdateSocialMediaView.as_view(),
        name="edit_social",
    ),
    path(
        "social/<int:pk>/delete/",
        views.DeleteSocialMediaView.as_view(),
        name="delete_social",
    ),
]

