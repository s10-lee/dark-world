from .models import Link
from datetime import timedelta, datetime
from fastapi.exceptions import HTTPException
from app.src.functions import generate_unique_string


async def create(url: str):
    code = generate_unique_string()
    item = await Link.filter(url=url).first()
    if item:
        return item
    check = await check_rate_limit()
    if not check:
        raise HTTPException(status_code=429, detail='Too Many Requests')
    item = await Link.create(url=url, code=code)
    return item


async def check_rate_limit():
    items = await Link.all().limit(5).order_by('-created_at').values_list('created_at', flat=True)
    if len(items) <= 1:
        return True
    print(len(items))
    limit = datetime.now()
    limit += timedelta(hours=-3)
    delta = items[0].replace(tzinfo=None)
    minus = timedelta(seconds=30)
    print('limit', limit)
    print('delta', delta)
    print(limit - delta)
    print(limit - delta > minus)

    return limit - delta > minus


async def receive(code: str):
    return await Link.get(code=code)

