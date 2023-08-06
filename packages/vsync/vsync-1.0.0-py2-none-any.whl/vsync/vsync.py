import sys
import traceback
import vsync_dal as dal
import click
import re
import random
import string
import logging


# private methods
def _gen_sync_params(ctx, source_dsn, dest_dsn, table, dest_table):
    ctx.obj['cursor_src'] = dal.connect(source_dsn, logger)
    ctx.obj['cursor_dst'] = dal.connect(dest_dsn, logger)
    ctx.obj['dbname_src'] = dal.run_sql_one_row(ctx.obj['cursor_src'], "SELECT DBNAME();")[0]
    ctx.obj['dbname_dst'] = dal.run_sql_one_row(ctx.obj['cursor_dst'], "SELECT DBNAME();")[0]
    ctx.obj['table'] = table
    ctx.obj['dest_table'] = dest_table or table
    ctx.obj['user'], ctx.obj['pwd'], ctx.obj['host_dest'], ctx.obj['port'] = dal.parse_dsn(dest_dsn)
    ctx.obj['host_src'] = dal.parse_dsn(source_dsn)[2]


@click.group()
@click.pass_context
@click.option('-f', '--force', default=False, is_flag=True, help='Do not ask for override confirmation')
@click.option('--log-file', default='/dev/null', help='Path to log file')
@click.option('--debug', type=click.Choice(['1', '2', '3']), default='2', help='Log level')
def main(ctx, force, log_file, debug):

    """Tool for syncing data between dissimilar Vertica clusters"""

    global logger
    logger = dal.logger_init(log_file, "vsync", debug)

    ctx.obj = dict()
    ctx.obj['force'] = force


@main.command(name='test-dsn-connection')
@click.pass_context
@click.option('-d', '--dsn', required=True, help='Comma separated list of DSNs to test')
def test_dsn_connection(ctx, dsn):

    """Test connection to space separated Vertica DSNs"""

    dsn = dsn.split(',')
    for d in dsn:
        logger.info("Testing {}".format(d))
        cursor = dal.connect(d, logger)
        dal.disconnect(cursor, logger)


@main.command(name='sync-table-schema')
@click.pass_context
@click.option('-s', '--source-dsn', required=True, help='Source DSN')
@click.option('-d', '--dest-dsn', required=True, help='Destination DSN')
@click.option('-t', '--table', required=True, help='Table to sync')
@click.option('--dest-table', default=None, help='Destination table, default as TABLE')
@click.option('--sync-projections/--no-projections', default=True, is_flag=True,
              help='Sync / don\'t sync projections. Default: true')
def sync_table_schema(ctx, source_dsn, dest_dsn, table, dest_table, sync_projections):

    """Sync table's schema between 2 Vertica DSNs"""

    if not 'cursor_src' in ctx.obj:
        _gen_sync_params(ctx, source_dsn, dest_dsn, table, dest_table)

    logger.info('Syncing schema of {}:{}.{} ====> {}:{}.{}'.format(ctx.obj['host_src'],
                                                                   ctx.obj['dbname_src'],
                                                                   ctx.obj['table'],
                                                                   ctx.obj['host_dest'],
                                                                   ctx.obj['dbname_dst'],
                                                                   ctx.obj['dest_table']))

    if not ctx.obj['force'] and dal.check_table_exists(ctx.obj['cursor_dst'], ctx.obj['dest_table']):
        proceed = ''
        while proceed not in ['y', 'n', 'yes', 'no']:
            logger.warn("")
            proceed = raw_input("{} exists on destination. This may cause data loss, proceed? (y/n) "
                                .format(ctx.obj['dest_table']))
        if proceed in ['n', 'no']:
            logger.info("Existing")
            sys.exit(0)

    # manipulate table's schema
    table_schema_sql = dal.get_table_schema(ctx.obj['cursor_src'], ctx.obj['table'], sync_projections=sync_projections, logger=logger)
    table_schema_sql = table_schema_sql.replace(ctx.obj['table'], ctx.obj['dest_table'])
    table_schema_sql = table_schema_sql.replace(ctx.obj['table'].split('.')[1] + '.', '')
    table_schema_sql = re.sub('\/\*.*\*\/', '', table_schema_sql)
    table_schema_sql = re.sub('SELECT MARK_DESIGN_KSAFE.*', '', table_schema_sql)
    # print table_schema_sql

    logger.info('Dropping {} if exists on destination'.format(ctx.obj['dest_table']))
    dal.run_sql_command(ctx.obj['cursor_dst'], "DROP TABLE IF EXISTS {} CASCADE;".format(ctx.obj['dest_table']))
    logger.info('Creating schema')
    dal.run_sql_command(ctx.obj['cursor_dst'], table_schema_sql)


