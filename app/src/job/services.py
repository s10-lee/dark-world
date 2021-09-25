from app.src.job.models import Result, Job, Step
from app.library.web import make_request_json


async def save_job_result(**kwargs):
    return await Result.create(**kwargs)


async def get_job(pk: int):
    item = await Job.get(id=pk)
    await item.fetch_related("steps")
    return item


async def execute_code_block(code, callback_name='run', **kwargs):
    _locals = dict()
    _globals = {
        'make_request_json': make_request_json,
        'save_job_result': save_job_result,
    }
    exec(code, _globals, _locals)
    func = _locals[callback_name]
    return await func(**kwargs)


async def start_job(pk: int):
    job = await get_job(pk)
    kwargs = await execute_code_block(job.code)

    for step in job.steps:
        kwargs = await execute_code_block(step.code, **kwargs)

