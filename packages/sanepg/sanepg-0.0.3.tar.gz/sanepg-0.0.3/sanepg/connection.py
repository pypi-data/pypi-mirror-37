
import asyncio
import functools

import tornado.ioloop

import sanepg

try:
    import psycopg2
    psycopg2.extensions.POLL_OK
except Exception:
    raise ImportError('Please upgrade psycopg2') from None


class _Connection:
    def __init__(self, dsn,
            connectionFactory = None,
            cursorFactory     = None,
            ):
        self._dsn  = dsn
        self._conn = None
        self._fd   = None

        self.connectionFactory = connectionFactory
        self.cursorFactory     = cursorFactory

        self._ioloop = tornado.ioloop.IOLoop.current()

        self._options = {
            'async' : True,
            }

    def connect(self):
        self._conn = psycopg2.connect(self._dsn, **self._options)
        self._fd = self._conn.fileno()

        future   = asyncio.Future()
        callback = functools.partial(self._callback, future, self)
        self._ioloop.add_handler(self._fd, callback, tornado.ioloop.IOLoop.WRITE)

        def _check_exception(future):
            if future.exception():
                self._conn = None
                self._fd   = None

        self._ioloop.add_future(future, _check_exception)
        return future

    def execute(self, future, statement, *args):
        #kwargs = {"cursor_factory": cursor_factory} if cursor_factory else {}
        cursor = self._conn.cursor(cursor_factory = self.cursorFactory)
        try:
            cursor.execute(statement, args)
        except psycopg2.ProgrammingError as e:
            raise sanepg.SaneError('%s', e) from None

        callback = functools.partial(self._callback, future, cursor)
        self._ioloop.add_handler(self._fd, callback, tornado.ioloop.IOLoop.WRITE)
        return future

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            self._fd   = None

    def _callback(self, future, result, fd, events):
        try:
            state = self._conn.poll()
        except (psycopg2.OperationalError,psycopg2.ProgrammingError) as e:
            self._ioloop.remove_handler(self._fd)
            future.set_exception(sanepg.SaneError('%s', e))
            return

        if state == psycopg2.extensions.POLL_OK:
            self._ioloop.remove_handler(self._fd)
            future.set_result(result)
        elif state == psycopg2.extensions.POLL_READ:
            self._ioloop.update_handler(self._fd, tornado.ioloop.IOLoop.READ)
        elif state == psycopg2.extensions.POLL_WRITE:
            self._ioloop.update_handler(self._fd, tornado.ioloop.IOLoop.WRITE)
        else:
            future.set_exception(sanepg.SaneError('unknown state: %s', state))
