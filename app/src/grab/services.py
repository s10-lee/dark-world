from app.library.web import make_request, make_session, parse_xml, parse_json
from app.src.grabber.models import GrabberProject, GrabberRequest, GrabberResponse
from jsonpath_ng import parse


def replace_variables(string: str, variables: dict):
    for search, replace in variables.items():
        string = string.replace('{' + search + '}', str(replace))
    return string


def convert_response_to_dict(source_type, response_body: str):
    converters = {
        'JSON': parse_json,
        'XML': parse_xml,
    }
    if source_type in converters:
        return converters[source_type](response_body)
    return response_body


async def prepare_request(pk: int = None, request: GrabberRequest = None, variables: dict = None):
    if pk:
        request = await GrabberRequest.get(id=pk)
    if not request:
        raise RuntimeError('Request is null')

    result = {
        'method': request.method,
        'url': request.url,
        'params': request.params,
        'headers': request.headers,
        'data': request.data,
    }

    if variables:
        # URL
        result['url'] = replace_variables(request.url, variables)
        # Params
        if request.params:
            result['params'] = {name: replace_variables(value, variables) for name, value in request.params.items()}
        # Headers
        if request.headers:
            result['headers'] = {name: replace_variables(value, variables) for name, value in request.headers.items()}
        # Data
        if request.data:
            result['data'] = {name: replace_variables(value, variables) for name, value in request.data.items()}

    return result


async def parse_response_data(request: GrabberRequest, response_data: dict, variables: dict = None):
    await request.fetch_related('parsers')

    for parser in request.parsers:
        result = dict()
        to_vars = parser.variables
        jsonpath_expr = parse(parser.rule)

        for match in jsonpath_expr.find(response_data):
            parsed = match.value
            path = str(match.path)

            if isinstance(parsed, dict) and parser.keys:
                _item = dict()
                for k in parser.keys:
                    _item[k] = parsed[k]
                if to_vars and k in to_vars:
                    variables[k] = parsed[k]
            else:
                _item = parsed

            if path not in result.keys():
                result[path] = list()

            if parser.one:
                result = _item
            else:
                result[path].append(_item)

