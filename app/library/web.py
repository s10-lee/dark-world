import aiohttp
import base64
import xmltodict
import orjson
from lxml import html
import typing
from enum import Enum
from typing import Union
from yarl import URL


class HttpRequest(aiohttp.ClientRequest):
    def __init__(self, method, url, *args, **kwargs):
        if isinstance(method, Enum):
            method = method.name
        url = URL(url)
        super().__init__(method, url, *args, **kwargs)


class HttpResponse:
    def __init__(
            self,
            method: str,
            url: Union[URL, str],
            status: int,
            encoding: str,
            content_type: str,
            content_disposition: str = None,
            headers: dict = None,
            body: Union[str, bytes, dict, list] = None,
    ) -> None:
        self.method = method
        self.url = url
        self.status = status
        self.encoding = encoding
        self.content_type = content_type
        self.content_disposition = content_disposition
        self.headers = headers
        self.body = body

    @classmethod
    async def prepare_body(
            cls,
            client_response: aiohttp.ClientResponse,
            raw: bool = None,
            convert: str = None,
    ) -> [str, dict, list, bytes]:
        if raw:
            return await client_response.read()

        content = await client_response.text()
        if content:
            if convert == 'xml':
                return convert_xml_to_dict(content)
            if convert == 'json':
                return convert_json_to_dict(content)
        return content

    @classmethod
    async def from_client_response(
            cls,
            client_response: aiohttp.ClientResponse,
            raw: bool = None,
            convert: str = None,
    ) -> "HttpResponse":
        body = await cls.prepare_body(client_response, raw, convert)
        return cls(
            method=str(client_response.method),
            url=str(client_response.url),
            status=client_response.status,
            encoding=client_response.get_encoding(),
            content_type=client_response.content_type,
            content_disposition=client_response.content_disposition,
            headers=dict(client_response.headers),
            body=body,
        )


async def send_http_request(
        method: str,
        url: Union[str, URL],
        raw: bool = False,
        convert: str = None,
        debug: bool = False,
        **kwargs,
) -> "HttpResponse":
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, ssl=False, **kwargs) as resp:
            response = await HttpResponse.from_client_response(resp, raw=raw, convert=convert)

            if debug:
                print('-' * 50)
                print(response.method, response.status, response.url)
                print(response.headers)
                print(type(response.body), len(response.body))
                print('-' * 50)
                print(response.body)
                print('-' * 50)

            return response


def generate_basic_auth(first, second):
    return base64.b64encode(f"{first}:{second}".encode("utf-8")).decode("utf-8")


def convert_xml_to_dict(content) -> dict:
    return xmltodict.parse(content)


def convert_json_to_dict(content: str) -> dict:
    return orjson.loads(content)


def convert_data_to_json(data) -> bytes:
    return orjson.dumps(data)


# lxml.html
def parse_html_response(html_content: str, pattern: str):
    return html.fromstring(html_content).xpath(pattern)
