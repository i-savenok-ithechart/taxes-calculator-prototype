

def get_connection_queries():
    from project.settings import TEST_MODE
    if not TEST_MODE:
        raise Exception('get_connection_queries() must be used only for testing.')
    from django.conf import settings
    settings.DEBUG = True
    from django.db import connection
    return connection.queries
