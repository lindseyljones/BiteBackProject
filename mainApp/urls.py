from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.main_page, name="index"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("index/", views.main_page, name="index"),
    path("profile", views.profile, name="profile"),
    path("explore", views.explore, name="explore"),
    path("settings", views.settings, name="settings"),
    path("create_post/", views.createpost, name="createpost"),
    path("edit_profile", views.editprofile, name="editprofile"),
    path("documents/", views.document_view, name="document_view"),
    path("documents/<int:pk>/", views.post_detail, name="post_detail"),
    path("update_status/<int:pk>/", views.update_status, name="update_status"),
    path(
        "update_message/<int:pk>/",
        views.update_resolution_message,
        name="update_resolution_message",
    ),
    path("my_posts/", views.myposts, name="myposts"),
    path("delete/<int:pk>/", views.custom_delete.as_view(), name="delete"),
    path("anonymous-access/", views.anonymous_access, name="anonymous_access"),
    path("report_post/", views.report, name="report_post"),
    path("submit_report/", views.submit_report, name="submit_report"),
    path("view_reports/", views.view_reports, name="view_reports"),
    path("restaurants/", views.get_restaurants, name="restaurants"),
    path("search_filter/", views.search_filter, name="search-filter"),
    path("clear-search/", views.clear_search, name="clear_search"),
]
