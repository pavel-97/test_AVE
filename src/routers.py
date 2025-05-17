import json

from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

from .pyds import SPhone


router = APIRouter(
    prefix=""
)


@router.get("/check_data")
async def get(phone: int):
    redis_backend = FastAPICache.get_backend()
    return await redis_backend.get(phone)


@router.post("/write_data")
@cache(expire=10)
async def create(data: Annotated[SPhone, Depends()]):
    redis_backend = FastAPICache.get_backend()
    await redis_backend.set(data.phone, data.model_dump_json())
    return {
        "phone": data.phone,
        "address": data.address
    }


@router.patch("/write_data")
async def update(data_phone: int, data: Annotated[SPhone, Depends()]):
    redis_backend = FastAPICache.get_backend()
    cache = await redis_backend.get(data_phone)
    if cache is not None:
        cache = json.loads(cache)
        cache.update(**data.model_dump())
        await redis_backend.clear(key=data_phone)
        await redis_backend.set(cache.get("phone"), json.dumps(cache))
        return cache
    return cache