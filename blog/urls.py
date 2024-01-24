from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("view_article/<int:article_id>", views.view_article, name="view_article"),
    path("view_repository/<str:repository_name>", views.view_repository, name="view_repository"),
    path("author_details/<int:author_id>", views.author_details, name="author_details"),
    path("view_category/<int:category_id>", views.view_category, name="view_category"),
    path("blog", views.blog, name="blog"),
]
