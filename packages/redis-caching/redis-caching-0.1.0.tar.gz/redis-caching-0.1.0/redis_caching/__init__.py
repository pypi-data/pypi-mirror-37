from aioredis import Redis
from functools import wraps
from typing import Callable, Any, Optional
import dill
import inspect


__version__ = '0.1.0'


class Cache:
    def __init__(self, redis: Optional[Redis] = None):
        self._redis = None
        self.redis = redis

    @property
    def redis(self) -> Redis:
        return self._redis

    @redis.setter
    def redis(self, value: Redis) -> None:
        self._redis = value

    def __call__(self, pre_serialize_coro: Callable, post_serialize_coro: Callable) -> Callable:
        def decorator(coro: Callable) -> Callable:
            module_coro_key = (inspect.getsourcefile(object=coro) + coro.__name__).encode(encoding='ascii')

            @wraps(coro)
            async def wrapper(*args, **kwargs) -> Any:
                args_key = dill.dumps(obj=args) + dill.dumps(obj=kwargs)
                key = module_coro_key + args_key
                value = await self.redis.get(key)
                if value is None:
                    result = await coro(*args, **kwargs)
                    result_for_serialization = await pre_serialize_coro(result)
                    result_serialized = dill.dumps(obj=result_for_serialization)
                    await self.redis.set(key=key, value=result_serialized)
                else:
                    result_serialized = dill.loads(str=value)
                    result = await post_serialize_coro(result_serialized)
                return result

            return wrapper

        return decorator
