from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
import requests
import markdown
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from . import models
from cms import models as cmsmodel

GITHUB_USERNAME = "AyushAryal"

REQUESTS_CACHE = {}

def skills_view(request):
    skills = cmsmodel.Skill.objects.all()
    return render(request, 'blog/home.html', {'skills': skills})


def set_base_path(soup, base_path):
    img_tags = soup.find_all("img", src=True)
    for img_tag in img_tags:
        src = img_tag["src"]
        if not src.startswith(("http://", "https://", "//")):
            img_tag["src"] = urljoin(base_path, src)
    return soup


def make_image_responsive(soup):
    img_tags = soup.find_all("img", src=True)
    for img_tag in img_tags:
        img_tag["class"] = img_tag.get("class", []) + ["img-fluid"]
    return soup


def render_markdown(content, base_url):
    content = base64.b64decode(content).decode()
    rendered_readme = markdown.markdown(content, extensions=["codehilite", "extra"])
    soup = BeautifulSoup(rendered_readme, "html.parser")
    set_base_path(soup, base_url)
    make_image_responsive(soup)
    return str(soup)


def home(request):
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    if url not in REQUESTS_CACHE:
        response = requests.get(url)
        if response.status_code == 200:
            REQUESTS_CACHE[url] = response.json()
        else:
            REQUESTS_CACHE[url] = []

    github_profile_readme = (
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_USERNAME}/readme"
    )
    if github_profile_readme not in REQUESTS_CACHE:
        response = requests.get(github_profile_readme)
        if response.status_code == 200:
            REQUESTS_CACHE[github_profile_readme] = response.json()
        else:
            REQUESTS_CACHE[github_profile_readme] = {"content": ""}

    base_url = (
        f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_USERNAME}/master/"
    )
    rendered_readme = render_markdown(
        REQUESTS_CACHE[github_profile_readme]["content"], base_url
    )
    skills = cmsmodel.Skill.objects.all()
    cv = cmsmodel.Cv.objects.first()

    return render(
        request,
        "blog/home.html",
        {
            "article_list": models.Article.objects.all(),
            "repository_list": REQUESTS_CACHE[url],
            "github_profile_readme": rendered_readme,
            "skills": skills,
            "cv": cv,
        },
    )


def view_repository(request, repository_name):
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repository_name}/readme"
    if repository_name not in REQUESTS_CACHE:
        response = requests.get(url)
        if response.status_code == 200:
            REQUESTS_CACHE[url] = response.json()
        else:
            return redirect(
                f"https://github.com/{GITHUB_USERNAME}/{repository_name}",
            )

    base_url = (
        f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repository_name}/master/"
    )
    rendered_readme = render_markdown(REQUESTS_CACHE[url]["content"], base_url)

    return render(
        request,
        "blog/view_repository.html",
        {
            "url": f"https://github.com/{GITHUB_USERNAME}/{repository_name}",
            "readme": rendered_readme
        },
    )


def view_article(request, article_id):
    article = get_object_or_404(models.Article, id=article_id)
    return render(request, "blog/view_article.html", {"article": article})


def author_details(request, author_id):
    author = get_object_or_404(models.Author, pk=author_id)
    return render(request, "blog/author_details.html", {"author": author})


def view_category(request, category_id):
    category = get_object_or_404(models.Tag, pk=category_id)
    return render(request, "blog/view_category.html", {"category": category})


def blog(request):
    return render(
        request, "blog/blog.html", {"article_list": models.Article.objects.all()}
    )


