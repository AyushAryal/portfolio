from django import template
from bs4 import BeautifulSoup

register = template.Library()


@register.filter()
def responsive_image(html):
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all("img", src=True)
    for img_tag in img_tags:
        img_tag["class"] = img_tag.get("class", []) + ["img-fluid"]
    return str(soup)
