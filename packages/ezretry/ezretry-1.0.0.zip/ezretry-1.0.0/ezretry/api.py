from ezretry.core import RetryGroup, __retry_internal, check_params
import logging
import functools

_default_logger = logging.getLogger(__name__)


def retry(retry_groups=[RetryGroup()], logger=_default_logger):
    """
    use retry by decorator
    :param retry_groups: retry exception params
    :param logger: print retry logs
    :return: function
    """
    check_params(retry_groups)

    def _inline(func):
        @functools.wraps(func)
        def __inline(*args, **kwargs):
            args = args if args else list()
            kwargs = kwargs if kwargs else dict()
            return __retry_internal(functools.partial(func, *args, **kwargs), retry_groups, logger)

        return __inline

    return _inline


def retry_call(func, f_args=None, f_kwargs=None, retry_groups=[RetryGroup()], logger=_default_logger):
    """
    this equal below usage:
        @decorator(retry_params_list, logger)
        def func(*f_args, **f_kwargs):
            pass
    """
    check_params(retry_groups)

    args = f_args if f_args else list()
    kwargs = f_kwargs if f_kwargs else dict()
    return __retry_internal(functools.partial(func, *args, **kwargs), retry_groups, logger)
