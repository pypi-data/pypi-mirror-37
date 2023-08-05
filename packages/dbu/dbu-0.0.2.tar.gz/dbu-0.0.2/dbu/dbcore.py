""" db_core 180903_2140
        180809_1100
        171203_2100
"""

import logging
import time
import psycopg2
import psycopg2.errorcodes

from tittles import mod
_t = mod.Mod("tittles.tittles")


def mods_rld(recursive=False):
    _t.reload()
    # Nothing to reload recursively
    if recursive: pass


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(module)s:%(lineno)d(%(funcName)s) %(message)s", level=logging.DEBUG)
_log = logging.getLogger(__name__)


RECONNECT_ATTEMPTS = 0
RECONNECT_PAUSE = 500
PG_DEFAULT_PORT = "5432"


def _debug_stmt(**kwargs):
    if kwargs.get("debug") == "statement" and not kwargs.get("no_logging"): return True


def db_apply_commit(ctx, **kwargs):
    for cn_ in ctx:
        conn_ = ctx[cn_]
        if conn_["stmt"] and kwargs.get("apply"):
            conn_["conn"].execute_batch(conn_["stmt"], **kwargs)
        if kwargs.get("commit"):
            conn_["conn"].commit()
        if conn_["stmt"] and kwargs.get("info"):
            if len(conn_["stmt"]) > 1:
                _log.info("CONN: %s; STMT:%s", conn_["conn"], "\n%s;" % ";\n".join(conn_["stmt"]))
            else:
                _log.info("CONN: %s; STMT: %s;", conn_["conn"], conn_["stmt"][0])
        conn_["stmt"] = []