@main.command(name='sync-table')
@click.pass_context
@click.option('-s', '--source-dsn', required=True, help='Source DSN')
@click.option('-d', '--dest-dsn', required=True, help='Destination DSN')
@click.option('-t', '--table', required=True, help='Table to sync')
@click.option('--dest-table', default=None, help='Destination table, default as TABLE')
@click.option('--sync-projections/--no-projections', default=True, is_flag=True,
              help='Sync / don\'t sync projections. Default: true')
def sync_table(ctx, source_dsn, dest_dsn, table,
               dest_table, sync_projections):

    """Sync table between 2 Vertica DSNs"""

    _gen_sync_params(ctx, source_dsn, dest_dsn, table, dest_table)

    need_to_swap = False
    orig_dest_table = ''

    if dal.check_table_exists(ctx.obj['cursor_dst'], ctx.obj['dest_table'], logger):

        if not ctx.obj['force']:
            proceed = ''
            while proceed not in ['y', 'n', 'yes', 'no']:
                logger.warn("")
                proceed = raw_input("{} exists on destination. This may cause data loss, proceed? (y/n) "
                                    .format(ctx.obj['dest_table']))
            if proceed in ['n', 'no']:
                logger.info("Existing")
                sys.exit(0)

        need_to_swap = True

        swap_table = ctx.obj['dest_table'] + '_vsync' + ''.join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(7))

        orig_dest_table = ctx.obj['dest_table']
        ctx.obj['dest_table'] = swap_table

    ctx.invoke(sync_table_schema, source_dsn=source_dsn, dest_dsn=dest_dsn,
               table=table, dest_table=ctx.obj['dest_table'], sync_projections=sync_projections)

    logger.info("Creating DB link")
    dal.db_link(ctx.obj['cursor_src'], ctx.obj['dbname_dst'], ctx.obj['user'], ctx.obj['pwd'],
                ctx.obj['host_dest'], ctx.obj['port'])  # , logger)

    logger.info('Syncing data of {}:{}.{} ====> {}:{}.{}'.format(ctx.obj['host_src'],
                                                                 ctx.obj['dbname_src'],
                                                                 ctx.obj['table'],
                                                                 ctx.obj['host_dest'],
                                                                 ctx.obj['dbname_dst'],
                                                                 ctx.obj['dest_table']))
    sync_cmd = """
                    EXPORT TO VERTICA {}.{} 
                    as 
                    SELECT * FROM {};""".format(ctx.obj['dbname_dst'], ctx.obj['dest_table'], ctx.obj['table'])
    count = dal.run_sql_row_count(ctx.obj['cursor_src'], sync_cmd, logger)[0]
    logger.info("Synced {} rows".format(count))

    if need_to_swap:
        logger.info("Swaping tables")
        dal.run_sql_command(ctx.obj['cursor_dst'],
                            "ALTER TABLE {}, {}, {} RENAME TO {}, {}, {}"
                            .format(orig_dest_table,
                                    ctx.obj['dest_table'],
                                    ctx.obj['dest_table'].split('.')[0] + '.swapTemp',
                                    'swapTemp',
                                    orig_dest_table.split('.')[1],
                                    ctx.obj['dest_table'].split('.')[1]),
                            logger)
        dal.run_sql_command(ctx.obj['cursor_dst'],
                            "DROP TABLE IF EXISTS {} CASCADE;".format(ctx.obj['dest_table']),
                            logger)


@main.command(name='sync-table-parts')
@click.pass_context
@click.option('-s', '--source-dsn', required=True, help='Source DSN')
@click.option('-d', '--dest-dsn', required=True, help='Destination DSN')
@click.option('-t', '--table', required=True, help='Table to sync')
@click.option('--dest-table', default=None, help='Destination table, default as TABLE')
@click.option('--sync-projections/--no-projections', default=True, is_flag=True,
              help='Sync / don\'t sync projections. Default: true')
