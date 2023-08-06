from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from psycopg2.pool import ThreadedConnectionPool


def create_connection_pool(min, max, **kwargs):
    return ThreadedConnectionPool(min, max, **kwargs)


def create_connection_factory(pool):
    @contextmanager
    def factory():
        try: 
            connection = pool.getconn() 
            yield connection
        finally: 
            pool.putconn(connection)

    return factory


def create_cursor_factory(connection_factory):
    @contextmanager
    def factory(commit=False):
        with connection_factory() as c:
            cur = c.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try: 
                yield cur
                if commit:
                     c.commit() 
            finally: 
                cur.close()

    return factory
