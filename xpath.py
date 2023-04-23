from lxml import etree

text = """
<div>
    <ul>
        <li class="pl2"><a href="https://book.douban.com/subject/1007305/">红楼梦</a>
        <li class="pl2"><a href="https://book.douban.com/subject/4913064/">活着</a></li>
        <li class="pl2"><a href="https://book.douban.com/subject/6082808/">百年孤独</a></li>
        <li class="pl1"><a href="https://book.douban.com/subject/4820710/">1984</a></li>
    </ul>
</div>
"""


html = etree.HTML(text)

result = etree.tostring(html,encoding="utf-8")
print(html.xpath('count(//li[not (contains(@class,"pl1"))]/a)'))


