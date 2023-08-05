# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zsql.py
   Author :       Zhang Fan
   date：         18/10/10
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

try:
    import pymysql as DB
except:
    raise Exception('没有检查到pymysql模块, 请使用pip install pymysql')


def connect(host='localhost', user='root', password='root', db_name=None, charset="utf8"):
    '''连接数据库'''
    return zsql(host=host, user=user, password=password, db_name=db_name, charset=charset)


# 表结构
DescTable = {
    0: 'Field',  # 字段
    1: 'Type',  # 类型
    2: 'Null',  # 允许空值
    3: 'Key',  # 属性
    4: 'Default',  # 默认值
    5: 'Extra'  # 额外
}


class zsql:
    def __init__(self, host='localhost', user='root', password='root', db_name=None, charset="utf8"):
        '''连接数据库(ip地址,用户名,密码,可选 库名,编码)'''
        self._base = DB.connect(host=host, user=user, password=password, database=db_name, charset=charset)
        self._cursor = self._base.cursor()
        self._db_name = db_name
        self._charset = charset
        self.__is_close = False

    def close(self):
        '''关闭'''
        if not self.__is_close:
            self.__is_close = True
            self._cursor.close()
            self._base.close()

    def __del__(self):
        self.close()

    @property
    def is_close(self):
        return self.__is_close

    @property
    def cursor(self):
        return self._cursor

    @property
    def db_name(self):
        return self._db_name

    # region 库操作
    def create_db(self, db_name, charset='utf8', use=True):
        '''创建库(库名,可选 编码)'''
        s = 'CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET={}'.format(db_name, charset)
        self.sql_command(s, True)
        if use:
            self.use_db(db_name)

    def drop_db(self, db_name):
        '''删除库(库名)'''
        s = 'DROP DATABASE IF EXISTS {}'.format(db_name)
        if self._db_name == db_name:
            self._db_name = None
        self.sql_command(s, True)

    def use_db(self, db_name):
        '''使用库(库名)'''
        s = 'USE {}'.format(db_name)
        self._db_name = db_name
        self.sql_command(s, True)

    # endregion

    # region 表操作
    def create_table(self, table_name, *attr, charset='utf8'):
        '''
        创建表\n
        create_table(self,'tablename','ID int','Name char(20)')
        '''
        s = 'CREATE TABLE {} ({}) DEFAULT CHARSET={}'.format(table_name, ', '.join(attr), charset)
        self.sql_command(s, True)

    def create_table_ex(self, table_name, charset='utf8', **fields):
        '''
        创建表\n
        create_table_ex('tablename',ID='int',Name='char(20)')
        '''
        fs = ', '.join(['{} {}'.format(key, value) for key, value in fields.items()])
        s = 'CREATE TABLE {} ({}) DEFAULT CHARSET={}'.format(table_name, fs, charset)
        self.sql_command(s, True)

    def change_table_name(self, table_name, new_name):
        '''修改表名(表名,新表名)'''
        s = 'ALTER TABLE {} RENAME {}'.format(table_name, new_name)
        self.sql_command(s, True)

    def drop_table(self, table_name):
        '''删除表(表名)'''
        s = 'DROP TABLE IF EXISTS {}'.format(table_name)
        self.sql_command(s, True)

    def set_primary(self, table_name, field):
        '''设置主键(表名,字段名)'''
        s = 'ALTER TABLE {} ADD PRIMARY KEY ({})'.format(table_name, field)
        self.sql_command(s, True)

    def drop_primary(self, table_name):
        '''删除主键(表名)'''
        s = 'ALTER TABLE {} DROP PRIMARY KEY'.format(table_name)
        self.sql_command(s, True)

    def set_unique(self, table_name, *fields):
        '''设置字段为unique查询(表名,字段名元组)'''
        s = 'ALTER TABLE {} ADD UNIQUE ({})'.format(table_name, ', '.join(fields))
        self.sql_command(s, True)

    def set_index(self, table_name, field, index_name=None):
        '''创建索引字段'''
        if index_name == None:
            index_name = field

        s = 'CREATE INDEX {} ON {}({})'.format(index_name, table_name, field)
        self.sql_command(s, True)

    # endregion

    # region 数据库结构
    def show_dbs(self):
        '''查看所有库名'''
        s = 'SHOW DATABASES'
        datas = self.select_command(s)
        return [x[0] for x in datas]

    def show_tables(self, db_name=None):
        '''查看一个库的所有表名(可选 库名)'''
        s = 'SHOW TABLES' if db_name == None else 'SHOW TABLES FROM {}'.format(db_name)
        datas = self.select_command(s)
        return [x[0] for x in datas]

    def show_desc(self, table_name):
        '''查看当前库下一个表的结构(表名)'''
        s = 'DESC {}'.format(table_name)
        return self.select_command(s)

    # endregion

    # region 查询数据
    def select(self, tname, *, fields: list or tuple = None, where: None or str or dict = None, groupby=None,
               having=None, orderby=None,
               limit=None):
        '''查询记录(表名,*,(字段1,字段2,字段3),where=条件,limit=选择)'''
        field = ', '.join(fields) if fields else '*'
        where = self._where_to_text(where)
        groupby = '' if groupby == None else ' GROUP BY {}'.format(groupby)
        having = '' if having == None else ' HAVING {}'.format(having)
        orderby = '' if orderby == None else ' ORDER BY {}'.format(orderby)
        limit = '' if limit == None else ' LIMIT {}'.format(limit)
        s = 'SELECT {} FROM {}{}{}{}{}{}'.format(field, tname, where, groupby, having, orderby, limit)
        return self.select_command(s)

    def select_all(self, table_name):
        '''查询一个表的所有记录'''
        s = 'SELECT * FROM {}'.format(table_name)
        return self.select_command(s)

    # endregion

    # region 数据操作
    def save_values(self, table_name, *save_item: list or tuple, commit=True):
        '''添加数据(表名,['id', '用户名', '密码'])'''
        value_text = ', '.join([self._base.escape(item) for item in save_item])
        s = "INSERT INTO {} VALUES {}".format(table_name, value_text)
        self.sql_command(s, commit)

    def save_dict(self, table_name, save_item: dict, commit=True):
        fields, values = [], []
        for key, value in save_item.items():
            fields.append(key)
            values.append(value)

        values_escape = self._base.escape(values)
        field = '({})'.format(', '.join(fields)) if len(fields) > 0 else ''

        s = "INSERT INTO {}{} VALUES {}".format(table_name, field, values_escape)
        self.sql_command(s, commit)

    def del_data(self, table_name, *, where: None or str or dict = None, commit=True):
        '''删除数据(表名,where=条件,是否提交到数据库)'''
        where = self._where_to_text(where)
        s = 'DELETE FROM {}{}'.format(table_name, where)
        self.sql_command(s, commit)

    def update(self, table_name, new_item: dict, *, where: None or str or dict = None, commit=True):
        '''更新数据(表名,新数据,where=条件)'''

        set_values = [
            '{} = {}'.format(key, self._base.escape(value))
            for key, value in new_item.items()
        ]

        where = self._where_to_text(where)
        set_text = ', '.join(set_values)
        s = 'UPDATE {} SET {}{}'.format(table_name, set_text, where)
        self.sql_command(s, commit)

    # endregion

    # region 字段操作
    def add_field(self, table_name, field_name, data_type, after: bool or str = True):
        '''添加字段(表名,字段名,数据类型,位置)位置可以为字段名'''
        if isinstance(after, str):  # 字段后
            after = ' AFTER {}'.format(after)
        elif after:  # 所有字段后
            after = ''
        else:  # 所有字段前
            after = ' FIRST'

        s = 'ALTER TABLE {} ADD {} {}{}'.format(table_name, field_name, data_type, after)
        self.sql_command(s, True)

    def drop_field(self, table_name, field_name):
        '''删除字段(表名,字段名)'''
        s = 'ALTER TABLE {} DROP {}'.format(table_name, field_name)
        self.sql_command(s, True)

    def change_field_type(self, table_name, field_name, data_type):
        '''修改字段数据类型(表名,字段名,数据类型)'''
        s = 'ALTER TABLE {} MODIFY {} {}'.format(table_name, field_name, data_type)
        self.sql_command(s, True)

    def change_field_name(self, table_name, field_name, new_name, data_type):
        '''修改字段名(表名,字段名,新字段名,数据类型)'''
        s = 'ALTER TABLE {} CHANGE {} {} {}'.format(table_name, field_name, new_name, data_type)
        self.sql_command(s, True)

    # endregion

    # region 性能分析
    def on_property(self):
        '''开启性能分析'''
        s = 'SET PROFILING = 1'
        self.sql_command(s)

    def off_property(self):
        '''关闭性能分析'''
        s = 'SET PROFILING = 0'
        self.sql_command(s)

    def show_profiles(self):
        '''显示性能结果'''
        s = 'SHOW PROFILES'
        return self.select_command(s)

    # endregion

    # region 数据库命令
    def sql_command(self, command, commit=True):
        '''执行命令(命令,是否提交到数据库执行),一般用于改变数据库数据的操作,不会返回任何数据'''
        if commit:
            print('\033[1;31m{};\033[0m'.format(command))
            self._cursor.execute(command)
            self._base.commit()
        else:
            print('\033[1;34m{};\033[0m'.format(command))
            self._cursor.execute(command)

    def select_command(self, command):
        '''执行查询命令(命令)'''
        print('\033[1;36m{};\033[0m'.format(command))
        self._cursor.execute(command)
        datas = self._cursor.fetchall()
        return list(datas)

    def sql_commit(self):
        print('\033[1;31m db.commit()\033[0m')
        self._base.commit()

    def rollback(self):
        '''回滚上次操作'''
        print('\033[1;35m ROLLBACK();\033[0m')
        self._base.rollback()

    # endregion

    # region 工具
    def _where_to_text(self, where):
        if where is None:
            return ''

        if isinstance(where, str):
            return ' WHERE {}'.format(where)

        if isinstance(where, dict):
            where_text = ' AND '.join([
                '{}={}'.format(key, self._base.escape(value))
                for key, value in where.items()
            ])

            return ' WHERE {}'.format(where_text)

        raise Exception('类型为{}的where未定义处理方式'.format(type(where)))

    # endregion


