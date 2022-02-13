from lxml import etree, html
from app.library.web import make_request


async def grab_from_pinterest(url):
    resp = await make_request(url)
    return html.fromstring(resp.data).xpath('//head/link[@as="image"]/@href').pop()


async def grab_from_dribble(url):
    resp = await make_request(url)
    return html.fromstring(resp.data).xpath('//head/meta[@property="og:image"]/@content').pop()
