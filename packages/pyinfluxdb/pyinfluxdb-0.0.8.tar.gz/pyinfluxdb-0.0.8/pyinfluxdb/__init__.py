import logging
from datetime import datetime, timedelta

import pytz
from dateutil import parser
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)


class InfluxClient(InfluxDBClient):
    def __init__(self,
                 host='localhost',
                 port=8086,
                 username='root',
                 password='root',
                 database=None,
                 timezone='Asia/Shanghai',
                 **kwargs
                 ):
        super().__init__(host, port, username, password, database, timeout=10, **kwargs)
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__timezone = timezone
        self.__kwargs = kwargs

        self._database_list = self.get_list_database()
        logger.debug(self._database_list)

    def connect_to_database(self, name):
        return Database(host=self.__host,
                        port=self.__port,
                        username=self.__username,
                        password=self.__password,
                        database=name,
                        timezone=self.__timezone,
                        **self.__kwargs
                        )

    def __getattr__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            raise AttributeError(
                "Database has no attribute %r. To access the %s"
                " collection, use database[%r]." % (name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        if {'name': name} not in self._database_list:
            self.create_database(name)
        return self.connect_to_database(name)


class Database(InfluxDBClient):
    def __init__(self,
                 host='localhost',
                 port=8086,
                 username='root',
                 password='root',
                 database=None,
                 timezone='Asia/Shanghai',
                 **kwargs
                 ):
        super().__init__(host, port, username, password, database, timeout=10, **kwargs)
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__kwargs = kwargs
        self._measurements_list = self.get_list_measurements()
        logger.debug(self._measurements_list)
        pass

    def get_measurement(self, name):
        tz = pytz.timezone('Asia/Shanghai')
        return Measurement(self, name, timezone=tz)

    def __getattr__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            raise AttributeError(
                "Database has no attribute %r. To access the %s"
                " collection, use database[%r]." % (name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        return self.get_measurement(name)


def time_to_local(time_in):
    time = parser.parse(time_in)
    time_local = time + timedelta(hours=-8)
    time_out = time_local.strftime('%Y-%m-%d %H:%M:%S')
    return time_out


class Measurement(object):
    FIND_ONE_BASE = 'SELECT * FROM {condition} ORDER BY time DESC LIMIT 1;'
    FIND_BASE = 'SELECT * FROM {condition} ORDER BY time DESC;'
    key_words = ['name', 'key']

    def __init__(self, database, name, timezone):
        if not isinstance(name, str):
            raise TypeError("name must be an instance "
                            "of %s" % (str.__name__,))

        if not name or ".." in name:
            raise Exception("collection names cannot be empty")
        if "$" in name and not (name.startswith("oplog.$main") or
                                name.startswith("$cmd")):
            raise Exception("collection names must not "
                            "contain '$': %r" % name)
        if name[0] == "." or name[-1] == ".":
            raise Exception("collection names must not start "
                            "or end with '.': %r" % name)
        if "\x00" in name:
            raise Exception("collection names must not contain the "
                            "null character")

        self.__database = database
        self.__name = name
        self.__timezone = timezone

    def insert_one(self, tags, fields):
        point = dict(
            fields=fields,
            tags=tags,
            measurement=self.__name
        )

        return self.__database.write_points([point])

    def _find(self, select='*', filter=None, desc=True, groupby=None, limit=None, slimit=None, **kwargs):
        condition = '{measurement}'.format(measurement=self.__name)
        if filter is not None:
            condition += ' WHERE ' + filter
        other = ''
        if groupby is not None:
            other += 'GROUP BY {groupby} '.format(groupby=groupby)
        if limit is not None:
            other += 'LIMIT {limit} '.format(limit=limit)
        if slimit is not None:
            other += 'SLIMIT {slimit} '.format(slimit=slimit)

        # other += " tz('{}')".format(self.__timezone)
        sql_str = 'SELECT {select} FROM {condition} ORDER BY time {order} {other};'.format(
            select=select,
            condition=condition,
            order='DESC' if desc else 'ASC',
            other=other
        )
        logger.debug(sql_str)

        rs = self.__database.query(sql_str)

        return rs

    def find_one(self, filter):
        for k in filter.keys():
            if k in self.key_words:
                raise Exception('key {} is keyword'.format(k))
        kwargs_str_list = ["{} = '{}'".format(k, v) for k, v in filter.items()]
        condition = '{measurement}'.format(measurement=self.__name)
        if kwargs_str_list:
            kwargs_str = ' AND '.join(kwargs_str_list)
            condition += ' WHERE {where}'.format(where=kwargs_str)
        sql_str = self.FIND_ONE_BASE.format(condition=condition)
        logger.debug(sql_str)
        rs = self.__database.query(sql_str)
        if rs is None:
            return None
        points = list(rs.get_points(measurement=self.__name))
        if not points:
            return None
        point = points[0]
        return point

    def find(self, filter, desc=True, limit=None, slimit=None):
        kwargs_str_list = list()
        for k, v in filter.items():
            if k in self.key_words:
                raise Exception('key {} is keyword'.format(k))
            if isinstance(v, str):
                value = v
                if k == 'time':
                    value = time_to_local(v_f)
                kwargs_str_list.append("{} = '{}'".format(k, value))
                continue
            if isinstance(v, dict):
                for k_f, v_f in v.items():
                    if k_f in ['>', '<', '>=', '<=']:
                        value = v_f
                        if k == 'time':
                            value = time_to_local(v_f)
                        kwargs_str_list.append("{} {} '{}'".format(k, k_f, value))
                continue
        # kwargs_str_list = ["{} = '{}'".format(k, v) for k, v in filter.items()]
        kwargs_str = None
        if kwargs_str_list:
            kwargs_str = ' AND '.join(kwargs_str_list)

        rs = self._find(filter=kwargs_str, desc=desc, limit=limit, slimit=slimit)
        if rs is None:
            return None
        points = list(rs.get_points(measurement=self.__name))
        if not points:
            return []
        return points

    # def FILL(self, filter, desc=True, groupbytime=None, groupbytag=None):
    #
    #     for k in filter.keys():
    #         if k in self.key_words:
    #             raise Exception('key {} is keyword'.format(k))
    #     kwargs_str_list = ["{} = '{}'".format(k, v) for k, v in filter.items()]
    #     # condition = '{measurement}'.format(measurement=self.__name)
    #     kwargs_str = None
    #     if kwargs_str_list:
    #         kwargs_str = ' AND '.join(kwargs_str_list)
    #
    #     if groupbytime is not None:
    #         groupby = 'time({time}),*'.format(time=groupbytime)
    #
    #     if groupbytag is not None and len(groupbytag) == 2:
    #         groupby = 'tag({tag}),{value}'.format(time=groupbytag[0], value=groupbytag[1])
    #
    #     rs = self._find(filter=kwargs_str, desc=desc, groupby=groupby)
    #     if rs is None:
    #         return None
    #     points = list(rs.get_points(measurement=self.__name))
    #     if not points:
    #         return []
    #     return points
