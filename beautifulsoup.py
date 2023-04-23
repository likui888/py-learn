from bs4 import BeautifulSoup, SoupStrainer

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
<p>and they lived at the bottom of a well.<p>11</p></p>
<p class="story" id="11">...</p>
"""

only_a_tags = SoupStrainer("a")

only_tags_with_id_link2 = SoupStrainer(id="link2")


def is_short_string(string):
    return len(string) < 10


only_short_strings = SoupStrainer(string=is_short_string)


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


soup = BeautifulSoup(html, 'lxml', parse_only=only_a_tags)
for tag in soup.find_all():
    tag.clear()
    tag.string = "11"
    print(tag)
# print(soup.find(attrs={"class": "story", "id": "11"})["class"])
# print(soup.find_all(string="Lacie"))
