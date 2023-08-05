from generic_report_generator import DropTempTableStrategy

class PSQLDropTempTableStrategy(DropTempTableStrategy):
    def __init__(self, logger):
        self.logger = logger

    def list_temp_table(self, connection):
        # https://www.postgresql.org/docs/current/static/view-pg-tables.html
        rows = connection.execute("""SELECT
    tablename
FROM
    pg_catalog.pg_tables
WHERE
    schemaname LIKE 'pg_temp_%'""")
        return [row['tablename'] for row in rows]

    def drop_temp_table(self, connection, temp_table):
        connection.execute("DROP TABLE IF EXISTS \"{}\"".format(temp_table))
