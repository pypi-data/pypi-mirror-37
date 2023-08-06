from shortesttrack_tools.unique import Unique


class LoggerRegistry(Unique):
    logger_ids: set = None

    @classmethod
    def _do_init(cls, *args, **kwargs):
        cls.logger_ids = set()
