import urllib.request
import lxml.html as parser

global msg
def poet():
    url = 'https://autopoet.yandex.ru/'
    html = urllib.request.urlopen(url).read()
    page = html.decode('utf-8')
    doc = parser.document_fromstring(page)
    poem_list  = doc.xpath('/html/body/table/tbody/tr/td[2]/div/div/div[3]/p/text()')
    global msg
    msg ='\n'.join(poem_list)
poet()