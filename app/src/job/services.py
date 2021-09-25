from app.src.job.models import Result, Job, Step


async def save_job_result(**kwargs):
    return await Result.create(**kwargs)


async def start_job(pk: int):
    item = await Job.get(id=pk).select_related()
    return item
