from django.core.cache import cache
from .manager import FeatureList
from .base import FeatureBase, functional_handler_factory
import types


__version__ = '0.1.0'


handlers = FeatureList()


__all__ = [
    'handlers',
    'feature_enabled',
    'autodiscover',
    'FeatureBase',
    'register'
]


def feature_enabled(name, request):
    if not getattr(request, 'user', None):
        return False

    def a():
        u = request.user.is_authenticated
        return u() if callable(u) else u

    if a():
        cachekey = 'feature.%s.enabled.%s' % (
            name,
            request.user.username
        )

        if cachekey in cache:
            return cache.get(cachekey)
    else:
        cachekey = None

    if name not in handlers._features:
        return False

    klass, groups = handlers._features.get(name)
    feature = klass(name, groups)
    value = feature.enabled(request)

    if cachekey:
        cache.set(cachekey, value)

    return value


def register(name, *groups):
    def wrapper(kls):
        if isinstance(kls, types.FunctionType):
            handlers.register(
                name,
                functional_handler_factory(kls),
                *groups
            )
        else:
            handlers.register(name, kls, *groups)

        return kls

    return wrapper
