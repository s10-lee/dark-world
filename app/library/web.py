import aiohttp
import base64
import xmltodict
import orjson


def generate_basic_auth(first, second):
    return base64.b64encode(f"{first}:{second}".encode("utf-8")).decode("utf-8")


async def make_request(decoder: callable = None, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(ssl=False, **kwargs) as resp:
            text = await resp.text()
            return {
                # 'request_info': resp.request_info,
                'status': resp.status,
                'headers': resp.headers,
                'content_type': resp.content_type,
                'data': decoder(text) if decoder else text
            }


def make_session(**kwargs):
    return aiohttp.ClientSession(**kwargs)


async def make_request_json(**kwargs):
    return await make_request(decoder=parse_json, **kwargs)


async def make_request_xml(**kwargs):
    return await make_request(decoder=parse_xml, **kwargs)


def parse_xml(content):
    return xmltodict.parse(content)


def parse_json(content):
    return orjson.loads(content)

