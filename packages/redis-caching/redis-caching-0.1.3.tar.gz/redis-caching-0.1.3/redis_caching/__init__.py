from aioredis import Redis
from functools import wraps
from typing import Callable, Any, Optional
import dill
import inspect


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

    async def clear(self, arg: Optional[str] = None) -> None:
        if arg is not None:
            arg_serialized = dill.dumps(obj=arg)
            for key in await self.redis.mget(key=arg_serialized):
                if key is not None:
                    await self.redis.delete(key=key)
            await self.redis.delete(key=arg_serialized)
        else:
            await self.redis.flushdb()

    def __call__(self, pre_serialize_coro: Optional[Callable] = None,
                 post_deserialize_coro: Optional[Callable] = None, store_by_arg: Optional[str] = None) -> Callable:
        def decorator(coro: Callable) -> Callable:
            module_coro_key = (inspect.getsourcefile(object=coro) + coro.__name__).encode(encoding='ascii')

            @wraps(coro)
            async def wrapper(*args, **kwargs) -> Any:
                args_key = dill.dumps(obj=args) + dill.dumps(obj=kwargs)
                key = module_coro_key + args_key
                value = await self.redis.get(key)
                if value is None:
                    result = await coro(*args, **kwargs)
                    result_for_serialization = (await pre_serialize_coro(result)
                                                if pre_serialize_coro is not None else
                                                result)
                    result_serialized = dill.dumps(obj=result_for_serialization)
                    await self.redis.set(key=key, value=result_serialized)
                    if store_by_arg is not None:
                        arg_values = inspect.getargvalues(inspect.currentframe())
                        try:
                            arg = arg_values.locals[store_by_arg]
                        except KeyError:
                            arg = arg_values.locals['kwargs'][store_by_arg]
                        arg_serialized = dill.dumps(obj=arg)
                        await self.redis.append(key=arg_serialized, value=key)
                else:
                    result_deserialized = dill.loads(str=value)
                    result = (await post_deserialize_coro(result_deserialized)
                              if post_deserialize_coro is not None else
                              result_deserialized)
                return result

            return wrapper

        return decorator
