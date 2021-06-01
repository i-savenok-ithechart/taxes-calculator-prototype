

def get_connection_queries():
    from project.settings import TEST_MODE
    if not TEST_MODE:
        raise Exception('get_connection_queries() must be used only for testing.')
    from django.conf import settings
    settings.DEBUG = True
    from django.db import connection
    return connection.queries


class InfinityLimit:
    def __le__(self, other): return True if isinstance(other, InfinityLimit) else False
    def __lt__(self, other): return False
    def __ge__(self, other): return True
    def __gt__(self, other): return False if isinstance(other, InfinityLimit) else True
    def __eq__(self, other): return True if isinstance(other, InfinityLimit) else False
