###
# Author : Betacodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by Betacodings on 2019.
#############################################
#############################################
# Support Table Artisan Conducts Database querys
# Using Schema Pattern to controller callable funtions and methods
# Each method represent query builder attribute


from pytonik import App, Version, Log

app = App.App()


class Table:
    def __init__(self, table=""):
        self.DB = app.DB()
        self.prefix = self.DB.prefix
        self.table = str(self.prefix) + str(table)
        self.tabledict = table
        self.result = None
        self.rowCount = None
        self.table_from = ""
        self.table_select = ""
        self.table_exist = ""
        self.table_notexist = ""
        self.table_where = []
        self.table_wherenotin = ""
        self.table_wherein = ""
        self.table_orwhere = []
        self.table_drop = ""
        self.table_delete = ""
        self.table_value = ""
        self.table_pluck = ""
        self.table_groupby = ""
        self.table_orderby = ""
        self.table_offset = ""
        self.table_limit = ""
        self.table_join = []
        self.table_leftjoin = []
        self.table_rightjoin = []
        self.table_outerjoin = []
        self.table_whereBetween = ""
        self.table_whereNotBetween = ""
        self.table_max = ""
        self.table_min = ""
        self.table_count = ""
        self.table_distinct = ""
        self.table_avg = ""
        self.error = ""
        self.table_On = ""
        self.table_orOn = []

        return None

    def drop(self):
        self.table_drop = "DROP TABLE {exists} {table}".format(table=self.table, exists='IF ' + str(
            self.table_exist) if self.table_exist is not "" else "")
        t_result = self.query(self.table_drop)
        self.error = t_result.Exception
        return self

    def exists(self, rawquery=""):
        rawString = "WHERE EXISTS ({rawquery})".format(rawquery=rawquery) if rawquery is not "" else "EXISTS"
        self.table_exist = "{rawquery}".format(rawquery=rawString)
        return self

    def notExist(self, rawquery=""):
        rawString = "WHERE NOT EXISTS ({rawquery})".format(rawquery=rawquery) if rawquery is not "" else "NOT EXISTS"
        self.table_notexist = "{rawquery}".format(rawquery=rawString)
        return self

    def select(self, *value):

        if self.table_value is not "":
            values = self.table_value

        elif len(value) > 0:

            values = ""

        else:
            values = '*'

        if self.table_where is not "":
            _and = " AND "

            _where = ""
        else:
            _and = ""
            _where = " WHERE "

        if len(self.table_orwhere) > 0:
            _or = " OR " if _where is not "WHERE" else ''

        else:
            _or = ""

        value = value if value is not "" else ""
        self.table_select = "SELECT {value}{distinct}{values}{pluck}{max}{min}{count}{avg} FROM {table}{exists}{notexist}{outerjoin}{join}{leftjoin}{rightjoin}{where}{whereBetween}{whereNotBetween}{wherenotin}{orwhere}{groupBy}{orderBy}{limit}".format(
            distinct=self.table_distinct,
            value=','.join(value) if self.table_count is "" else '',
            values=values if self.table_count is "" else '',
            pluck=self.table_pluck if self.table_pluck is not "" else '',
            max=self.table_max,
            min=self.table_min,
            count=self.table_count if len(self.table_outerjoin) < 1 else '',
            avg=self.table_avg,
            table=self.table,
            exists=self.table_exist,
            whereBetween=str(" WHERE") + self.table_whereBetween if len(self.table_whereBetween) > 0 else '',
            whereNotBetween=str(" WHERE") + self.table_whereNotBetween if len(self.table_whereNotBetween) > 0 else '',
            notexist=self.table_notexist,
            outerjoin=" ".join(self.table_outerjoin),
            join=" ".join(self.table_join),
            leftjoin=" ".join(self.table_leftjoin),
            rightjoin=" ".join(self.table_rightjoin),
            where=str(" WHERE") + str(_and.join(self.table_where)) if len(self.table_where) > 0 else '',
            wherenotin=str(_where) + str(_and) + str(self.table_wherenotin) if len(
                self.table_wherenotin) > 0 is not "" else '',
            orwhere=str(_or) + str(_or.join(self.table_orwhere)),
            groupBy=self.table_groupby,
            orderBy=self.table_orderby,
            limit=self.table_limit
        )

        return self

    def max(self, column):
        self.table_max = ",MAX({column})".format(column=column)
        return self

    def min(self, column):
        self.table_min = ",MIN({column})".format(column=column)
        return self

    def count(self, *column):
        if len(column) > 1:
            variables = column[0] if column[0] is not "" else '*'
            columnas = column[1]
            sign = "as"
        else:
            variables = column[0] if column[0] is not "" else '*'
            sign = ""
            columnas = ""

        self.table_count = "COUNT({column}) {sign} {string} ".format(column=variables, sign=sign, string=columnas)
        return self

    def avg(self, column):
        self.table_avg = ", AVG({column})".format(column=column)
        return self

    def distinct(self, column=""):
        self.table_distinct = "DISTINCT {}".format(column=column)
        return self

    def whereAnd(self, variable="", sign="", string=""):
        string_type = "'{string}'".format(string=string) if (type(string) == str) == True else string
        self.table_distinct = "AND {variable} {sign} {string}".format(variable=variable, sign=sign, string=string_type)
        return self

    def whereIn(self, variable, list=[]):

        self.table_wherenotin = "{variable} NOT IN {list}".format(variable=variable, list='({})'.format(",".join(list)))

        return self

    def whereNotIn(self, variable, list=[]):

        self.table_wherenotin = "{variable} NOT IN {list}".format(variable=variable, list='({})'.format(",".join(list)))

        return self

    def orOn(self):
        if len(variable) > 2:
            variables = variable[0]
            sign = variable[1]
            string = variable[2]
        else:
            variables = variable[0]
            sign = '='
            string = variable[1]
        table_orOn = " OR {variable} {sign} {string}".format(variable=variables, sign=sign, string=string)

        self.table_orOn.append(table_orOn)
        return self

    def on(self):

        if len(variable) > 2:

            variables = variable[0]
            sign = variable[1]
            string = variable[2]

        else:
            variables = variable[0]
            sign = '='
            string = variable[1]

        self.table_On = " ON {variable} {sign} {string}".format(variable=variables, sign=sign, string=string)

        return self

    def orWhere(self, *variable):
        if len(variable) > 2:
            variables = variable[0]
            sign = variable[1]
            string = variable[2]
        else:
            variables = variable[0]
            sign = '='
            string = variable[1]

        string_type = "'{string}'".format(string=string) if (type(string) == str) == True else string

        table_orwhere = "{variable} {sign} {string}".format(variable=variables, sign=sign, string=string_type)
        self.table_orwhere.append(table_orwhere)

        return self

    def whereColumn(self, *variable):

        if len(variable) > 2:
            variables = variable[0]
            sign = variable[1]
            string = variable[2]
        else:
            variables = variable[0]
            sign = '='
            string = variable[1]

        if (type(variables) == tuple) == True:
            lv = []
            for v in variable:
                lv.append(" ".join(v))
            self.table_select = "SELECT FROM {table} WHERE {variable} ".format(table=self.table,
                                                                               variable=" AND ".join(lv))

        elif (type(variables) == str) == True:

            self.table_select = "SELECT FROM {table} WHERE {variable} {sign} {string} ".format(table=self.table,
                                                                                               variable=variables,
                                                                                               sign=sign, string=string)

        return self

    def whereBetween(self, column, values=[]):

        self.table_whereBetween = " {column} BETWEEN {values} ".format(column=column, values=" AND ".join(values))

        return self

    def whereNotBetween(self, column, values=[]):

        self.table_whereNotBetween = " {column} NOT BETWEEN {values} ".format(column=column,
                                                                              values=" AND ".join(values))

        return self

    def whereBetweenRaw(self, column, values=[]):

        column = " {column} BETWEEN {values} ".format(column=column, values=" AND ".join(values))

        return column

    def whereRaw(self, string):
        rawset = string
        return rawset

    def selectRaw(self, string):
        rawset = string
        return rawset

    def where(self, *variable):
        if len(variable) > 2:
            variables = variable[0]
            sign = variable[1]
            string = variable[2]
        else:
            variables = variable[0]
            sign = '='
            string = variable[1]

        string_type = "'{string}'".format(string=string) if (type(string) == str) == True else string

        table_where = " {variable} {sign} {string}".format(variable=variables, sign=sign, string=string_type)

        self.table_where.append(table_where)
        return self

    def whereNull(self, string):
        self.table_whereisnull = " WHERE {string} IS NULL".format(string=string)
        return self

    def delete(self):
        self.table_delete = "DELETE FROM {table} {where}".format(table=self.table, where=self.table_where)
        t_result = self.query(self.table_delete)
        return t_result.save() if t_result.Exception == "" else t_result.Exception

    def groupBy(self, *values):
        self.table_groupby = " GROUP BY {values}".format(values=' , '.join(values))
        return self

    def orderBy(self, value, sort):
        self.table_orderby = " ORDER BY {value} {sort}".format(value=value, sort=sort)
        return self

    def offset(self, offset=""):
        self.table_offset = str(offset) + ',' if offset is not "" else 0
        return self

    def limit(self, limits):

        self.table_limit = " LIMIT {offset} {limit}".format(offset=self.table_offset, limit=limits)
        return self

    def value(self, *values):
        self.table_value = "{values}".format(values=' , '.join(values))
        return self

    def join(self, *variable):

        if len(variable) > 3:
            table = variable[0]
            variables = variable[1]
            sign = variable[2]
            string = variable[3]
        elif len(variable) == 3:
            table = variable[0]
            variables = variable[1]
            sign = '='
            string = variable[2]
        else:

            table = variable[0]
            variables = variable[1]
            sign = ""
            string = ""

        table_join = " JOIN {table} ON {variable} {sign} {string}".format(table=str(self.prefix) + str(table),
                                                                          variable=variables, sign=sign, string=string)
        self.table_join.append(table_join)

        return self

    def outerJoin(self, *variable):

        if len(variable) > 3:
            table = variable[0]
            variables = variable[1]
            sign = variable[2]
            string = variable[3]
        elif len(variable) == 3:
            table = variable[0]
            variables = variable[1]
            sign = '='
            string = variable[2]
        else:

            table = variable[0]
            variables = variable[1]
            sign = ""
            string = ""

        table_outerjoin = " LEFT OUTER JOIN  {table} ON {variable} {sign} {string}".format(table=str(table),
                                                                                           variable=variables,
                                                                                           sign=sign, string=string)
        self.table_outerjoin.append(table_outerjoin)
        return self

    def fromTable(self, *table):

        self.table_from = "FROM {}".format("AS".join(table))
        return self

    def leftJoin(self, *variable):

        if len(variable) > 3:
            table = variable[0]
            variables = variable[1]
            sign = variable[2]
            string = variable[3]
        elif len(variable) == 3:
            table = variable[0]
            variables = variable[1]
            sign = '='
            string = variable[2]
        else:

            table = variable[0]
            variables = variable[1]
            sign = ""
            string = ""

        table_leftjoin = " LEFT JOIN {table} ON {variable} {sign} {string}".format(table=str(self.prefix) + str(table),
                                                                                   variable=variable, sign=sign,
                                                                                   string=string)

        self.table_leftjoin.append(table_leftjoin)

        return self

    def rightJoin(self, *variable):
        if len(variable) > 3:
            table = variable[0]
            variables = variable[1]
            sign = variable[2]
            string = variable[3]
        elif len(variable) == 3:
            table = variable[0]
            variables = variable[1]
            sign = '='
            string = variable[2]
        else:

            table = variable[0]
            variables = variable[1]
            sign = ""
            string = ""

        table_rightjoin = " RIGHT JOIN {table} ON {variable} {sign} {string}".format(
            table=str(self.prefix) + str(table), variable=variable, sign=sign, string=string)
        self.table_rightjoin.append(table_rightjoin)
        return self

    def pluck(self, *column):
        self.table_pluck = ",{column}".format(column=' AS '.join(column))
        return self

    def find(self, num=0):
        self.table_find = "SELECT * FROM {table} ".format(table=str(self.prefix) + str(self.table))
        t_result = self.query(self.table_find)
        r = ""
        if t_result.Exception == "":
            get = self.get()
            if get.rowCount > 0:
                rg = get.result
                for l in rg:
                    rf = {}
                    if Version.PYVERSION_MA <= 2:
                        lt = l.iteritems()
                    else:
                        lt = l.items()
                    for k, v in lt:
                        lk = l[k]
                        if lk == num:
                            r = l
            else:
                r = ""
        else:
            r = t_result.Exception

        return r

    def find(self, num=0):
        self.table_find = "SELECT * FROM {table} ".format(table=str(self.prefix) + str(self.table))
        t_result = self.DB.query(self.table_find)
        r = ""
        if t_result.Exception == "":
            get = self.get()
            if get.rowCount > 0:
                rg = get.result
                for l in rg:
                    rf = {}
                    if Version.PYVERSION_MA <= 2:
                        lt = l.iteritems()
                    else:
                        lt = l.items()
                    for k, v in lt:
                        lk = l[k]
                        if lk == num:
                            r = l
            else:
                r = ""
        else:
            r = t_result.Exception

        return r

    def update(self, data=[]):
        if (type(data) == list):
            if len(data) > 0:
                value = []
                column = []
                for l in data:
                    value.append(l)
                    if Version.PYVERSION_MA <= 2:
                        lt = l.iteritems()
                    else:
                        lt = l.items()
                    for k, v in lt:
                        if k not in column:
                            column.append('{k}="{v}"'.format(k=k, v=v))

                lcolumn = ' , '.join(column)

                table_update = "UPDATE {table} SET {column} {where}".format(table=str(self.prefix) + str(self.table),
                                                                            column=lcolumn, where=self.table_where)
                t_result = self.DB.query(table_update)
                return t_result.save() if t_result.Exception == "" else t_result.Exception
            else:
                return "Empty Data"
        else:
            return "Only Accepts type list"

    def insert(self, data=[]):
        if (type(data) == list):
            if len(data) > 0:
                ksys = []
                value = []
                val = []
                column = []
                il = 1
                for l in data:
                    value.append(l)
                    if Version.PYVERSION_MA <= 2:
                        lt = l.iteritems()
                    else:
                        lt = l.items()
                    il += 1
                    ksys.append(':{}'.format(il))
                    for k, v in lt:
                        if k not in column:
                            column.append(k)
                    val.append(tuple(l.values()))

                lcolumn = ' , '.join(column)
                kvariables = ' ,'.join(ksys)

                table_insert = "INSERT INTO  {table}  ({column}) VALUES ({kvariables}) ".format(
                    table=str(self.prefix) + str(self.table), column=lcolumn, kvariables=kvariables)

                if len(value) == 1:
                    t_result = self.DB.query(table_insert, val[0])
                else:
                    t_result = self.DB.querymultiple(table_insert, val)
                return t_result.save() if t_result.Exception == "" else t_result.Exception
            else:
                return "Empty Data"
        else:
            return "Only Accepts type list"

    def create(self):
        if type(self.tabledict) == dict:
            for table_name in self.tabledict:
                table_description = self.tabledict[table_name]
                t_result = self.DB.query(table_description)
            return t_result.save() if t_result.Exception == "" else t_result.Exception
        else:
            return "Accepts type dictionary"

    def raw(self, rawstring):
        return rawstring

    def query(self, raw):
        return self.DB.query(raw)

    def clear(self):
        if Version.PYVERSION_MA <= 2 and Version <= 7:
            self.table_where[:]
        elif Version.PYVERSION_MA == 3 and Version.PYVERSION_MI <= 3:
            self.table_where[:]
            self.table_where[:]
            self.table_orwhere[:]
        elif Version.PYVERSION_MA == 3 and Version.PYVERSION_MI >= 4:
            self.table_where.clear()
            self.table_orwhere.clear()
            self.table_join.clear()
            self.table_leftjoin.clear()
            self.table_rightjoin.clear()
            self.table_outerjoin.clear()

        self.table_select = ""
        self.table_whereBetween = ""
        self.table_whereNotBetween = ""
        self.table_from = ""
        self.table_exist = ""
        self.table_notexist = ""
        self.table_wherenotin = ""
        self.table_wherein = ""
        self.table_drop = ""
        self.table_delete = ""
        self.table_value = ""
        self.table_pluck = ""
        self.table_groupby = ""
        self.table_orderby = ""
        self.table_offset = ""
        self.table_limit = ""
        self.table_whereBetween = ""
        self.table_whereNotBetween = ""
        self.table_max = ""
        self.table_min = ""
        self.table_count = ""
        self.table_distinct = ""
        self.table_avg = ""
        self.error = ""
        self.table_On = ""

    def get(self):

        t_result = self.DB.query(self.table_select)

        self.error = t_result.Exception
        self.result = t_result.fetch()
        self.rowCount = t_result.count()
        self.clear()

        return self