from fastapi import Depends, APIRouter
from app.src.grab.services import filter_json
from app.src.scrape.models import Request, Collection, Step, Parser, Variable
from app.src.scrape import schemas, services
from app.src.auth.services import get_current_user_id
from app.library.web import send_http_request, parse_html_response, convert_data_to_json, convert_json_to_dict
from uuid import UUID


router = APIRouter(tags=['HTTP Collection'])


@router.get('/ws-collection/{pk}/')
async def execute_runner(pk: int, user_id: UUID = Depends(get_current_user_id)):
    print('\n\n\r')

    collection = await Collection.get(id=pk, user_id=user_id)

    variables = {}
    steps = await Step.filter(collection_id=pk, collection__user__id=user_id).order_by('id')
    for key, val in await Variable.filter(collection_id=pk).values_list('name', 'value'):
        variables[key] = val

    cr = None
    print('-----')
    for step in steps:

        if step.type == 'request':

            request = await Request.get(id=step.entity_id)

            request_data = {
                'method': request.method,
                'url': request.url,
                'params': filter_json(request.params),
                'headers': filter_json(request.headers),
                'data': request.data,
                'cookies': request.cookies,
            }

            prepared_request = convert_data_to_json(request_data).decode('utf-8')

            for var_name, replace_value in variables.items():
                prepared_request = prepared_request.replace('{{' + var_name + '}}', replace_value)

            prepared_request_data = convert_json_to_dict(prepared_request)

            try:
                cr = await send_http_request(**prepared_request_data)
                print(cr.url, cr.status)
            except Exception as e:
                cr = None
                print('Yep !')

        elif step.type == 'parser':
            parser = await Parser.get(id=step.entity_id)
            action_to_call = None

            print('parser', parser.search_pattern)

            if cr:
                cr_dict = cr.to_dict()
                body = cr_dict.get(parser.search_field)

                parse_result = parse_html_response(body, parser.search_pattern)
                found_value = parse_result[parser.element_index if parser.element_index else 0]

                print(found_value)

                if parser.action == 'action_save_to_variable':
                    action_to_call = services.action_save_to_variable

                if parser.action == 'action_save_img_to_file':
                    action_to_call = services.action_save_img_to_file

                if parser.action_args:
                    await action_to_call(**parser.action_args, variables=variables, data=found_value)
                else:
                    try:
                        await action_to_call(user_id=user_id, url=found_value)
                    except Exception:
                        print(action_to_call.__name__, 'error')
                        pass

        print('\n\r')

    print(variables)

    print('\n\n\r')
    return []


# @router.get('/http-request/{pk}/exec/')
# async def execute_request(pk: UUID, user_id: UUID = Depends(get_current_user_id)):
#     req = await Request.get(id=pk, collection__user__id=user_id)

#
#     request_data = {
#         'method': req.method,
#         'url': req.url,
#         'params': filter_json(req.params),
#         'headers': filter_json(req.headers),
#         'data': req.data,
#         'cookies': req.cookies,
#     }
#
#     prepared_request = orjson.dumps(request_data).decode('utf-8')
#
#     for v in await req.collection.variables.all():
#         replace_value = v.value
#         if v.call:
#             replace_value = GRAB_UTILS.get(v.call)()
#         prepared_request = prepared_request.replace('{{' + v.name + '}}', replace_value)
#
#     for name, callback in GRAB_UTILS.items():
#         prepared_request = prepared_request.replace('{{@' + name + '}}', callback())
#
#     prepared_request_data = orjson.loads(prepared_request.encode('utf-8'))
#
#     cr = await send_http_request(**prepared_request_data, debug=True)
#
#     response = await Response.create(
#         data=cr.json(),
#         request=req,
#     )
#
#     return convert_json_to_dict(response.data)
