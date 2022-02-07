import aiohttp
import base64
import xmltodict
import orjson
import collections

response_object_creator = collections.namedtuple('response_namedtuple', ['status', 'headers', 'content_type', 'data'])


def generate_basic_auth(first, second):
    return base64.b64encode(f"{first}:{second}".encode("utf-8")).decode("utf-8")


async def decode_response_data(resp: aiohttp.ClientResponse, data_format: str = None):
    if data_format == 'xml':
        data = parse_xml(await resp.text())
    elif data_format == 'json':
        data = parse_json(await resp.text())
    elif data_format == 'binary':
        data = await resp.read()
    else:
        data = await resp.text()
    return data


async def make_request(url, data_format=None, **kwargs) -> response_object_creator:
    kwargs['method'] = kwargs.get('method', 'get')
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, ssl=False, **kwargs) as resp:
            return response_object_creator(
                status=resp.status,
                headers=dict(resp.headers),
                content_type=resp.content_type,
                data=await decode_response_data(resp, data_format=data_format)
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
