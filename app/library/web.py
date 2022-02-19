import aiohttp
import base64
import xmltodict
import orjson
import collections
from lxml import html
from pprint import pp
import typing
from typing import Union, TypeVar
from yarl import URL


class HttpResponse:
    def __init__(
            self,
            url: URL,
            status: int,
            encoding: str,
            content_type: str,
            headers: dict = None,
            body: Union[str, bytes, dict, list] = None,
    ) -> None:
        self.url = url
        self.status = status
        self.encoding = encoding
        self.content_type = content_type
        self.headers = headers
        self.body = body

    @classmethod
    async def prepare_body(
            cls,
            client_response: aiohttp.ClientResponse,
            raw_body: bool = None,
            convert_to: str = None
    ):
        if raw_body:
            return await client_response.read()
        return await convert_http_response_body(client_response, convert_to=convert_to)

    @classmethod
    async def from_client_response(
            cls,
            client_response: aiohttp.ClientResponse,
            raw_body: bool = None,
            convert_to: str = None
    ) -> "HttpResponse":

        if raw_body:
            body = await client_response.read()
        else:
            body = await convert_http_response_body(client_response, convert_to=convert_to)

        return cls(
            url=client_response.url,
            status=client_response.status,
            encoding=client_response.get_encoding(),
            content_type=client_response.content_type,
            headers=dict(client_response.headers),
            body=body,
        )


MyResponse = TypeVar('MyResponse', bound=HttpResponse)


async def response_object_factory(
        client_response: aiohttp.ClientResponse,
        raw_body: bool = False,
        convert_to: str = None
) -> "HttpResponse":
    return await HttpResponse.from_client_response(client_response, raw_body=raw_body, convert_to=convert_to)


response_object_creator = collections.namedtuple(
    'response_namedtuple', [
        'url', 'status', 'encoding', 'content_type', 'headers', 'body'
    ]
)


def generate_basic_auth(first, second):
    return base64.b64encode(f"{first}:{second}".encode("utf-8")).decode("utf-8")


async def convert_http_response_body(
        resp: aiohttp.ClientResponse,
        convert_to: str = None
) -> Union[str, dict, list]:
    content = await resp.text()
    if convert_to == 'xml':
        return convert_xml_to_dict(content)
    if convert_to == 'json':
        return convert_json_to_dict(content)
    return content


# async def prepare_http_response_body(
#         resp: aiohttp.ClientResponse,
#         raw_body: bool = False,
#         convert_to: str = None
# ) -> Union[bytes, str, dict, list]:
#     if raw_body:
#         return await resp.read()
#     return await convert_http_response_body(resp=resp, convert_to=convert_to)


async def send_http_request(
        url,
        method='get',
        raw: bool = False,
        convert_to: str = None,
        debug: bool = False,
        **kwargs,
) -> "HttpResponse":

    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, ssl=False, **kwargs) as resp:
            response = await response_object_factory(resp, raw_body=raw, convert_to=convert_to)

            # response = response_object_creator(
            #     url=resp.url,
            #     status=resp.status,
            #     encoding=resp.get_encoding(),
            #     headers=dict(resp.headers),
            #     content_type=resp.content_type,
            #     body=await prepare_http_response_body(resp, raw=raw, convert_to=convert_to),
            # )

            if debug:
                print('-' * 50)
                print(response.status, response.url)
                print(response.content_type, ' = ', response.encoding)
                pp(response.headers)
                print(type(response.body))
                print(len(response.body))
                print('-' * 50)

            return response


async def get_http_request(url, **kwargs):
    kwargs['method'] = 'get'
    return await send_http_request(url, **kwargs)


def convert_xml_to_dict(content) -> dict:
    return xmltodict.parse(content)


def convert_json_to_dict(content) -> dict:
    return orjson.loads(content)


# lxml.html
def parse_html_response(html_content: str, pattern: str):
    return html.fromstring(html_content).xpath(pattern)