if __name__ == '__main__':
    # 创建操作数据库的实例
    sql = zsql()
    # 创建一个库
    sql.create_db('db_name')
    # 使用库
    sql.use_db('db_name')
    # 创建一个表
    sql.create_table_ex('table_name', ID='int', name='char(16)', pwd='char(32)')
    # 保存数据
    sql.save_values('table_name', (0, '用户0', '密码0'), (1, '用户1', '密码1'))
    # 更新数据
    sql.update('table_name', new_item=dict(name='新用户名', pwd='新密码'), where=dict(name='用户1', pwd='密码1'))
    # 查询数据
    data = sql.select_all('table_name')
    # 删除表
    sql.drop_table('table_name')
    # 删除库
    sql.drop_db('db_name')
    # 显示数据
    for v in data:
        print(v)
    # 关闭
    sql.close()

    '''
    打印出以下结果
    CREATE DATABASE IF NOT EXISTS db_name DEFAULT CHARSET=utf8;
    USE db_name;
    USE db_name;
    CREATE TABLE table_name (ID int, name char(16), pwd char(32)) DEFAULT CHARSET=utf8;
    INSERT INTO table_name VALUES (0,'用户0','密码0'), (1,'用户1','密码1');
    UPDATE table_name SET name = '新用户名', pwd = '新密码' WHERE name='用户1' AND pwd='密码1';
    SELECT * FROM table_name;
    DROP TABLE IF EXISTS table_name;
    DROP DATABASE IF EXISTS db_name;
    (0, '用户0', '密码0')
    (1, '新用户名', '新密码')
    '''
