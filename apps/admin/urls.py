from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="admin_dashboard"),
    path("products/", views.AdminProductsView.as_view(), name="admin_products"),
    path("products/create/", views.CreateProductView.as_view(), name="create_product"),
    path("users/", views.AdminUsersView.as_view(), name="admin_users"),
    path("users/create/", views.CreateUserView.as_view(), name="create_user"),
    path("banners/", views.AdminBannersView.as_view(), name="admin_banners"),
    path("banners/create/", views.CreateBannerView.as_view(), name="create_banner"),
    path("media/", views.AdminMediaView.as_view(), name="admin_media"),
    path("media/create/", views.CreateMediaView.as_view(), name="create_media"),
    path("orders/", views.AdminOrdersView.as_view(), name="admin_orders"),
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
