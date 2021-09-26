from app.library.web import make_request_json
from app.src.grabber.models import GrabberRequest, GrabberResponse


async def prepare_request(pk: int = None, request: GrabberRequest = None):
    if pk:
        request = await GrabberRequest.get(id=pk)



