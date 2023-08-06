import configparser
import logging
import os
import pyodbc
import time
import timeit


def logger_init(logfile, loggername, log_level):
    # type: (object, object, object) -> object
    """Initiating the logger, to write the logs for your script.

    Example:
        >> logger = logger_init(logfile="/home/dbadmin/scripts/part_rem.log", loggername="part_drop")

    :param logfile: path to the log file you want to save.
    :param loggername: the name of the logger if you want to access it again.
    :param logdir: (optional) path to the log directory you want save. if not given, it assumes `logfile` is the full
    :param log_level: default logging.INFO
    path.
    """

    if log_level == '1':
        log_level = logging.WARNING
    elif log_level == '2':
        log_level = logging.INFO
    elif log_level == '3':
        log_level = logging.DEBUG

    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=logfile, level=log_level)

    # log level colors
    logging.addLevelName(logging.DEBUG, "\033[1;36m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    logger = logging.getLogger(loggername)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(name)-12s: %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def log(logger, lvl, msg):
    """Logs a msg in a given logger, if it isn't None.

    :param logger: the logger
    :param msg: the msg to log
    :param lvl: the level of the msg (e.g. debug, warning, error, info)
    """
    levels = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10}
    if isinstance(logger, logging.Logger):
        if isinstance(lvl, str):
            lvl = levels.get(lvl.upper(), 0)
        logger.log(lvl, msg)


def connect(dsn, logger=None, autocommit=True, timeout=3):
    """Creates and returns a connection to the vertica database.
    The connection may use to execute sql queries.

    Example:
        >> cursor = connect(dsn="vertica1")

    :param dsn: dsn to connect.
    :param logger: (optional) logger to log this operation.
    :return cursor: connection to the given dsn.
    """
    try:
        os.environ['VERTICAINI'] = '/etc/vertica.ini'
        conn = pyodbc.connect("DSN=%s" % dsn, autocommit=autocommit, timeout=timeout)
        cursor = conn.cursor()
        log(logger, 'INFO', "Connected to %s successfully" % dsn)
        return cursor
    except Exception as e:
        log(logger, 'ERROR', "Vertica database connection failed")
        raise Exception(e)


def disconnect(cursor, logger=None):
    """Closes and deletes the cursor connection.

    :param cursor: cursor to disconnect.
    :param logger: (optional) logger to log this operation.
    """
    try:
        cursor.close()
        del cursor
    except Exception as e:
        log(logger, 'ERROR', e)
        raise Exception(e)


def set_resource_pool(cursor, resource_pool=None):
    """Setting resource pool.

    :param cursor: connection to the given dsn.
    :param resource_pool: (optional) the resource pool you want the select to run on.
    """
    if resource_pool:
        cursor.execute("set session resource pool %s;" % resource_pool)


def run_sql_one_row(cursor, sql, logger=None, resource_pool=None):
    """Runs sql code and returns the first result rows.

    :param cursor: cursor connection to to run the sql code.
    :param sql: sql code to run (command, query, etc.).
    :param logger: (optional) logger to log this operation.
    :param resource_pool: (optional) the resource pool you want the select to run on.
    :return row: the first result row of the sql code.
    """
    try:
        set_resource_pool(cursor, resource_pool=resource_pool)
        log(logger, 'DEBUG', "Executing sql: %s" % sql)
        start_tm = timeit.default_timer()
        row = cursor.execute(sql).fetchone()
        end_tm = timeit.default_timer()
        run_time = (end_tm - start_tm)
        log(logger, 'DEBUG', "Run time: " + str(run_time))
        return row
    except Exception as e:
        log(logger, 'ERROR', "SQL command failed")
        raise Exception(e)


