import csv
import tempfile
import contextlib
import os

from generic_report_generator import ResultDownloadStrategy

class PSQLResultDownloadStrategy(ResultDownloadStrategy):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection

    def download(self, from_table, csv_header):
        return _export_result_set(
            self.db_connection,
            from_table,
            csv_header
        )

@contextlib.contextmanager
def _export_result_set(db_connection, from_table, headers):
    fetch_result_sql_statement = "SELECT * FROM {table}".format(table=from_table)
    error = None
    try:
        rs = db_connection.execute(fetch_result_sql_statement)
        local_csv = _result_set_to_csv(rs, headers)
        yield local_csv
        os.remove(local_csv)
        db_connection.execute("DROP TABLE IF EXISTS {table}".format(table=from_table))
    except Exception as e:
        error = e
    finally:
        db_connection.close()
    if error is not None:
        raise error

def _result_set_to_csv(result_set, headers):
    result_path = ''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as csv_dest_file:
        result_path = csv_dest_file.name
        csv_writer = csv.writer(csv_dest_file)
        csv_writer.writerow(headers)
        for row in result_set:
            csv_writer.writerow([col for col in row])
    return result_path