@click.option('-p', '--parts', default='all', help='Comma seperated list of partitions. Default to all partitions')
def sync_table_parts(ctx, source_dsn, dest_dsn, table,
                     dest_table, sync_projections, parts):

    """Sync table between 2 Vertica DSNs"""

    _gen_sync_params(ctx, source_dsn, dest_dsn, table, dest_table)

    if not dal.check_table_exists(ctx.obj['cursor_dst'], ctx.obj['dest_table'], logger):
        logger.error("{} does not exist on destination run 'vsync sync-table-schema' and try again"
                     .format(ctx.obj['dest_table']))
        sys.exit(1)

    # get partition expression
    partition_expression_sql = """
                    SELECT partition_expression 
                    FROM v_catalog.tables 
                    WHERE table_schema || '.' || table_name = '{}'
        """.format(ctx.obj['table'])
    partition_expression = dal.run_sql_one_row(ctx.obj['cursor_src'], partition_expression_sql, logger)[0]

    # get partitions
    if parts == 'all':
        get_partitions_sql = """
                    SELECT partition_key
                    FROM v_monitor.partitions a
                    JOIN v_catalog.projections b 
                    USING (projection_id)
                    WHERE a.table_schema || '.' || b.anchor_table_name = '{}'
                    GROUP BY 1
                    ORDER BY 1;
        """.format(ctx.obj['table'])
        parts = [str(p[0]) for p in dal.run_sql_many_rows(ctx.obj['cursor_src'], get_partitions_sql, logger)]

    else:
        parts = [str(p) for p in parts.replace(', ', ',').split(',')]
        logger.info("Check if partitions exist on source")
        for part in parts:
            exists_on_src = dal.check_partition_exists(ctx.obj['cursor_src'], ctx.obj['table'], part, logger)
            if not exists_on_src:
                raise Exception("Partition {} does not exists".format(part))

    if not ctx.obj['force']:
        logger.info("Check if partitions exist on destination")
        for part in parts:
            exists_on_dest = dal.check_partition_exists(ctx.obj['cursor_dst'], ctx.obj['table'], part, logger)
            if exists_on_dest:
                proceed = ''
                while proceed not in ['y', 'n', 'yes', 'no']:
                    logger.warn("")
                    proceed = raw_input("Partitions exist on destination. This may cause data loss, proceed? (y/n) ")
                if proceed in ['n', 'no']:
                    logger.info("Existing")
                    sys.exit(0)
                else:
                    break

    logger.info("Going to export partitions: {}".format(parts))
    logger.info("Creating DB link")
    dal.db_link(ctx.obj['cursor_src'], ctx.obj['dbname_dst'], ctx.obj['user'], ctx.obj['pwd'],
                ctx.obj['host_dest'], ctx.obj['port']   , logger)

    for part in parts:
        logger.info('Syncing data of {}:{}.{}.{} ====> {}:{}.{}.{}'.format(ctx.obj['host_src'],
                                                                           ctx.obj['dbname_src'],
                                                                           ctx.obj['table'],
                                                                           part,
                                                                           ctx.obj['host_dest'],
                                                                           ctx.obj['dbname_dst'],
                                                                           ctx.obj['dest_table'],
                                                                           part))

        swap_table = ctx.obj['dest_table'] + '_vsync' + ''.join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(7))

        try:
            logger.debug("Creating swap table")
            dal.run_sql_command(ctx.obj['cursor_dst'],
                                "CREATE TABLE {} LIKE {} INCLUDING PROJECTIONS".format(swap_table, ctx.obj['dest_table']),
                                logger)

            sync_sql = """
                    EXPORT TO VERTICA {}.{}
                    as
                    SELECT * FROM {}
                    WHERE {} = '{}';
                    """.format(ctx.obj['dbname_dst'],
                               swap_table,
                               ctx.obj['table'],
                               partition_expression,
                               part)
            count = dal.run_sql_row_count(ctx.obj['cursor_src'], sync_sql, logger)[0]
            logger.info("Synced {} rows".format(count))

            logger.debug("Swapping partitions")
            dal.run_sql_command(ctx.obj['cursor_dst'],
                                "SELECT swap_partitions_between_tables('{}','{}','{}','{}');"
                                .format(ctx.obj['dest_table'],
                                        part,
                                        part,
                                        swap_table),
                                logger)

        except (Exception, KeyboardInterrupt) as e:
            logger.error(e)
            raise Exception("Failed to sync partition")

        finally:
            logger.debug("Cleaning swap table")
            dal.run_sql_command(ctx.obj['cursor_dst'],
                                "DROP TABLE IF EXISTS {} CASCADE;".format(swap_table),
                                logger)


def safe_main():
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(traceback.format_exc())
        logger.error(e)
        sys.exit(1)


if __name__ == '__main__':
    safe_main()


# TODO: test permmisions (owner, create...)
# TODO: if debug=3 print traceback
# TODO: sync resource pool, grants, users, roles