def run_sql_many_rows(cursor, sql, logger=None, resource_pool=None):
    """Runs sql code and returns all result rows.

    :param cursor: cursor connection to to run the sql code.
    :param sql: sql code to run (command, query, etc.).
    :param logger: (optional) logger to log this operation.
    :param resource_pool: (optional) the resource pool you want the select to run on.
    :return rows: all result rows of the sql code.
    """
    try:
        set_resource_pool(cursor, resource_pool=resource_pool)
        log(logger, 'DEBUG', "Executing sql: %s" % sql)
        start_tm = timeit.default_timer()
        rows = cursor.execute(sql).fetchall()
        end_tm = timeit.default_timer()
        run_time = (end_tm - start_tm)
        log(logger, 'DEBUG', "Run time: " + str(run_time))
        return rows
    except Exception as e:
        log(logger, 'ERROR', "SQL command failed")
        raise Exception(e)


def run_sql_row_count(cursor, sql, logger=None, resource_pool=None):
    """Runs sql code and returns the number of rows in the result.

    :param cursor: cursor connection to to run the sql code.
    :param sql: sql code to run (command, query, etc.).
    :param logger: (optional) logger to log this operation.
    :param resource_pool: (optional) the resource pool you want the select to run on.
    :return row_count: the number of rows in the result.
    """
    try:
        set_resource_pool(cursor, resource_pool=resource_pool)
        log(logger, 'DEBUG', "Executing sql: %s" % sql)
        start_tm = timeit.default_timer()
        row_count = cursor.execute(sql).rowcount
        end_tm = timeit.default_timer()
        run_time = (end_tm - start_tm)
        log(logger, 'DEBUG', "Run time: " + str(run_time))
        if not logger:
            return int(row_count)
        return int(row_count), run_time
    except Exception as e:
        log(logger, 'ERROR', "SQL command failed")
        raise Exception(e)


def run_sql_command(cursor, sql, logger=None, resource_pool=None):
    """Runs the sql code and returns its run time.

    :param cursor: cursor connection to to run the sql code.
    :param sql: sql code to run (command, query, etc.).
    :param logger: (optional) logger to log this operation.
    :param resource_pool: (optional) the resource pool you want the select to run on.
    :return run_time: running time of the sql code (in seconds?).
    """
    try:
        set_resource_pool(cursor, resource_pool=resource_pool)
        log(logger, 'DEBUG', "Executing sql: %s" % sql)
        start_tm = timeit.default_timer()
        cursor.execute(sql)
        end_tm = timeit.default_timer()
        run_time = (end_tm - start_tm)
        log(logger, 'DEBUG', "Run time: " + str(run_time))
        return run_time  # in seconds.
    except Exception as e:
        log(logger, 'ERROR', "SQL command failed")
        raise Exception(e)


def run_sql_command_with_try(cursor, sql, max_tries=1, logger=None, sleep_time=None, **kwargs):
    """Runs the sql code and returns its run time.

    :param cursor: cursor connection to to run the sql code.
    :param sql: sql code to run (command, query, etc.).
    :param max_tries: maximum tries before error.
    :param logger: (optional) logger to log this operation.
    :param sleep_time: (optional) sleeping time (in secs) between failure to retry.
    :return run_time: running time of the sql code (in seconds?).
    """
    for try_num in range(1, max_tries + 1):
        try:
            log(logger, 'DEBUG',
                'Sql Running, try {try_num} of {max_tries}.'.format(try_num=try_num,
                                                                    max_tries=max_tries))
            run_time = run_sql_command(cursor, sql, logger=logger, **kwargs)
            break
        except Exception as e:
            log(logger, 'ERROR', 'Try number {try_num} failed.'.format(try_num=try_num))
            log(logger, 'ERROR', e)

        if sleep_time is not None:
            log(logger, 'DEBUG', 'Sleeping for {sleep_time} seconds before retry.'.format(
                sleep_time=sleep_time))
            time.sleep(sleep_time)
    else:
        log(logger, 'ERROR', 'Sql Run Failed!')
        raise Exception('Sql Run Failed!')

    log(logger, 'DEBUG',
        'Sql Run Succeeded on try {try_num} of {max_tries}.'.format(try_num=try_num,
                                                                    max_tries=max_tries))
    return run_time


