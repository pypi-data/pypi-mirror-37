#!/usr/bin/env python   
# -*- coding:utf8 -*-   
# Author:DenisHuang
# Date:2013/11/7
# Usage:
from django.db import connections
import logging

log = logging.getLogger("django")

db = connections['default']
cursor = db.cursor()
cursor._defer_warnings = True


def get_table_fields(conn, table_name, schema=None):
    return get_table_schema(conn, table_name, schema=schema)['fields']


def switch_schema(cursor, schema=None):
    if not schema:
        schema = 'public' if cursor.db.vendor == 'postgresql' else None
    if schema:
        if cursor.db.vendor == 'postgresql':
            cursor.execute("set search_path to '%s'" % schema)


def get_table_schema(conn, table_name, schema=None):
    if schema is None:
        ps = table_name.split(".")
        table_name = ps[-1]
        schema = ps[0] if len(ps) > 1 else None
    with conn.cursor() as cursor:
        switch_schema(cursor, schema)
        from collections import OrderedDict
        fields = OrderedDict()
        introspection = conn.introspection
        primary_key_columns = None
        unique_columns_groups = []
        try:
            constraints = introspection.get_constraints(cursor, table_name)
            for c in constraints.values():
                if c['primary_key']:
                    primary_key_columns = c['columns']
                elif c['unique']:
                    unique_columns_groups.append(
                        c['columns']
                    )
        except NotImplementedError:
            constraints = {}
        primary_key_column = ",".join(primary_key_columns) if primary_key_columns else None
        unique_columns = [g[0] for g in unique_columns_groups if len(g) == 1]
        for row in introspection.get_table_description(cursor, table_name):
            name = row[0]
            field_params = OrderedDict()
            field_notes = []

            try:
                field_type = introspection.get_field_type(row[1], row)
            except KeyError:
                field_type = 'TextField'
                field_notes.append('This field type is a guess.')

            # This is a hook for data_types_reverse to return a tuple of
            # (field_type, field_params_dict).
            if type(field_type) is tuple:
                field_type, new_params = field_type
                field_params.update(new_params)

            if name == primary_key_column:
                field_params['primary_key'] = True
            elif name in unique_columns:
                field_params['unique'] = True

            # Add max_length for all CharFields.
            if field_type == 'CharField' and row[3]:
                ml = int(row[3])
                field_params['max_length'] = ml if ml > 0 else 64

            if field_type == 'DecimalField':
                if row[4] is None or row[5] is None:
                    field_notes.append(
                        'max_digits and decimal_places have been guessed, as this '
                        'database handles decimal fields as float')
                    md = row[4] if row[4] is not None else 10
                    dp = row[5] if row[5] is not None else 5
                else:
                    md = row[4]
                    dp = row[5]
                field_params['max_digits'] = md == 65535 and 100 or md
                field_params['decimal_places'] = dp == 65535 and 5 or dp
            if row[6]:  # If it's NULL...
                if field_type == 'BooleanField(':
                    field_type = 'NullBooleanField('
                else:
                    field_params['blank'] = True
                    field_params['null'] = True
            fields[name] = dict(name=name, type=field_type, params=field_params, notes=field_notes)

        return dict(
            fields=fields,
            constraints=constraints,
            primary_key_columns=primary_key_columns,
            unique_columns_groups=unique_columns_groups
        )


def create_table(conn, table, fields, schema=None, force_lower_name=False, primary_key=None):
    try:
        old_fields = get_table_fields(conn, table, schema=schema)
        return  # table exists, do nothing
    except Exception, e:
        log.warning("dbutils.create_table exception: %s", e)  # table not exists, continue

    class NoneMeta(object):
        db_tablespace = None

    class NoneModel(object):
        _meta = NoneMeta()

    fs = {}
    model = NoneModel
    from django.db.models import fields as field_types
    column_sqls = []
    with conn.schema_editor() as schema_editor:
        for k, v in fields.items():
            es = "field_types.%s('%s',%s)" % (v['type'], k, ','.join(["%s=%s" % a for a in v['params'].items()]))
            fs[k] = field = eval(es)
            field.column = force_lower_name and k.lower() or k
            definition, extra_params = schema_editor.column_sql(model, field)
            column_sqls.append("%s %s" % (
                schema_editor.quote_name(field.column),
                definition.replace('with time zone', 'without time zone'),
            ))
        full_table_name = schema and "%s.%s" % (schema, schema_editor.quote_name(table)) or schema_editor.quote_name(
            table)
        full_table_name = force_lower_name and full_table_name.lower() or full_table_name
        sql = schema_editor.sql_create_table % {
            "table": full_table_name,
            "definition": ", ".join(column_sqls)
        }
        result = schema_editor.execute(sql)
        if primary_key and ',' in primary_key:
            sql = schema_editor.sql_create_pk % {
                "table": full_table_name,
                "name": schema_editor.quote_name("%s_pk_%s") % (table, primary_key.replace(',', '_')),
                "columns": primary_key,
            }
            schema_editor.execute(sql)
        return result


def execute_sql(sql, db_name='default'):
    cur = connections[db_name].cursor()
    return cur.execute(sql), cur


def getDB(dbName='default'):
    return connections[dbName]


def getDBOptionals():
    return [(k, v["HOST"]) for k, v in connections.databases.iteritems()]


def django_db_setting_2_sqlalchemy(sd):
    emap = {"mysql": "mysql+mysqldb"}
    engine = sd['ENGINE'].split(".")[-1]
    engine = emap.get(engine, engine)
    charset = sd.get("OPTIONS", {}).get("charset")
    params = charset and "?charset=%s" % charset or ""
    return "%s://%s:%s@%s/%s%s" % (engine, sd['USER'], sd['PASSWORD'], sd['HOST'], sd['NAME'], params)


def db_sqlalchemy_str(db):
    return django_db_setting_2_sqlalchemy(connections[db].settings_dict)


def get_slave_time(db):
    con = connections[db]
    sd = con.settings_dict
    engine = sd['ENGINE'].split(".")[-1]
    sql = {
        'mysql': "show slave status",
        "postgresql": "select pg_last_xact_replay_timestamp()::timestamp without time zone  as end_time"
    }.get(engine)
    if not sql:
        return
    import pandas as pd
    from datetime import datetime, timedelta
    now = datetime.now()
    df = pd.read_sql(sql, django_db_setting_2_sqlalchemy(sd))
    # print df
    if len(df) == 1:
        if engine == 'mysql':
            sbm = df.iloc[0]['Seconds_Behind_Master']
            return now - timedelta(seconds=sbm)
        elif engine == 'postgresql':
            return df.iloc[0]['end_time']
