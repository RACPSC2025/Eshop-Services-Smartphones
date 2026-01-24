from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from apps.orders.models import Order
from apps.products.models import Product, FileResource, Category
from apps.pages.models import Banner, About, Testimonial
from apps.social.models import SocialMedia
from .forms import (
    ProductForm,
    UserForm,
    BannerForm,
    MediaForm,
    CategoryForm,
    AboutForm,
    TestimonialForm,
    SocialMediaForm,
)


class StepAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class DashboardView(StepAdminMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Stats
        # Total Revenue (sum of total for completed orders usually, but taking all non-cancelled/refunded for now or just checking payment_status)
        # Using payment_status=True for revenue
        revenue = (
            Order.objects.filter(payment_status=True).aggregate(Sum("total"))[
                "total__sum"
            ]
            or 0
        )
        context["total_revenue"] = revenue

        # Total Orders
        context["total_orders"] = Order.objects.count()

        # Total Users
        context["total_users"] = User.objects.count()

        # Total Products
        context["total_products"] = Product.objects.count()

        # Recent Orders (Top 10)
        context["recent_orders"] = Order.objects.select_related("user").order_by(
            "-created_at"
        )[:10]

        return context


class AdminProductsView(StepAdminMixin, ListView):
    model = Product
    template_name = "admin/admin_products.html"
    context_object_name = "products"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()
        return context


class CreateProductView(StepAdminMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("admin:admin_products")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(
            self.success_url
        )  # For simplicity in this iteration, validation errors handling can be improved later


class AdminUsersView(StepAdminMixin, ListView):
    model = User
    template_name = "admin/admin_users.html"
    context_object_name = "users"
    ordering = ["-date_joined"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserForm()
        return context


class CreateUserView(StepAdminMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("admin:admin_users")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class AdminOrdersView(StepAdminMixin, ListView):
    model = Order
    template_name = "admin/admin_orders.html"
    context_object_name = "orders"
    ordering = ["-created_at"]


class AdminBannersView(StepAdminMixin, ListView):
    model = Banner
    template_name = "admin/admin_banners.html"
    context_object_name = "banners"
    ordering = ["position", "-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BannerForm()
        return context


class CreateBannerView(StepAdminMixin, CreateView):
    model = Banner
    form_class = BannerForm
    success_url = reverse_lazy("admin:admin_banners")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class AdminMediaView(StepAdminMixin, ListView):
    model = FileResource
    template_name = "admin/admin_media.html"
    context_object_name = "files"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MediaForm()
        return context


class CreateMediaView(StepAdminMixin, CreateView):
    model = FileResource
    form_class = MediaForm
    success_url = reverse_lazy("admin:admin_media")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


# ==================== CATEGORY VIEWS ====================
class AdminCategoriesView(StepAdminMixin, ListView):
    model = Category
    template_name = "admin/admin_categories.html"
    context_object_name = "categories"
    ordering = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CategoryForm()
        return context


class CreateCategoryView(StepAdminMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("admin:admin_categories")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class UpdateCategoryView(StepAdminMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("admin:admin_categories")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)


class DeleteCategoryView(StepAdminMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("admin:admin_categories")


# ==================== ABOUT VIEWS ====================
class AdminAboutView(StepAdminMixin, ListView):
    model = About
    template_name = "admin/admin_about.html"
    context_object_name = "about_entries"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AboutForm()
        return context


class CreateAboutView(StepAdminMixin, CreateView):
    model = About
    form_class = AboutForm
    success_url = reverse_lazy("admin:admin_about")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class UpdateAboutView(StepAdminMixin, UpdateView):
    model = About
    form_class = AboutForm
    success_url = reverse_lazy("admin:admin_about")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)


class DeleteAboutView(StepAdminMixin, DeleteView):
    model = About
    success_url = reverse_lazy("admin:admin_about")


# ==================== TESTIMONIAL VIEWS ====================
class AdminTestimonialsView(StepAdminMixin, ListView):
    model = Testimonial
    template_name = "admin/admin_testimonials.html"
    context_object_name = "testimonials"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TestimonialForm()
        return context


class CreateTestimonialView(StepAdminMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    success_url = reverse_lazy("admin:admin_testimonials")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class UpdateTestimonialView(StepAdminMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    success_url = reverse_lazy("admin:admin_testimonials")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)


class DeleteTestimonialView(StepAdminMixin, DeleteView):
    model = Testimonial
    success_url = reverse_lazy("admin:admin_testimonials")


# ==================== SOCIAL MEDIA VIEWS ====================
class AdminSocialView(StepAdminMixin, ListView):
    model = SocialMedia
    template_name = "admin/admin_social.html"
    context_object_name = "social_media"
    ordering = ["platform"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SocialMediaForm()
        return context


class CreateSocialMediaView(StepAdminMixin, CreateView):
    model = SocialMedia
    form_class = SocialMediaForm
    success_url = reverse_lazy("admin:admin_social")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return redirect(self.success_url)


class UpdateSocialMediaView(StepAdminMixin, UpdateView):
    model = SocialMedia
    form_class = SocialMediaForm
    success_url = reverse_lazy("admin:admin_social")

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.success_url)


class DeleteSocialMediaView(StepAdminMixin, DeleteView):
    model = SocialMedia
    success_url = reverse_lazy("admin:admin_social")