def run_parallel_export(cursor, sql, path, columns, compression=None, separator=',', label=None, logger=None,
                        resource_pool=None, suffix='.csv'):
    """Runs sql and export the data to files (file per node).

    :param cursor - the cursor which is connected to the database, and can make selects on.
    :param sql - the sql command
    :param path - shared path between all nodes where the files will be created
    :param columns - string of comma seperated columns to be exported
    :param compression - compression type, default None
    :param separator - field separator, defalut , (comma)
    :param label (Optional) - sql label
    :param logger(Optional) - the logger you created to write the logs to a file.
    :param resource_pool(Optional) - the resource pool you want the select to run on.
    :return run_time: running time in seconds
    """
    if compression == 'bzip2':
        suffix = suffix + '.bz2'
    elif compression == 'gzip':
        suffix = suffix + '.gz'
    elif compression is None:
        compression = 'cat'
    else:
        raise Exception("Wrong compression type")

    export_sql = """
        SELECT /*+label({label})*/ 
          exportdata({columns}
          using parameters cmd='{compression} - > {path}',
          separator=E'{separator}')
          over (partition auto)
        FROM ({sql}) q;
    """.format(label=label,
               columns=columns,
               compression=compression,
               path=path + '_\${nodeName}' + suffix,
               separator=separator,
               sql=sql)

    try:
        set_resource_pool(cursor, resource_pool=resource_pool)
        log(logger, 'DEBUG', "Executing sql: " + str(export_sql))
        start_tm = timeit.default_timer()
        cursor.execute(export_sql)
        end_tm = timeit.default_timer()
        run_time = (end_tm - start_tm)
        log(logger, 'DEBUG', "Run time: " + str(run_time))
        return run_time
    except Exception as e:
        log(logger, 'ERROR', "Export command failed")
        raise Exception(e)


def db_link(cursor, dbname, user, pwd, host, port, logger=None):
    log(logger, 'INFO', "Creating DB link")
    run_sql_command(cursor,
                    "CONNECT TO VERTICA {} USER {} PASSWORD '{}' ON '{}',{};".format(dbname, user, pwd, host, port),
                    logger)


def get_table_schema(cursor, table, sync_projections='yes', logger=None):
    log(logger, 'INFO', "Getting table's schema")
    if sync_projections:
        return run_sql_one_row(cursor, "SELECT export_objects('','{}');".format(table), logger)[0]
    else:
        return run_sql_one_row(cursor, "SELECT export_tables('','{}');".format(table), logger)[0]


def parse_dsn(dsn, odbc_config='/etc/odbc.ini'):
    parser = configparser.RawConfigParser(allow_no_value=True)
    parser.read_file(open(odbc_config))
    user = parser.get(dsn, 'Username')
    host = parser.get(dsn, 'Servername')
    pwd = parser.has_option(dsn, 'Password') and parser.get(dsn, 'Password') or ''
    port = parser.has_option(dsn, 'Port') and parser.get(dsn, 'Port') or '5433'
    return user, pwd, host, port


def check_table_exists(cursor, table, logger):
    return run_sql_one_row(cursor,
                           """
                            SELECT table_schema || '.' || table_name 
                            FROM v_catalog.tables 
                            WHERE table_schema || '.' || table_name = '{}'
                            """.format(table),
                           logger
                           )


def check_partition_exists(cursor, table, partition_key, logger):
    return run_sql_one_row(cursor,
                           """
                            SELECT partition_key
                            FROM v_monitor.partitions a
                            JOIN v_catalog.projections b USING (projection_id) 
                            WHERE a.table_schema || '.' || b.anchor_table_name = '{}'
                            AND partition_key = '{}'
                            GROUP BY 1
                            ORDER BY 1;""".format(table, partition_key),
                          logger)
