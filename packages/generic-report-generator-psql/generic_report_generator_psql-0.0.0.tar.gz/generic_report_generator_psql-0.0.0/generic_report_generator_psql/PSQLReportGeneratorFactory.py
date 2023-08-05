from generic_report_generator import ReportGeneratorFactory

from .PSQLResultDownloadStrategy import PSQLResultDownloadStrategy
from .PSQLPersistenceStrategy import PSQLPersistenceStrategy
from .PSQLDropTempTableStrategy import PSQLDropTempTableStrategy

class PSQLReportGeneratorFactory(ReportGeneratorFactory):
    def persistence_strategy(self, create_table_statement, schema, buffer_prefix, fixed_buffer_id):
        return PSQLPersistenceStrategy(
            create_table_statement,
            schema,
            buffer_prefix,
            fixed_buffer_id
        )

    def drop_all_temp_table_strategy(self, logger):
        return PSQLDropTempTableStrategy(logger)

    def result_download_strategy(self):
        return PSQLResultDownloadStrategy(self.get_db_connection())