class Db():
    """DB connection class with core functions"""

    def __init__(self, parms, **kwargs):
        self.__conn = None
        self.__user = None
        self.__pass = None
        self.__dbname = None
        self.__host = None
        self.__port = None
        self.__set_parms(parms, **kwargs)

    def __str__(self):
        return "%s @ %s : %s / connected=%s; id=%s" % (
            self.__user == self.__dbname and self.__user or "%s(%s)" % (self.__user, self.__dbname),
            self.__host, self.__port, self.is_connected(), hex(id(self)), )

    def __set_parms(self, parms, **kwargs):
        changed_ = 0

        def __set_if_changed(current_val, dic, key, default=None):
            nonlocal changed_
            changed_val_ = _t.m.nvl(dic.get(key, default), default)
            if changed_val_ and changed_val_ != current_val:
                changed_ += 1
                return changed_val_
            return current_val

        # USER
        self.__user = __set_if_changed(self.__user, parms, "USER")
        if not self.__user:
            raise _t.m.ConfigError("USER is not defined")
        # PASSWORD
        self.__pass = __set_if_changed(self.__pass, parms, "PASSWORD")
        if not self.__pass:
            raise _t.m.ConfigError("PASSWORD is not defined")
        # DB
        self.__dbname = __set_if_changed(
            self.__dbname, parms, "DATABASE",
            kwargs.get("default_db_equals_user") and self.__user or "postgres")
        # HOST
        self.__host = __set_if_changed(self.__host, parms, "HOST", "localhost")
        # PORT
        self.__port = __set_if_changed(self.__port, parms, "PORT", PG_DEFAULT_PORT)

        return True if changed_ else False

    def set_parms(self, parms, **kwargs):
        """Set connection parameters"""
        if self.__set_parms(parms, **kwargs):
            # Close connection if any parameter updated
            self.close(**kwargs)

    def encoding(self):
        """Get DB encoding"""
        return self.__get_conn().encoding

    def connect(self, **kwargs):
        """Create new database connection"""
        if _debug_stmt(**kwargs):
            _log.debug("Connect to %s; reopen=%s", self, kwargs.get("reopen", False))
        if self.is_connected():
            # If reopen - close connection
            if kwargs.get("reopen"):
                self.close(**kwargs)
            # Nothing to do - already connected
            else:
                return self.__conn
        try:
            self.__conn = psycopg2.connect(
                "".join([
                    "host=", self.__host,
                    " dbname=", self.__dbname,
                    " user=", self.__user,
                    " password=", self.__pass,
                    " port=", self.__port,
                ])
            )
        except psycopg2.Error as e_:
            raise _t.m.DbConnectError("Can't connect to %s: %s" % (self, e_))
        return self.__conn

    def __get_conn(self, **kwargs):
        if not self.__conn: self.connect(**kwargs)
        return self.__conn

    def is_connected(self):
        if self.__conn and self.__conn.closed == 0: return True
        return False

    def close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None
        return self

    def commit(self):
        if self.__conn: self.__conn.commit()
        return self

    def rollback(self):
        if self.__conn: self.__conn.rollback()
        return self

    def cursor(self, **kwargs):
        return self.__get_conn(**kwargs).cursor()

    def cursor_close(self, cursor):
        if cursor: cursor.close()

    def __select(self, stmt, args, **kwargs):
        csr_ = self.cursor(**kwargs)
        csr_.execute(stmt, args)
        return csr_

    def __execute(self, stmt, args, **kwargs):
        csr_ = None
        try:
            csr_ = self.cursor(**kwargs)
            csr_.execute("begin")
            csr_.execute("savepoint svp_" + hex(id(csr_)))
            csr_.execute(stmt, args)
            return csr_.rowcount
        except Exception:
            if csr_:
                csr_.execute("rollback to svp_" + hex(id(csr_)))
            raise
        finally:
            self.cursor_close(csr_)

    def __exec_reconn_wrapper(self, stmt, args, exec_func, **kwargs):
        # Retrieve number of attempts and pause between them
        attempts_ = kwargs.get("reconnect_attempts", RECONNECT_ATTEMPTS)
        pause_ = kwargs.get("reconnect_pause", RECONNECT_PAUSE)

        # Compose statement
        stmt_ = _t.m.lovts(stmt)
        if _debug_stmt(**kwargs):
            _log.debug("STMT [%s] ARGS %s (attempts=%s, pause=%s, id=%s)", stmt_, args, attempts_, pause_, hex(id(self)))

        # Do execute several times
        while attempts_ >= 0:
            try:
                return exec_func(stmt_, args, **kwargs)

            except psycopg2.Error as e_:

                # Check ignore error function
                def __ignore_errs(e_, **kwargs):
                    if e_.pgcode:
                        ignore_errs_ = kwargs.get("ignore_errs")
                        if ignore_errs_ and (e_.pgcode in ignore_errs_):
                            return True

                # In case of error in ignore list - do nothing, simply return
                if __ignore_errs(e_, **kwargs):
                    if not kwargs.get("no_logging"):
                        _log.warning(
                            ("Can't execute (ignored) STMT [%s] ARGS %s"
                             " (connected=%s, pgcode=%s, class=%s, id=%s): %s"),
                            stmt_, args, self.is_connected(), e_.pgcode,
                            e_.__class__.__name__, hex(id(self)), e_)
                    return

                # If error not related to closed connection
                # or number of attemts exhausted - raise exception
                if not self.__get_conn().closed or attempts_ <= 0:
                    raise _t.m.msg_exc(("Can't execute STMT [%s] ARGS %s / connected=%s; pgcode=%s; class=%s; id=%s: %s") % (stmt_, args, self.is_connected(), e_.pgcode, e_.__class__.__name__, hex(id(self)), e_))
                    # raise _t.m.DbExecuteError((
                    #     "Can't execute STMT [%s] ARGS %s"
                    #     " (connected=%s, pgcode=%s, class=%s, id=%s): %s") % (
                    #         stmt_, args, self.is_connected(),
                    #         e_.pgcode, e_.__class__.__name__, hex(id(self)), e_))

                # ... else log warning and keep trying execution
                if not kwargs.get("no_logging"):
                    _log.warning(
                        ("Can't execute (will try again) STMT [%s] ARGS %s"
                         " (connected=%s, pgcode=%s, class=%s, id=%s): %s"),
                        stmt_, args, self.is_connected(),
                        e_.pgcode, e_.__class__.__name__, hex(id(self)), e_)

                time.sleep(pause_ / 1000.0)
                # do reconnect
                self.connect(reopen=True, **kwargs)
                attempts_ -= 1

    def select(self, stmt, args=None, **kwargs):
        return self.__exec_reconn_wrapper(stmt, args, self.__select, **kwargs)

    def select_one(self, stmt, args=None, **kwargs):
        csr_ = None
        try:
            csr_ = self.select(stmt, args, **kwargs)
            return csr_.fetchone()
        finally:
            if csr_: csr_.close()

    def select_all(self, stmt, args=None, **kwargs):
        csr_ = None
        try:
            csr_ = self.select(stmt, args, **kwargs)
            return csr_.fetchall()
        finally:
            if csr_: csr_.close()

    def execute(self, stmt, args=None, **kwargs):
        rowcount_ = self.__exec_reconn_wrapper(stmt, args, self.__execute, **kwargs)
        if kwargs.get("commit") == "statement": self.commit()
        return rowcount_

    def execute_batch(self, batch, **kwargs):
        rowcount_ = -1
        for s_ in batch: rowcount_ += self.execute(s_, **kwargs)
        if kwargs.get("commit") == "batch": self.commit()
        return rowcount_

    def __del__(self):
        self.rollback()
        self.close()


def test():
    # import time

    db_parms_ = {
        "USER": "database-user",
        "PASSWORD": "password",
    }

    conn_ = Db(db_parms_, default_db_equals_user=True, debug="statement")
    conn_.connect(debug="statement")

    conn_.execute("create table xx (i integer, t text)")
    conn_.execute("insert into xx (i, t) values (1, 'text 1')")
    conn_.execute("insert into xx_ (i, t) values (2, 'text 2')", ignore_errs=("42P01",))
    conn_.execute("insert into xx (i, t) values (3, 'text 3')")
    _log.debug("RESULTS:")
    for r_ in conn_.select_all("select * from xx"):
        _log.debug("R: %s", (r_, ))

    # _log.debug("setting parms without changes...")
    # conn_.set_parms(db_parms_, default_db_equals_user=True)
    #
    # _log.debug("setting changed parms...")
    # conn_.set_parms(db_parms_)
    # conn_.connect(debug="statement")
    #
    # time.sleep(20) # kill DB connection during the pause
    #
    # conn_.execute(
        # "DROP TABLE NON_EXISTENT_TABLE",
        # ignore_errs=(psycopg2.errorcodes.UNDEFINED_TABLE),
        # reconnect_attempts=1, debug="statement")

    # csr_ = None
    # try:
    #     csr_ = db_.select("select * from t_records where id = %s", (10, ), debug="statement")
    #     for r_ in csr_.fetchall():
    #         _log.debug("record: %s" % (r_,))
    # finally: csr_ and csr_.close()


if __name__ == "__main__":
    test()
