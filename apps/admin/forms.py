from django import forms
from django.contrib.auth.models import User
from apps.products.models import Product, FileResource, Category
from apps.pages.models import Banner, About, Testimonial
from apps.social.models import SocialMedia
from apps.orders.models import Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "description",
            "image",
            "catalog_type",
            "tag",
            "rating",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "rows": 4,
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "catalog_type": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "tag": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
            }
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
            "password",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "is_staff": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
            "is_superuser": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        else:
            # Preserve existing password if not changing
            if user.pk:
                from django.contrib.auth.models import User
                original_user = User.objects.get(pk=user.pk)
                user.password = original_user.password
        if commit:
            user.save()
        return user


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["title", "image", "link", "is_active", "position"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "link": forms.URLInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
            "position": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
        }


class MediaForm(forms.ModelForm):
    class Meta:
        model = FileResource
        fields = ["title", "file", "is_active"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "file": forms.FileInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "additional_info", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "additional_info": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "rows": 3,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ["title_info", "content", "is_active"]
        widgets = {
            "title_info": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["user", "comment", "rating", "is_active"]
        widgets = {
            "user": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "rows": 4,
                }
            ),
            "rating": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "min": 1,
                    "max": 5,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ["platform", "url", "icon", "is_active"]
        widgets = {
            "platform": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "url": forms.URLInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "icon": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "placeholder": "e.g., fab fa-facebook",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-xiaomi bg-gray-100 border-gray-300 rounded focus:ring-xiaomi focus:ring-2"
                }
            ),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status", "payment_method", "notes"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "payment_method": forms.Select(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:border-xiaomi transition-colors",
                    "rows": 3,
                }
            ),
        }
