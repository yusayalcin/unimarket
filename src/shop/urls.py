from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path("categories/<category>/", views.cat, name="category"),
    path("product/<title>/", views.product, name="product"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("create_post/", views.create_post, name="create_post"),
    path("my-items/", views.my_items, name="my-items"),
    path("profile/", views.profile, name="profile"),
    path("profile/activation/", views.profile_activation, name="profile_activation"),
    path("search/", views.MySearchView.as_view(), name="search_view"),
]

# for static in dev mod
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
