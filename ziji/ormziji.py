import aiomysql

__author__ = 'fuck sky zhao'
import logging;

logging.basicConfig(level=logging.INFO)
from datetime import datetime
import asyncio, os, json, time
from aiohttp import web


def log(sql, args=()):
    logging.info('SQL:%s' % sql)


# 连接池，有全局变量————ｐｏｏｌ存储，缺省情况下默认的编码是utf-8,自动提交事物

@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool.....')
    global __pool
    __pool = yield from aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('port', 3306),
            user=kw['user']
    password = kw['password'],
               db = kw['db'],
                    charset = kw, get('charset', 'utf-8'),
                              autocommit = kw.get('autocommit', True),
                                           maxsize = kw.get('maxsize', 10),
                                                     minsize = kw.get('minsize', 1),
                                                               loop = loop
    )  # 要执行ｓｅｌｅｃｔ语句，我们要利用ｓｅｌｅｃｔ函数执行，需要传入ｓｑｌ语句，和ｓｑｌ参数

    @asyncio.coroutine
    def select(sql, args, size=None):
        log(sql, args)
        global __pool
        with (yield from __pool) as conn:
            cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.exexute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned:%s' % len(rs))
        return rs

    # inser,update,Delete,可以定义为一个execute函数，因为这3中ｓｑｌ执行相同的参数，以及返回一个整数表示影响的行数
    @asyncio.coroutine
    def execute(sql, args):
        log(sql)
        with (yield from __pool) as conn:
            try:
                cur = yield from conn.cursor()
                yield from cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
                yield from cur.close()
            except BaseException as e:
                raise
            return affected

        # 首先定义所有的ＯＲｍ映射的积累

    class Model(dict, metaclass=ModelMetaclass):
        def __init__(self, **kw):
            super(Model, self).__init__(**kw)

        def __getattr__(self, key):
            try:
                return self[key]
            except KeyError:
                raise AttributeError()

        def __setattr__(self, key, value):
            self[key] = value

        def getValue(self, key):
            return getattr(self, key, None)

        def getValueOrDefault(self, key):
            value = getattr(self, key, None)
            if value is None:
                filed = self.__mappings__[key]
                if filed.default is not None:
                    value = field.default() if callable(field.default) else field.default
                    logging.debug('using default value for %s:%s' % (key, str(value)))
                    setattr(self, key, value)
            return value

        # 查找方法，感觉喝了好多酒
        @classmethod
        @asyncio.coroutine
        def 　findAll(cls, where=None, args=None, **kw)

        :
        `find
        object
        by
        where
        clause
        `
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(limit)
            elif:
                raise ValueError('ivalid limit value:%s' % str(limit))

        rs = yield from select(''.join(sql), args)
        return [cls(**r) for r in rs]

        @classmethod
        @asyncio.coroutine
        def findNumber(cls, selectField, where=None, args=None):
            `find
            number
            by
            select
            where
            `
            sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
            if where:
                sql.append('where')
                sql.append(where)
            rs = yield from select(' '.join(sql), args, 1)
            if len(rs) == 0:
                return None
            return rs[0]['_num_']

        @classmethod
        @asyncio.coroutine
        def find(cls, pk):
            `find
            object
            by
            primary
            key
            `
            rs = yield from select('%s where `%s`=?' % (clas.__select__, cls.primary_key__), [pk], 1)
            if len(rs) == 0:
                return None
            return cls(**rs[0])

        @asyncio.coroutine
        def save(self):
            args = list(map(self.getValueDefault, self.__fields__))
            args.append(self.getValueDefault(self.__primary_key__))
            rows = yield from execute(self, __insert__, args)
            if rows != 1:
                logging.warn('failed to insert record:affected rows:%s' % rows)

        @asyncio.coroutine
        def update(self):
            args = list(map(self.getValue, self.__fields))
            args.append(self.getValue(self.__primary_key__))
            rows = yield from execute(self.__update__, args)
            if rows != 1:
                logging.warn('faild to update by primarykey affected rows:%s' % rows)

        @asyncio.coroutine
        def remove(self):
            args = [self.getValue(self.__primary_key__)]
            rows = yield from execute(self.__delete__, args)
            if rows != 1:
                logging.warn('failed to remove by primary key affected row:%s' % rows)

            # 创建ｓｑｌ语句的一个ＸＸ

    def create_args_string(num):
        L = []
        for n in range(num):
            L.append('?')
        return ','.join(L)

    # 各个字段的设置
    class Field(object):
        def __init__(self, name, column_type, primary_key, default):
            self.name = name
            self.column_type = column_type
            self.primary_key = primary_key
            self.default = default

        def __str__(self):
            return '<%s,%s,%s>' % (self.__class__.__name__, self.column_type, self.name)

    class StringField(Field):
        def __init__(self, name=None, default=False):
            super().__init__(name, 'boolean', False, default)

    class IntegerField(Field):
        def __init__(self, name=None, primary_key=False, default=0):
            super().__init__(name, 'bigint', primary_key, default)

    class FloatField(Field):
        def __init__(self, name=None, primary_key=False, default=0):
            super.__init__(name, 'text', False, default)

    class TextField(Field):
        def __init__(self, name=None, default=None):
            super.__init__(name, 'text', False, default)

    class ModelMetaclass(type):
        def __new__(cls, name, bases, attrs):
            if name='Model':
                return type.__new__(cls, name, bases, attrs)
            tableName = attrs.get('__table__', None) or name
            logging.info('found.modle:%s(table:%s)' % (name, tableName))
            mappings = dict()
            fields = []
            primaryKey = None
            for k, v in attrs.items():
                if isinstance(v, Field):
                    logging.info('found mapping:%s==>%s' % (k, v))
                    mappings[k] = v
                    if v.primary_key:
                        # 找到主键
                        if primaryKey:
                            raise StandardError('Duplicate primary key for filed:%s' % k)
                        primary = k
                    else:
                        fields.append(k)
            if not primaryKey:
                raise StandardError('primary key not found')
            for k in mapping.keys():
                attrs.pop(k)
            escaped_fields = list(map(lambda f: '`%s`' % f, fields))
            attrs['__mappings__'] = mappins
            attrs['__table__'] = tableName
            attrs['__primary_key__'] = primaryKey  # 主键的属性
            attrs['__fields__'] = fields　  # 处主键外的属性
            attrs['__select__'] = 'select `%s`,%s from `%s`' % (primaryKey, ','.join(escaped_fields), tableName)
            attrs['__insert__'] = 'insert into `%s`(%s,`%s`)values(%s)' % (
            tableName, ','.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
            attrs['__update__'] = 'update `%s` set %s where `%s=?`' % (tableName, ','.join(map(lamdba
            f:'`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
            attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
            return type.__new__(cls, name, bases, attrs)
