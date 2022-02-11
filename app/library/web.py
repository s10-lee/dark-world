import aiohttp
import base64
import xmltodict
import orjson
import collections

response_object_creator = collections.namedtuple('response_namedtuple', ['status', 'headers', 'content_type', 'data'])


def generate_basic_auth(first, second):
    return base64.b64encode(f"{first}:{second}".encode("utf-8")).decode("utf-8")


async def parse_response_text(resp: aiohttp.ClientResponse, as_content_type: str = None):
    content = await resp.text()

    if as_content_type == 'xml':
        return parse_xml(content)

    if as_content_type == 'json':
        return parse_json(content)

    return content


async def get_request_binary(url, method='get', **kwargs) -> response_object_creator:
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, ssl=False, **kwargs) as resp:
            return response_object_creator(
                status=resp.status,
                headers=dict(resp.headers),
                content_type=resp.content_type,
                data=await resp.read()
            )


async def make_request(url, method='get', data_format=None, **kwargs) -> response_object_creator:
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, ssl=False, **kwargs) as resp:
            return response_object_creator(
                status=resp.status,
                headers=dict(resp.headers),
                content_type=resp.content_type,
                data=await parse_response_text(resp, as_content_type=data_format)
            )


def parse_xml(content):
    return xmltodict.parse(content)


def parse_json(content):
    return orjson.loads(content)


# BS4
async def parse_bs4(page):
    import bs4
    soup = bs4.BeautifulSoup(page, 'html.parser')
    soup.prettify()
    return soup


# lxml.html
def parse_html_lxml(content):
    import lxml.html
    return lxml.html.fromstring(content)
